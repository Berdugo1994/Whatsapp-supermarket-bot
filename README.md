# WhatsApp-Supermarket
Wellcome to supermarket whatsapp list manager.
This tiny repo includes:
Twilio API, Flask service, MongoDB and ngrok for testing
Easily group managing supermarket list, with CRUD options such as:
Add, Update, Delete, Show.

<b>MongoDB configuriation:</b>


- 1 DB 

![alt text](https://i.postimg.cc/ZK88npDq/image.png)
- 2 collections 

![alt text](https://i.postimg.cc/jdbfpCdY/image.png)

- doc structures:

![alt text](https://i.postimg.cc/FHPJkZbh/image.png)
![alt text](https://i.postimg.cc/jC049hgp/image.png)

<b>Python - Flask configuriation:</b>
* install packages with : pip install -r requirements.txt
* set your flask env as:
FLASK_APP = app.py


* edit config.py according to your details

![alt text](https://i.postimg.cc/FKLsFgDW/image.png)

<b>To run the service type: `flask run` in cmd </b>


* you can now test the App using a client side(such as postman at localhost:5000/whatsapp_hook)

![alt text](https://i.postimg.cc/Pf3GcvMP/image.png)

* <b>ngrok</b> - If you would like to test the app using your mobile phone, you will need to integrate the twilio API with a public ip. This where ngrok comes into the picture.
download ngrok and in cmd type: ngrok http 5000 this will give you public domain, integrate it with twilio api at twilio.com (dont forget to add subdomain /whatsapp_hook)

<b> You're ready to test it with your phone!</b>


** EXAMPLE
![1](https://i.postimg.cc/V6XqttL4/image.png)
![2](https://i.postimg.cc/TPDg8bmG/image.png)

Manage your list and save time at the supermarket🥕🌶
