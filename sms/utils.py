from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

import requests

from dotenv import load_dotenv
load_dotenv()


import smtplib, ssl


from staff.models import *
from Ia.models import *
from sms.models import *


from datetime import *
from django.db.models import Max,Sum

import calendar
from calendar import monthrange

from sysadmin.models import *


from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.template.loader import render_to_string

import random




def get_termii_balance():
    url = url =settings.TERMII_SMS_BALANCE

    params = {"api_key": settings.TERMII_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    # raises error if status != 200
    # {'application': 'Thriftplus', 
    # 'balance': 4620.26, 
    # 'currency': 'NGN',
    #  'user': 'Thriftplus'} 
    return response.json()



def get_SMS_balance_buiness(branch):
    k=0


def get_SMS_balance_customer(customer):
    ip=k




def get_branch_SMS_sales(branch, transdate):
    sss = tblsmscustmerbuy.objects.filter(branch=branch, date=transdate, is_declined=False)

    if sss.count() == 0:
        total=0
    
    else:
        mt=sss.aggregate(Sum('amount'))
        mt = mt['amount__sum']
        total = int(mt)

    f={'total':total,'filter':sss}


    return f
    

def get_merchant_SMS_sales(sss,merchant):

    dds = sss.filter(merchant= merchant)

    if dds.count() == 0:
        sales=0
    
    else:
        m1=dds.aggregate(Sum('amount'))
        m2 = m1['amount__sum']
        sales = int(m2)

    return sales