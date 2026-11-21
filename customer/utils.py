
from django.core.mail import send_mail
from django.conf import settings


import smtplib, ssl

import random


# send_mail(
# 	subject,
# 	message, 
# 	EMAIL_HOST_USER, 
# 	[recepient], 
# 	fail_silently = False)



def wallet_registration(receiver_email):
    messageSent = False
    subject = "WALLET CREATED SUCCESSFULLY"
    message = "A WALLET HAS BEEN CREATED FOR YOU"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True



def generate_phone():
    krt = random.randint(1,9)
    pyb = random.randint(0,9)
    qtv = random.randint(0,9)
    bb = random.randint(0,9)
    vb = random.randint(0,9)
    hz = random.randint(0,9)
    ywq = random.randint(0,9)
    xfg = random.randint(0,9)
    zvv = random.randint(0,9)
    a = random.randint(0,9)


    pin =  str(krt) + str(pyb) + str(qtv) + str(bb)+ str(vb) + str(hz) + str(ywq) + str(xfg) + str(zvv)+ str(a)

    

    return pin



"""
'your loan is repaid for the month of %s, %d' % (month, year)

in the future, msg should be more detailed, giving the present month and year, and 
the number of months left or when the loan will be fully repaid 

"%s is %d years old." % (name, age)

moreso, we can send html emails, where u can follow a link and view the repayment history a
among other details. This is called MIME emails.........woooow
"""

