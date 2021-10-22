# Book-Store-API
This an API which has been put in place just to make you order for books, upload books with price, image and all, pay and automtically download books

# Installation
To install required packages, all you need to do is quite simple as long as you have [pip](https://pypi.org/project/pip/). There's a requirement.txt file in the root directory so run ```
pip install -r requirements.txt``` to have them installed. Ive filtered some packages you won't need but couldn't help it all

# Usage
To register, send this as post request
```yaml 
    "username": "BloggeR",
    "password": "Tobsanifedip2468",
    "email": "localhost@gmail.com",
     "country": "Isla Sala y Gómez",
    "name": "Your daddy's sister"

```
Use your informations to login which will automatically redirect you to your profile. The major links of the api can be found in the home urls.py

# Payment 
Firstly, startup your ngrok server. If you dont't know how to do so, head over [here](https://ngrok.com/download) for proper tutorial. After yve gotten your tunnel link, head on to your flutterwave dashboard and insert it to your Webhook under your settings<img width="1440" alt="Screenshot 2021-10-14 at 8 12 44 AM" src="https://user-images.githubusercontent.com/63419117/137269128-f7cbd9a9-5c64-4d1c-9a11-b8825779e8fc.png">

After that, insert the link into your `ALLOWED_HOST` in your settings.py file and your orders app views.py redirect_url above the flutterwave endpoint for your charges transaction. Also go back to your flutterwave dashboard and copy your test api secret key and put it in your orders app .env file.
