from functools import reduce
from config import *
from flask import Flask
from flask import request
from twilio.rest import Client
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient(config["mongo"]["MongoClient"])
groceries_collection = client["WhatsappSupermarket"]["groceries_collection"]
groups_collection = client["WhatsappSupermarket"]["groups_collection"]

ACCOUNT_ID = config["twilio"]["TWILIO_ACCOUNT"]
TWILIO_TOKEN = config["twilio"]["TWILIO_TOKEN"]
client = Client(ACCOUNT_ID, TWILIO_TOKEN)
TWILIO_NUMBER = config["twilio"]["TWILIO_NUMBER"]


def send_msg(msg, recipient):
    client.messages.create(
        from_=TWILIO_NUMBER,
        body=msg,
        to=recipient
    )


def check_if_user_in_group(sender):
    res = list(groups_collection.find({"user_phone": sender}))
    if len(res)==1:
        return res[0]["group_name"]
    return False


def delete_groceries(group_name):
    groceries_collection.delete_many({"group_name": group_name})

def get_groceries(group_name):
    groceries = [""] + list(groceries_collection.find({"group_name": group_name}))
    if len(groceries)>1:
        respond = reduce(lambda tmp_res, item: tmp_res + item["product"] + " " + str(item["amount"]) + "\n", groceries)
        respond += "כדי למחוק את המוצרים שלח *סיים*"
    else:
        respond = "הרשימה כבר ריקה"
    return respond


def check_if_product_exist(group, product):
    item = list(groceries_collection.find({"product": product, "group_name": group}))
    if len(item)>0:
        return str(item[0]["amount"])
    return False


def add_to_list(msg, group, sender):
    msg_splited = msg.split()
    product = msg_splited[0]
    amount = check_if_product_exist(group,product)
    if amount:
        msg = "המוצר {P} כבר ברשימה עם כמות {A}\n" \
              "לשינוי שלח: *שינוי* {P} <כמות>".format(A=amount, P=product)
        send_msg(msg, sender)
        return
    amount = 1
    if len(msg_splited) == 2 and msg_splited[1].isnumeric():
        amount = msg_splited[1]
    rec = {
        "group_name": group,
        "product": product,
        "amount": amount,
    }
    groceries_collection.insert_one(rec)


def edit_groceries(msg, group_name, sender):
    msg_splited = msg.split()
    if len(msg_splited) != 3 or not msg_splited[2].isnumeric():
        send_msg("הודעת שינוי נשלחה בפורמט לא תקין\nיש לשלוח: <שינוי> <שם-מוצר> <כמות>", sender)
        return
    product = msg_splited[1]
    new_amount = msg_splited[2]
    old_amount = check_if_product_exist(group_name, product)
    if not old_amount:
        add_to_list(msg[6:], group_name, sender)
        return
    new_value = {"$set": {"amount": new_amount}}
    groceries_collection.update_one({"product": product, "group_name": group_name}, new_value)


def delete_one_product(msg, group_name, sender):
    msg_splited = msg.split()
    if len(msg_splited) != 2:
        send_msg("הודעת מחיקה נשלחה בפורמט לא תקין\nיש לשלוח: <מחק> <שם-מוצר>", sender)
        return
    product = msg_splited[1]
    old_amount = check_if_product_exist(group_name, product)
    if not old_amount:
        # send_msg("המוצר לא היה קיים ברשימה", sender)
        return
    groceries_collection.delete_many({"product": product, "group_name": group_name})


def proccess_msg(msg, sender):
    first_word = msg.split()[0]
    group_name = check_if_user_in_group(sender)
    if not group_name:
        return "יש להיות חלק מקבוצה כדי לבצע פעולות"
    elif first_word == "רשימה":
        response = get_groceries(group_name)
        send_msg(response, sender)
    elif first_word == "סיים":
        delete_groceries(group_name)
        # send_msg("הרשימה נמחקה בהצלחה 👌", sender)
    elif first_word == "שינוי":
        edit_groceries(msg, group_name, sender)
        # send_msg("המוצר השתנה בהצלחה", sender)
    elif first_word == "מחק":
        delete_one_product(msg, group_name, sender)
    else:
        add_to_list(msg, group_name, sender)


@app.route('/whatsapp_hook', methods=["POST"])
def webhook():  # put application's code here
    f = request.form
    msg = f['Body']
    sender = f['From']
    proccess_msg(msg, sender)
    return "OK", 200


if __name__ == '__main__':
    app.run(debug=True)
