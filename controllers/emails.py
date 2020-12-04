import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from models.constants import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, REDIRECT_URL

class Emails:
    
    def send_registration_email(email, surname, password, contact, othernames, token):
        """
        Send email on sign up
        params: email, surname, password, contact, othernames,
        """
        mail_content ="""
        <h1>{surname}, Kari Hotel welcomes you!</h1>
        <h2>Enjoy best in class accomodation at Kari Hotel Uganda.</h2>
        <h2>.</h2>

        <h1>Activate your account on this link <a href="{url}/api/v1/auth/register/{token}/activate">website</a></h1>
        <h3>If you cannot view the link above Copy & paste this in your browser</h3>
        <p><b>{url}/api/v1/auth/register/{token}/activate</b></p>
        <p>Your password is: <span>{password}</span> </p>
        
        """.format(
            surname=surname,
            token=token,
            url=REDIRECT_URL,
            password=password
        )
        Emails.send_email(mail_content, 'html', email, 'KARI HOTEL WELCOMES YOU.')
        
    def send_email(mail_content, body_type, receiver_address, subject):
        #The mail addresses and password
        sender_address = MAIL_USERNAME
        sender_pass = MAIL_PASSWORD
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = subject   #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP(MAIL_SERVER, MAIL_PORT) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
    

    def send_activation_email(email,surname):
        """
        Send email on sign up
        params: email, surname, password, contact, othernames,
        """
        mail_content ="""
        <h1>{surname}, Your Account has been Successfully Activated!</h1>
        <h2>Feel free to book on our website<a href="https://kari-hotel.web.app">website</a></h2>
        <h3>If you cannot view the link above Copy & paste this in your browser</h3>
        <small><b>kari-hotel.web.app</b></small>
        """.format(
            surname=surname,
        )
        Emails.send_email(mail_content, 'html', email, 'KARI HOTEL - ACCOUNT ACTIVED.')
        #The mail addresses and password
    

    def send_purchase_email(email):
        """
        Send email on sign up
        params: email, surname, password, contact, othernames,
        """
        mail_content ="""
        <h1>Successful transaction!</h1>
        <p>Enjoy best in class accomodation at Kari Hotel Uganda.</p>
        <p>Feel free to book on our website<a href="https://kari-hotel.web.app/">website</a></p>
        <p>If you cannot view the link above Copy & paste this in your browser</p>
        <p><b>kari-hotel.web.app</b></p>
        """.format(
            surname=surname
        )
        
        Emails.send_email(mail_content, 'html', email, 'KARI HOTEL - SUCCESSFUL PAYMENT.')

