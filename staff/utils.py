

from django.conf import settings


from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import get_template

from django.template import Context


from django.template.loader import render_to_string

import random

import smtplib, ssl




def staff_registration(receiver_email, surname, password,firstname,mybranch):

    subject = 'YOUR ACCOUNT IS CREATED'
    from_email = settings.EMAIL_HOST_USER
    to = receiver_email
    link = settings.LINK



    text_content = render_to_string('staff/team_login.txt', {'company':mybranch,'link':link, 'surname': surname,
        'firstname': firstname,
        'password':password,
        'email':receiver_email})


    html_content = render_to_string('staff/team_login.html', {'company':mybranch,'link':link, 'surname': surname, 
        'firstname': firstname,
        'password':password,
        'email':receiver_email})



    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    result = msg.send()

    return result







def generate_staff_pin():
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
    hzp = random.randint(0,9)
    yq = random.randint(0,9)
    xj = random.randint(0,9)
    zp = random.randint(0,9)
    au = random.randint(0,9)
    pin =  str(krt) + str(pyb) + str(qtv) + str(bb)+ str(vb) + str(hz) + str(ywq) + str(xfg) + str(zvv)+ str(a) 

    return pin



def generate_password():
    krt = random.randint(0,9)
    pyb = random.randint(0,9)
    qtv = random.randint(0,9)
    bb = random.randint(0,9)
    vb = random.randint(0,9)
    hz = random.randint(0,9)

    password =  str(krt) + str(pyb) + str(qtv) + str(bb)+ str(vb) + str(hz)

    return password

def staff_registrationtt(receiver_email, surname, password):
    plaintext = get_template('staff/team_login.html')
    htmly     = get_template('staff/team_login.html')
    link = settings.LINK


    subject = 'YOUR ACCOUNT IS CREATED'
    from_email = settings.EMAIL_HOST_USER
    to = receiver_email


    # ✅ Use a plain dict, not Context
    d = { 
        'username': surname,
        'password': password,
        'email': receiver_email,
        'link': link 
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    text_content = render_to_string('staff/team_login.txt', { 'surname': firstname,'business':business,'password':password,'email':receiver_email})
    html_content = render_to_string('staff/team_login.html', { 'surname': firstname,'business':business,'password':password,'email':receiver_email})


    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()