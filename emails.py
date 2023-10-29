# from fastapi import BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from schemas import *
import jwt

SECRETS = '24bee0493c01b636e8a0fefb5beb37e7420eee7b'

conf = ConnectionConfig(
    MAIL_USERNAME="wevukus@hotmail.com",
    MAIL_PASSWORD="trythemailNOW123$",
    MAIL_FROM="wevukus@hotmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.hotmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)




async def send_email(email: EmailSchema, instance: Login):
    token_data = {
    "id": instance.id,
    "username": instance.username
    }

    token = jwt.encode(token_data, SECRETS)

    template = f""" <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    <div style="display: flex; align-items: center; justify-content: center; flex-direction; column">
    I
    <h3>Account Verification </h3>
    <br>"""

    
    message= MessageSchema(
        subject = "EasyShopas Account Verification Email", 
        recipients = email, #LIST OF RECIPIENTS,
        body = template,
        subtype="html"
    )

    fm = FastMail(conf)
    fm.send_message(message=message)
    