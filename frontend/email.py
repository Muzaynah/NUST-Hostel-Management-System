import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()

server.login('nusthostelmanagement@gmail.com','dlbw nljx rwpu pxfd')

server.sendmail('nusthostelmanagement@gmail.com', '##Students email##', 'first mail')

print('Mail sent')

