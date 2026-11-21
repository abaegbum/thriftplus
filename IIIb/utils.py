

from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

import smtplib, ssl


from staff.models import *
from Ia.models import *
from IIIb.models import *
from datetime import *
from django.db.models import Max,Sum
from calendar import monthrange



from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.template.loader import render_to_string

import random





def active_saving_scheme(branch):
    ppp = tblstandardsavingIIIB.objects.filter(branch=branch,active=True).exclude(description='-----')

    d=[]
    tdate=datetime.today()
    month_index=tdate.month #month_index

    for gh in ppp :

        starts = gh.from_month
        starts = datetime.strptime(starts,"%B") #converts month_name to month_index
        starts_index=starts.month

        stopp = gh.to_month
        stopp = datetime.strptime(stopp,"%B") #converts month_name to month_index
        stopp_index=stopp.month

        if month_index < starts_index:
            msg = 'This scheme is not yet open'
        
        elif month_index > stopp_index:
            msg = "This scheme is closed"
            
        else:
            d.append(gh)

    # d.append(paa[0])

    return d


def deposit_email(receiver_email,surname,firstname,amount,month,year):
    plaintext = get_template('IIIb/email.txt')
    htmly     = get_template('IIIb/deposit_email.html')

    d = Context({ 'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'month': month,
        'year': year })

    subject = 'THRIFTPLUS'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()




def savingscheme_email(mybranch,receiver_email,coop,amount,year,package,a,b):

    subject = 'YOUR APPICATION IS SUCCESSFUL'
    from_email = settings.EMAIL_HOST_USER
    to = receiver_email
    surname=coop.staff.surname
    firstname=coop.staff.firstname


    html_content = render_to_string('IIIb/mysavings_apply_email.html',{'company':mybranch, 'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'package':package,
        'start':a,
        'end':b,
        'year': year})


    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    result = msg.send()

    return 'kk'



def loanbook_email(mybranch,receiver_email,surname,firstname,amount,coop_man):
    subject = 'LOAN APPLICATION SUCCESSFUL'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email


    html_content = render_to_string('IIIb/loan-request-email.html',{'company':mybranch, 
        'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'coop_man': coop_man})


    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    result = msg.send()

    return 'kk'




def loanapproval_email_one(mybranch,receiver_email):

    subject = 'YOUR LOAN IS AWAITING DISBURSAL'
    from_email= settings.EMAIL_HOST_USER
    # to = receiver_email

    coop = tblIIIbcoop.get(staff=email.id)
    surname=coop.staff.surname
    firstname=coop.staff.firstname
    amount=email.amount
    month = email.month
    year=email.year

    html_content = render_to_string('IIIb/approved_loan_email.html',{'company':mybranch, 'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'year': year,
         'month': month})


    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    result = msg.send()

    return 'kk'




def loanapproval_email_many(mybranch,allscsenario,allcoop):

    subject = 'YOUR LOAN IS AWAITING DISBURSAL'
    from_email= settings.EMAIL_HOST_USER


    # coop = tblIIIbcoop.objects.filget(staff=email.staff.id)

    

    for email in allscsenario :
        coop = allcoop.get(staff=email.staff.id)
        surname=coop.staff.surname
        firstname=coop.staff.firstname
        amount=email.principal
        month = email.month
        year=email.year
        to=email.staff.staff.email


        html_content = render_to_string('IIIb/approved_loan_email.html',{'company':mybranch, 'surname': surname,
            'firstname': firstname,
            'amount': amount,
            'year': year,
             'month': month})


        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        result = msg.send()

    return 'kk'



def loandisbursal_email(mybranch,receiver_email,surname,firstname,amount):

    subject = 'YOUR LOAN IS DISBURSED'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email


    html_content = render_to_string('IIIb/approved_loan_email.html',{'company':mybranch, 'surname': surname,
        'firstname': firstname,
        'amount': amount,
        'year': year,
         'month': month})


    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    result = msg.send()

    return 'kk'



def generate_trans_pin():
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
    pin =  str(krt) + str(pyb) + str(qtv) + str(bb)+ str(vb) + str(hz) + str(ywq) + str(xfg) + str(zvv)+ str(a) + str(hzp) + str(yq) + str(xj) + str(zp)+ str(au)

    return pin




def walletbalance(mybranch,coop):


    sav_all=tblIIIbsavingsaccount.objects.filter(branch=mybranch,staff=coop)


    sav=sav_all.filter( status='CR',  account_type='Wallet')

    if sav.count()>0:
        add_cr=sav.aggregate(Sum('amount'))
        add_cr = add_cr['amount__sum']
    else:
        add_cr = 0


    lr=sav_all.filter( status='CR',  account_type='Loan Repayment')

    if lr.count()>0:
        add_lr=lr.aggregate(Sum('amount'))
        add_lr = add_lr['amount__sum']
    else:
        add_lr = 0



    crp=sav_all.filter( status='CR',  account_type='Commodities Repaymment')

    if crp.count()>0:
        add_crp=crp.aggregate(Sum('amount'))
        add_crp = add_crp['amount__sum']
    else:
        add_crp = 0




    sav_dr=sav_all.filter(status='DR', account_type='Loan')

    if sav_dr.count()>0 :
        add_dr=sav_dr.aggregate(Sum('amount'))
        add_dr = add_dr['amount__sum']
    else:
        add_dr =0

    sav_com=sav_all.filter(status='DR', account_type='Commodities')

    if sav_com.count()>0 :
        add_com=sav_com.aggregate(Sum('amount'))
        add_com = add_com['amount__sum']
    else:
        add_com =0


    amount=add_cr + add_lr + add_crp - add_dr - add_com 

    return amount



def otherbalance(mybranch,coop):


    bb = tblstandardsavingIIIB.objects.filter(branch=mybranch).exclude(description='Wallet')

    bb2=[a.description for a in bb]


    others=tblIIIbsavingsaccount.objects.filter(branch=mybranch,status='CR', staff=coop,account_type__in =bb2)

    if others.count()>0:

        kadd=others.aggregate(Sum('amount'))
        kadd_cr = kadd['amount__sum']
    else:
        kadd_cr = 0


    myothers=kadd_cr 

    
    return myothers


def checksub(branch,service):
    mybranch=tblBRANCH.objects.get(id=branch)


    sub_history = tblsubscription.objects.filter(branch=mybranch,app='Coop')#for coops

    uy= [x.id for x in sub_history]
    return uy
    suhi=sub_history.get(id=uy[-1])

    if suhi.status =='Queing':
        history=sub_history.get(id=uy[-2])

    else:
        history=sub_history.get(id=uy[-1])

    details= {'status':history.status,
    'staff_count':history.package.staff_count,
    'customer_count':history.package.customer_count,
    'package':history.package.package,
    'appendage':history.package.appendage,
    'stop':history.end}
    return details