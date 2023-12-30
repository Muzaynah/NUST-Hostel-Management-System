import smtplib
import random

def sendEmail(email,emailType):
    if(emailType=="forgot password"):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('nusthostelmanagement@gmail.com','dlbw nljx rwpu pxfd')
        otp = generate_otp()
        email_text = f'''
                Your One-Time Password is {otp}.
                
                If you did not click on Forgot Password, someone else is trying to change your password.
            '''
        server.sendmail('nusthostelmanagement@gmail.com', email, email_text)
        print('Mail sent')
        return otp

def generate_otp():
    return str(random.randint(1000, 9999))