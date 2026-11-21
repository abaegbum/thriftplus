from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

import smtplib, ssl


from staff.models import *
from Ia.models import *
from datetime import *
from django.db.models import Max,Sum

import calendar
from calendar import monthrange

from sysadmin.models import *


from django.db.models import Max,Sum
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.template.loader import render_to_string

import random









def rewrite_programme_filed(branch,dd):

    mybranch=tblBRANCH.objects.get(id=branch)
    memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

    allmmm=tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,esusu1a=1,id=87)


    dy=[]

    for m in allmmm:
        mer = m.id
        sss = tblIafieldagent.objects.filter(merchant=m,recdate=dd, is_declined= False)#[0:2]#get_item

        for vv in sss:

            ccc = vv.customer.id
            ccc=tblIaCUSTOMER.objects.get(id=ccc)


            fg = tblIamerchantBank.objects.filter(merchant=m, recdate=dd,customer=ccc,code=vv.code,transac_id=vv.transac_id)


            fg2 = tblIasavings_trans.objects.filter(merchant=m, recdate=dd,customer=ccc,code=vv.code,transac_id=vv.transac_id)



            d={'fd':vv,'ffn':fg,'mb':fg2}

            dy.append(d)



    return 'ok'




def television(branch,dd):

    mybranch=tblBRANCH.objects.get(id=branch)
    memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


    allmmm = tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,esusu1a=1)

    allmmm=tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,esusu1a=1,id=87)


    dy=[]

    for m in allmmm:
        mer = m.id
        sss = tblIafieldagent.objects.filter(merchant=m,recdate=dd, is_declined= False)#[0:2]#get_item

        for vv in sss:

            ccc = vv.customer.id
            ccc=tblIaCUSTOMER.objects.get(id=ccc)


            fg = tblIamerchantBank.objects.filter(merchant=m, recdate=dd,customer=ccc,code=vv.code,transac_id=vv.transac_id)


            fg2 = tblIasavings_trans.objects.filter(merchant=m, recdate=dd,customer=ccc,code=vv.code,transac_id=vv.transac_id)



            d={'fd':vv,'ffn':fg,'mb':fg2}

            dy.append(d)



    return 'ok'




def passwordlink(receiver_email,password,company):

    subject = 'Your password just arrived'
    from_email = settings.EMAIL_HOST_USER
    to = receiver_email
    # to = 'njo4mi@gmail.com'

    text_content = render_to_string('passlink.txt', { 'company': company,'password':password ,'email':receiver_email})
    html_content = render_to_string('passlink.html', { 'company': company,'password':password,'email':receiver_email })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

##Sending alternative content types
def customer_activationIaa(emails):
    subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def another_one(receiver_email,wallet,account,thrift,month,year):
    plaintext = get_template('Ia/email.txt')
    htmly     = get_template('Ia/deposit_email.html')

    d = Context({ 'email': email,
        'wallet': wallet,
        'account': account,
        'thrift': thrift,
        'month': month,
        'year': year })

    subject = 'ACCOUNT CREDITED SUCCESFULLY'
    from_email= settings.EMAIL_HOST_USER
    to = receiver_email

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def rrt(receiver_email):
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()



def customer_activationIa(receiver_email):
    messageSent = False
    subject = "Daily Contribution activation"
    message = "YOU HAVE SUCCESFULLY BEEN ACTIVATED FOR DAILY CONTRIBUTION"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True




def straightenout(request):
    branch=tblBRANCH.objects.get(id=12)
    t = tblIathrift.objects.filter(branch=branch,month='October')
    mm = tblIaMERCHANT.objects.get(branch=branch,id=35)


    d=[]

    for k in t:
        sac = tblIasavings_trans.objects.filter(description='Account Maintenance',
            branch=branch,code=k.code,merchant=mm)

        tt= sac.count()
        if int(tt) >0:
            for pp in sac:
                rr = tblIamerchantBank.objects.get(transac_id=pp.transac_id)

                kp =tblIasavings_trans.objects.filter(transac_id=rr.transac_id)
                kp.delete()

                tblIasavings_trans(branch=branch,
                    merchant=rr.merchant,
                    transac_id=rr.transac_id,
                    code=rr.code,
                    customer=rr.customer,
                    number=rr.number,
                    recdate=rr.transdate,
                    transdate=pp.transdate,
                    amount=rr.amount,
                    status='CR',
                    year=rr.year,
                    purpose = rr.purpose,
                    wallet_type='Main',
                    avalability='Available',
                    description='Credit').save()



    for k in t:
        sac = tblIasavings_trans.objects.filter(description='Account Maintenance',
            branch=branch,code=k.code,merchant=mm)
        tt= sac.count()
        if int(tt) >0:
            h={'customer':str(k.code),'count':tt}
            d.append(h)
    return render_to_response('Ia/selectloan.html',{'msg':d})



def register_field_officerIa(receiver_email):
    messageSent = False
    subject = "Field officer activation"
    message = "YOU HAVE SUCCESFULLY BEEN ACTIVATED AS A FIELD OFFICER"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True


def Direct_crediting_email(receiver_email):
    messageSent = False
    subject = "ACCOUNT CREDITED SUCCESSFULLY"
    message = "YOUR ACCOUNT HAS BEEN CREDITED SUCCESFULLY"
    send_mail(subject,
    	message,
    	settings.EMAIL_HOST_USER,
    	[receiver_email],
    	fail_silently=False)
    messageSent = True




def Direct_creditingIa(receiver_email,surname,thrift,amount,month):


    subject = 'Your account is credited'
    from_email = settings.EMAIL_HOST_USER
    to = receiver_email
    # to = 'njo4mi@gmail.com'

    text_content = render_to_string('Ia/direct_credit.txt', { 'surname': surname,'thrift':thrift,'amount':amount })
    html_content = render_to_string('Ia/direct_credit.html', { 'surname': surname,'month':month,'thrift':thrift,'amount':amount })

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()



def direct_depositIa(receiver_email):
    messageSent = False
    subject = "ACCOUNT CREDITED SUCCESSFULLY"
    message = "YOUR ACCOUNT WAS CREDITED SUCCESFULLY"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = True


def direct_withrawalIa(receiver_email):
    messageSent = False
    subject = "CASH WITHDRAWAL SUCCESSFUL"
    message = "YOU HAVE SUCCESFULLY WITHDRAWN FROM YOUR ACCOUNT"
    send_mail(subject,
        message,
        settings.EMAIL_HOST_USER,
        [receiver_email],
        fail_silently=False)
    messageSent = Truee




def appropriate_thrift(mybranch, year,monthname,wallet,cycle,card):


    details=tblCUSTOMER.objects.get(branch=mybranch,
        wallet=wallet,status=True)

    treu = tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)

    thriftrec=tblIathrift.objects.filter(branch=mybranch,
        purpose=card,
        year=year,
        month=monthname,
        cycle=cycle,
        customer=treu)

    if thriftrec.count() == 0:
        return 0

    elif thriftrec.count() == 1:
        return thriftrec.get()

    else:
        return 5



def view_thrift(month,user,wallet,cycle,card):


    www=int(month)

    monthname = calendar.month_name[www]

    staff = Userprofile.objects.get(email=user,status=True)
    staffid = staff.staffrec.id
    mybranch=staff.branch.id
    mybranch=tblBRANCH.objects.get(id=mybranch,status=True)

    memmerchant=tblIaMERCHANT.objects.get(thrift1a =1, staff= staffid ,status=True)
    fth = date.today()
    yyrp = fth.year


    details=tblCUSTOMER.objects.get(
        wallet=wallet,
        status=1)

    treu = tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)

    thriftrec=tblIathrift.objects.get(branch=mybranch,
        cycle = cycle,
        year=yyrp,
        purpose=card,
        month=monthname,
        customer=treu)

    return thriftrec





def whatsloanbal(code):


    kk = tblloandetails.objects.get(code=code)

    details= tblloanrepay.objects.filter(loan=kk)

    if details.count() > 0:

        pd = details.aggregate(Sum('repaid'))
        pd = int(pd['repaid__sum'])
    else:
        pd = 0

    bal= int(kk.repayment) - pd

    rt = {'loan':kk,'bal':bal,'details':details,'repaid':pd}



    return rt

def appropriate_thrift_history(month,user,wallet,cycle,card):


    www=int(month)

    monthname = calendar.month_name[www]

    staff = Userprofile.objects.get(email=user,status=True)
    staffid = staff.staffrec.id
    mybranch=staff.branch.id
    mybranch=tblBRANCH.objects.get(id=mybranch,status=True)

    memmerchant=tblIaMERCHANT.objects.get(thrift1a =1, staff= staffid ,status=True)
    fth = date.today()
    yyrp = fth.year


    details=tblCUSTOMER.objects.get(
        wallet=wallet,
        status=1)

    treu = tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)

    thriftrec=tblIathrift.objects.get(branch=mybranch,
        cycle=cycle,
        purpose=card,
        year=yyrp,
        month=monthname,
        customer=treu)

    return thriftrec



def factcheck(ddate,workers,mybranch):


    stf = tblIafieldagent.objects.filter(branch = mybranch, recdate=ddate,is_declined= False)
    bb= tblIamerchantBank.objects.filter(branch = mybranch,recdate=ddate,status='CR')
    cus= tblIasavings_trans.objects.filter(branch = mybranch,recdate=ddate,status='CR')
    product='Savings'
    ww=tblIaMERCHANT.objects.filter(branch=mybranch)

    dy=[]
    dp=[]

    drt = 0

    for wk in workers:
        w=ww.get(id=wk)

        g = stf.filter(merchant=w,status='Approved',is_declined= False)
        if g.count() >0:

            stafff = g.aggregate(Sum('amount'))
            stafff = int(stafff['amount__sum'])
        else:
            stafff=0

        biz= bb.filter(merchant=w,  status='CR',  product=product)

        if biz.count() >0:

            bzz = biz.aggregate(Sum('amount'))
            bzz = int(bzz['amount__sum'])

        else:
            bzz = 0


        cuzz= cus.filter(merchant=w, status='CR',product= product)

        if cuzz.count() >0:
            ccc = cuzz.aggregate(Sum('amount'))
            ccc = int(ccc['amount__sum'])
        else:
            ccc=0



        diff = stafff - ccc



        if stafff == 0:
            drt =drt + 0
            diff = 0
            selected= "unchecked"
            disabled = 'disabled'

        elif stafff ==bzz == ccc:
            drt =drt + 0
            selected= "unchecked"
            disabled = 'disabled'
        else:
            drt =drt +1
            selected= "checked"
            disabled = 'enable'



        vb= {'sss':stafff,'bbbb':bzz,'cus':ccc,'worker':w,
        'switch':selected,
        'dif':diff,'disabled':disabled}

        dy.append(vb)

    f= {'dy':dy}

    swi = {'drt':drt}


    dp.append(f)
    dp.append(swi)

    return dp




def factcheck2_ori(frrmdate,todate,workers,mybranch):#the dates are in str form


    a,b,c=frrmdate.split("-")
    a=int(a)
    b=int(b)
    c=int(c)

    x,y,z=todate.split("-")
    x=int(x)
    y=int(y)
    z=int(z)

    test_months = range(b,y+1)


    dp=[]
    dy=[]

    fff =0


    for k in test_months: # test_months is the months covered in the search
        monthname=calendar.month_name[int(k)]

        if k == test_months[0]: #if month is the first month
            if k == test_months[-1]: # if k is last month

                start_date= c #start
                end_date= z #end date
                fff= fff + start_date #increment

            else:
                start_date= c
                end_date = (monthrange(x, k))[-1]
                fff= fff + start_date

        else:
            if k == test_months[-1]:
                start_date= 1
                end_date = z
                fff= fff + start_date

            else:
                start_date= 1
                end_date = (monthrange(x, k))[-1]
                fff= fff + start_date

        while fff <= end_date:
            # dp7 = rrr(a,k,fff,mybranch,workers)


            frrmdate =date(a,k,fff) #python version of the date
            s1 = str(a) + '-' +str(k) +'-'+str(fff)  #str version of the date


            stf = tblIafieldagent.objects.filter(branch = mybranch, recdate=frrmdate)
            bb= tblIamerchantBank.objects.filter(branch = mybranch,recdate=frrmdate)
            cus= tblIasavings_trans.objects.filter(branch = mybranch,recdate=frrmdate)


            for wk in workers:
                w=tblIaMERCHANT.objects.get(id=wk)

                g = stf.filter(merchant=w,recdate=frrmdate,status='Approved',is_declined= False)
                if g.count() >0:

                    stafff = g.aggregate(Sum('amount'))
                    stafff = int(stafff['amount__sum'])
                else:
                    stafff=0

                biz= bb.filter(merchant=w,
                                recdate=frrmdate,
                                status='CR',
                                description='Credit',
                                product='Savings')

                if biz.count() >0:

                    bzz = biz.aggregate(Sum('amount'))
                    bzz = int(bzz['amount__sum'])

                else:
                    bzz = 0


                cuzz= cus.filter(merchant=w,
                                 recdate=frrmdate,
                                 product='Savings',
                                 status='CR')

                if cuzz.count() >0:
                    ccc = cuzz.aggregate(Sum('amount'))
                    ccc = int(ccc['amount__sum'])
                else:
                    ccc=0


                if stafff == bzz == ccc:
                    pass
                else:
                    vb= {'ddate':frrmdate}
                    dy.append(vb)


            [dp.append(item) for item in dy if item not in dp]



            fff +=1

        k +=1

    return dp




def factcheck2(frrmdate,todate,workers,mybranch):#the dates are in str form


    a,b,c=frrmdate.split("-")
    a=int(a) #year
    b=int(b) #month
    c=int(c) #day

    x,y,z=todate.split("-")
    x=int(x) #year
    y=int(y) #month
    z=int(z) #day

    test_months = range(b,y+1)


    dp=[]
    dy=[]


    fff =0

    start_date= 0
    end_date=0


    for kkk in test_months: # test_months is the months covered in the search
        monthname=calendar.month_name[int(kkk)]

        if kkk == test_months[0]: #if month is the first month
            if kkk == test_months[-1]: # if k is last month

                start_date= c #start
                end_date= z #end date
                fff= fff + start_date #increment

            else:
                start_date= c
                end_date = (monthrange(x, kkk))[-1]
                fff= fff + start_date

        else:
            if kkk == test_months[-1]: #if month is second and last month
                start_date= 1
                end_date = z
                fff= fff + start_date

            else: #if month is second
                start_date= 1
                end_date = (monthrange(x, kkk))[-1]
                fff= fff + start_date


        # frrmdate =date(a,kkk,fff)



        while fff <= end_date:
            # dp7 = rrr(a,k,fff,mybranch,workers)


            frrmdate =date(a,kkk,fff) #python version of the date
            s1 = str(a) + '-' +str(kkk) +'-'+str(fff)  #str version of the date


            stf = tblIafieldagent.objects.filter(branch = mybranch, recdate=frrmdate)
            bb= tblIamerchantBank.objects.filter(branch = mybranch,recdate=frrmdate,status='CR')
            cus= tblIasavings_trans.objects.filter(branch = mybranch,recdate=frrmdate,status='CR')


            for wk in workers:
                w=tblIaMERCHANT.objects.get(id=wk)

                g = stf.filter(merchant=w,recdate=frrmdate,status='Approved',is_declined= False)
                if g.count() >0:

                    stafff = g.aggregate(Sum('amount'))
                    stafff = int(stafff['amount__sum'])
                else:
                    stafff=0

                biz= bb.filter(merchant=w,
                                recdate=frrmdate,
                                status='CR',
                                description='Credit',
                                product='Savings')

                if biz.count() >0:

                    bzz = biz.aggregate(Sum('amount'))
                    bzz = int(bzz['amount__sum'])

                else:
                    bzz = 0


                cuzz= cus.filter(merchant=w,
                                 recdate=frrmdate,
                                 product='Savings',
                                 status='CR')

                if cuzz.count() >0:
                    ccc = cuzz.aggregate(Sum('amount'))
                    ccc = int(ccc['amount__sum'])
                else:
                    ccc=0


                if stafff == bzz == ccc:

                    NB=0
                    # vb = {'ddate':stafff}
                else:
                    dd=a +kkk + fff
                    vb= {'ddate':frrmdate,'dd':dd}

                    dy.append(vb)


            [dp.append(item) for item in dy if item not in dp]



            fff +=1



        fff =0
        start_date= 0
        end_date=0

    return dp


def rrr(y,m,d,mybranch,workers):

    dy =[]
    dp=[]
    frrmdate =date(y,m,d) #python version of the date
    s1 = str(y) + '-' +str(m) +'-'+str(d)  #str version of the date



    stf = tblIafieldagent.objects.filter(branch = mybranch, recdate=frrmdate)
    bb= tblIamerchantBank.objects.filter(branch = mybranch,recdate=frrmdate)
    cus= tblIasavings_trans.objects.filter(branch = mybranch,recdate=frrmdate)


    for wk in workers:
        w=tblIaMERCHANT.objects.get(id=wk)

        g = stf.filter(merchant=w,recdate=frrmdate,status='Approved',is_declined= False)
        if g.count() >0:

            stafff = g.aggregate(Sum('amount'))
            stafff = int(stafff['amount__sum'])
        else:
            stafff=0

        biz= bb.filter(merchant=w,
                        recdate=frrmdate,
                        status='CR',
                        description='Credit',
                        product='Savings')

        if biz.count() >0:

            bzz = biz.aggregate(Sum('amount'))
            bzz = int(bzz['amount__sum'])

        else:
            bzz = 0


        cuzz= cus.filter(merchant=w,
                         recdate=frrmdate,
                         product='Savings',
                         status='CR')

        if cuzz.count() >0:
            ccc = cuzz.aggregate(Sum('amount'))
            ccc = int(ccc['amount__sum'])
        else:
            ccc=0


        if stafff == bzz == ccc:
            pass
        else:
            vb= {'ddate':s1}
            dy.append(vb)


    [dp.append(item) for item in dy if item not in dp]


    return dp




def thrift_balancer(branch_id,email):

    mybranch=tblBRANCH.objects.get(id=branch_id)
    gh=[]
    ad=[]

    s= tblIasavings_trans.objects.filter(branch=mybranch,status='CR')
    t = tblIathrift.objects.filter(branch=mybranch)


    [gh.append(a.code) for a in s if a.code not in gh]

    for thrift_code in gh:
        savings=s.filter(code=thrift_code)

        customer_code= t.get(code=thrift_code).customer.code

        svc = savings.aggregate(Sum('number'))
        total_save = int(svc['number__sum'])

        ad2 = after_deposit(t,total_save)

        ad.append(ad2)

    return 'ok'


def account_balance_gen_saving(account):

    cus=tblIaCUSTOMER.objects.get(id =account)

    sav=tblIbbsavings_trans.objects.filter(customer=cus,
        wallet_type='Main',
        # status='Available',
        # avalability='Available'
        )

    sav_CR = sav.filter(status='CR')

    # sav=tblIbbsavings_trans.objects.filter(customer=cus,
    #     wallet_type='Main',
    #     status='Available',
    #     avalability='Available',
    #     description='CR')
        # msg = sav
        # return render_to_response('Ib/selectloan.html',{'msg':msg})

    if sav_CR.count()>0:
        add=sav_CR.aggregate(Sum('amount'))
        add_cr = add['amount__sum']
    else:
        add_cr = 0


    # sav_dr=tblIbbsavings_trans.objects.filter(customer=cus,description='DR')
    sav_dr=sav.filter(status='DR')

    if sav_dr.count()>0 :
        add=sav_dr.aggregate(Sum('amount'))
        add_dr = add['amount__sum']
    else:
        add_dr =0

    amount= add_cr - add_dr

    return amount




def fieldofficersales(merchant,recdate,status):


    mm = tblIaMERCHANT.objects.get(id=merchant)

    d,m,y=recdate.split('/')
    y=int(y)
    m=int(m)
    d=int(d)

    dpp = calendar.day_name[calendar.weekday(y,m,d)]

    recdate=date(y,m,d)
    ddt=[]


    if status =='Unapproved':


        thriftrec = tblIafieldagent.objects.filter(merchant=mm,
            recdate = recdate,
            is_declined = False,
            wallet_type='Main',
            status=status)

    elif status == 'Approved':
        thriftrec = tblIafieldagent.objects.filter(merchant=mm,
                recdate = recdate,
                is_declined = False,
                wallet_type='Main',
                status=status)

    mycount= thriftrec.count()


    if mycount >0:
        add=thriftrec.aggregate(Sum('amount'))
        add = int(add['amount__sum'])
        dl={'amount':add}
        ddt.append(dl)


    g={'record':thriftrec,'sales':add,'dow':dpp,'merchant':mm}






    return g



def selenco(bra,fd,td):


    mybranch= tblBRANCH.objects.get(id = bra)
    allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=True,thrift1a=1)

    dday,mday,yday = fd.split('/') #JSON Dates Object
    yday=int(yday)
    fmday=int(mday)
    fday=int(dday)

    fd=date(yday,fmday,fday)

    dday,mday,yday = td.split('/') #JSON Dates Object
    yday=int(yday)
    tmday=int(mday)
    tday=int(dday)


    td=date(yday,tmday,tday)


    if fmday <= tmday:
        a = range(fmday,tmday+1)
    else:
        a = range(tmday,fmday+1)

        fd=date(yday,tmday,tday)

        td=date(yday,fmday,fday)


    if fmday == tmday:
        if fday < tday:
            dddd=tday #to date
            tttt=fday #from date

        elif tday<fday:
            dddd=fday
            tttt=tday
        else:
            dddd =tttt=fday


    detli=[]
    toot=0


    if fd.year== td.year:

        merchant_sales=0
        for k in a: # a is the months covered in the search
            if k == a[0]: #if month is the first month
                if k == a[-1]: #use the boundaries set by the dates
                    # dddd = td.day
                    # tttt = fd.day
                    fff=0
                    fff= fff + tttt
                    while fff <= dddd :
                        fd1=date(yday,k,fff)
                        salees = tblIamerchantBank.objects.filter(
                            branch=mybranch,
                            status='Approved',
                            wallet_type='Main',
                            recdate=fd1)

                        couunt = salees.count()

                        if couunt> 0:
                            add=salees.aggregate(Sum('amount'))
                            add_cr = add['amount__sum']
                            merchant_sales=add_cr
                            toot = toot + add_cr

                            df = {'sum':merchant_sales,'details':fd1}
                            detli.append(df)

                        fff += 1

                else: #boundaries = from_date to month end

                    fff=0
                    fff= fff+ fd.day
                    dddd = (monthrange(fd.year, fd.month))[-1]

                    while fff <= dddd :
                        fd1=date(yday,k,fff) #k is month integer

                        salees = tblIamerchantBank.objects.filter(
                            branch=mybranch,
                            status='Approved',
                            wallet_type='Main',
                            recdate=fd1)

                        couunt = salees.count()
                        if couunt> 0:
                            add=salees.aggregate(Sum('amount'))
                            add_cr = add['amount__sum']
                            merchant_sales=add_cr
                            toot = toot + add_cr

                            df = {'sum':merchant_sales,'details':fd1}
                            detli.append(df)

                        fff += 1

            else:
                if k == a[-1]: #boundaries = 1st to to_date
                    dddd = td.day

                    fff=1
                    fff += 1
                    while fff <= dddd :
                        fd1=date(yday,k,fff)
                        salees = tblIamerchantBank.objects.filter(
                            branch=mybranch,
                            status='Approved',
                            wallet_type='Main',
                            recdate=fd1)

                        couunt = salees.count()
                        if couunt> 0:
                            add=salees.aggregate(Sum('amount'))
                            add_cr = add['amount__sum']
                            merchant_sales=add_cr
                            toot = toot + add_cr
                            df = {'sum':merchant_sales,'details':fd1}
                            detli.append(df)

                        fff += 1

                else: # loop thru the whole month

                    fff=0
                    fff += 1
                    dddd= (monthrange(td.year, k))[-1]

                    while fff <= dddd :
                        fd1=date(yday,k,fff)
                        salees = tblIamerchantBank.objects.filter(
                            branch=mybranch,
                            status='Approved',
                            wallet_type='Main',
                            recdate=fd1)

                        couunt = salees.count()
                        if couunt> 0:
                            add=salees.aggregate(Sum('amount'))
                            add_cr = add['amount__sum']
                            merchant_sales=add_cr
                            toot = toot + add_cr

                            df = {'sum':merchant_sales,'details':fd1}
                            detli.append(df)

                        fff += 1


        if detli !=[] :
            ddd= {'total':toot}
            detli.append(ddd)


        return detli


def get_business_yr(mybranch):

    # mybranch=tblBRANCH.objects.get(id=branch)

    yy = tblbusinessyear.objects.filter(branch=mybranch)
    if yy.count() == 1:
        yy=yy.get()


    elif yy.count() >1:

        yy = yy[yy.count() - 1 ]

    return yy



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

def contribution_count():


    mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,

        customer=customer1, #who owns the mo
        recdate__month=fdate.month, #tranaction date
        status ='CR',
        account_type = account_type,
        wallet_type='Main')

    if mont_contribution.count() == 0:
        add_count = 0
    else:
        add_count = mont_contribution.aggregate(Sum('number'))
        add_count = add_count['number__sum']

    return add_count


def repost_all_approved_deposits(bb):

    ceo=tblIaMERCHANT.objects.get(id=74)



    dy=[]
    branch=tblBRANCH.objects.get(id=bb)

    ff= tblIafieldagent.objects.filter(branch =branch,
                    status='Approved',
                    wallet_type='Main',
                    is_declined= False)


    thr= tblIathrift.objects.filter(branch=branch)

    all_sav = tblIasavings_trans.objects.filter(branch=branch,
                        wallet_type='Main',
                        product='Savings',
                        status='CR')

    del_sal= all_sav.exclude(merchant=ceo).delete()

    all_mem = tblIamerchantBank.objects.filter(branch=branch,
                        wallet_type='Main',
                        product='Savings',
                        status='CR')

    del_mem= all_mem.exclude(merchant=ceo).delete()
    approved_by='emeka6789@gmail.com'

    for cc in ff:
        customer_code=cc.customer.code
        customer=tblIaCUSTOMER.objects.get(code=customer_code)
        merchant=cc.merchant.id

        merchant=tblIaMERCHANT.objects.get(id = merchant)

        code =cc.code
        amount=cc.amount
        recdate=cc.recdate
        transdate=cc.recdate
        number =cc.number
        ttime= cc. ttime
        transac_id=cc.transac_id
        cycle= cc.cycle
        purpose=cc.purpose
        year=cc.recdate.year

        mythrift = thr.get(code=code)
        thrift = mythrift.thrift
        amount2= int(amount)- int(thrift)
        number2= int(number) - 1


        tblIamerchantBank(branch=branch,
            code=code,
            amount = amount,
            merchant=merchant,
            customer=customer,
            transdate=transdate,
            product='Savings',
            number =number,
            wallet_type='Main',
            status= 'CR',
            transac_id = transac_id,
            description='Credit',
            cycle= cycle,
            purpose=purpose,
            year=year,
            recdate=recdate,
            ttime= ttime,
            approved_by= approved_by).save()


        nm= all_sav.filter(code=code,description='Account Maintenance',status='CR')

        if nm.count() == 0:
            tblIasavings_trans(branch=branch,
                merchant=merchant,
                customer=customer,
                transdate=transdate,
                amount= thrift,
                wallet_type='Main',

                product='Savings',

                number =1,
                description='Account Maintenance',
                status='CR',
                code=code,
                cycle=cycle,
                purpose=purpose,
                year=year,
                avalability='Not Available',
                transac_id = transac_id,
                ttime= ttime,
                recdate=recdate).save()

            cc.programmm = 'X + Nj'
            cc.save()

            if amount2 > 0:
                tblIasavings_trans(branch=branch,
                    merchant=merchant,
                    customer=customer,
                    transdate=transdate,
                    amount= amount2,
                    wallet_type='Main',
                    product='Savings',
                    number =number2,
                    description='Credit',
                    status='CR',
                    code=code,
                    cycle=cycle,
                    purpose=purpose,
                    year=year,
                    avalability='Available',
                    transac_id = transac_id,
                    ttime= ttime,
                    recdate=recdate).save()

        elif nm.count() == 1:

            tblIasavings_trans(branch=branch,
                merchant=merchant,
                customer=customer,
                transdate=transdate,
                amount= amount,
                wallet_type='Main',

                product='Savings',

                number =number,
                description='Credit',
                status='CR',
                code=code,
                cycle=cycle,
                purpose=purpose,
                year=year,
                avalability='Available',
                transac_id = transac_id,
                ttime= ttime,
                recdate=recdate).save()

            cc.programmm= 'Nj'
            cc.save()



    return 'ok'




def overall_deposit(email,mybranch,ceo,customer1,amount,th,memstaff,contributed,number,product,program):

    merchant=tblIaMERCHANT.objects.get(staff=memstaff,thrift1a=1)


    card = th.purpose #since this is valid for only 1yr, it should be tied to it
    cycle=th.cycle
    year=th.year


    dddt = datetime.now()
    transdate = dddt.date()

    ttime = dddt.time()

    service_charge= th.service_charge
    thrift_code=th.code

    thrift=int(th.thrift)

    transac_id = generate_trans_pin()

    amount2 = amount - int(service_charge)
    number2 = number - 1


    if ceo ==1: #direct
        tblIamerchantBank(branch=mybranch,
            amount=amount,
            code = thrift_code,
            merchant=merchant,
            customer=customer1,
            transdate=transdate,
            product=product,
            number=number,
            wallet_type='Main',
            description='Credit',
            status='CR',
            cycle=cycle,
            transac_id=transac_id,
            purpose = card,
            year=year,
            ttime=ttime,
            recdate=transdate,
            approved_by=email).save()



        if program == "X + Nj":

            tblIasavings_trans(branch=mybranch,
                amount=service_charge,
                code = thrift_code,
                merchant=merchant,
                customer=customer1,
                transdate=transdate,
                product= product,
                number=1,
                wallet_type='Main',
                description='Account Maintenance',
                status='CR',
                purpose = card,
                ttime=ttime,
                transac_id=transac_id,
                recdate=transdate,
                cycle=cycle,
                avalability='Not Available',
                year=year).save()


            if amount2 > 0:

                tblIasavings_trans(branch=mybranch,
                    amount=amount2,
                    code = thrift_code,
                    merchant=merchant,
                    customer=customer1,
                    transdate=transdate,
                    product=product,
                    number=number2,
                    wallet_type='Main',
                    description='Credit',
                    status='CR',
                    purpose = card,
                    ttime=ttime,
                    transac_id=transac_id,
                    recdate=transdate,
                    cycle=cycle,
                    avalability='Available',
                    year=year).save()



        elif program == "Nj":

            tblIasavings_trans(branch=mybranch,
                amount=amount,
                code = thrift_code,
                merchant=merchant,
                customer=customer1,
                transdate=transdate,
                product=product,
                number=number,
                wallet_type='Main',
                description='Credit',
                status='CR',
                purpose = card,
                ttime=ttime,
                transac_id=transac_id,
                recdate=transdate,
                cycle=cycle,
                avalability='Available',
                year=year).save()


        total_save = contributed + number
        after_deposit(th,total_save)


    else :

        tblIafieldagent(branch=mybranch,
            status='Unapproved',
            merchant=merchant,
            wallet_type='Main',
            amount=amount,
            customer=customer1,
            code=thrift_code,
            recdate=transdate,
            programmm = program,
            number=number,
            ttime=ttime,
            transac_id=transac_id,
            purpose = card,
            cycle=cycle,
            is_declined= False).save()




    total_savings= int(account_balance(mybranch,customer1,th.purpose,year))


    k = {'customer':customer1,
        'amount':amount,
        'date':transdate,
        'thrift':thrift,
        'count':number,
        'total':total_savings,
        'agent':memstaff,
        'card_type':card,
        'month':th,
        'time':ttime,
        'year':transdate.year}



    return k


def after_deposit(th,total_save):

    if total_save >= 31 :
        th.complete_status=1
        th.is_closed = 1 #closed to further deposit
        th.is_contributed = 1
        th.withdraw_status = False
        th.save()



    else:
        th.complete_status= False
        th.is_closed = False #opened to further deposit
        th.is_contributed = 1
        th.withdraw_status = False
        th.save()

    return 'ok'


def account_balance(mybranch, customer,card,year):
    dff= tblIasavings_trans.objects.filter(
        branch=mybranch,
        customer=customer,
        purpose=card,year=year).exclude(description='Account Maintenance')

    CR = dff.filter(status='CR').exclude(description='Interest on Loan')


    DR= dff.filter(status='DR')



    if CR.count() > 0 :
        cr=CR.aggregate(Sum('amount'))
        cr = cr['amount__sum']
    else:
        cr =0

    if DR.count() > 0 :
        dr=DR.aggregate(Sum('amount'))
        dr = dr['amount__sum']
    else:
        dr = 0

    add = cr - dr

    return add


def reconciliation(ttt,staff,mybranch,transac_id,contributed):

    program= ttt.programmm
    number = ttt.number
    thrift_code=ttt.code
    amount=int(ttt.amount)
    cycle=ttt.cycle
    year = ttt.recdate.year

    month_index=ttt.recdate.month

    month=calendar.month_name[month_index]


    customer1= tblIaCUSTOMER.objects.get(id=ttt.customer.id)

    merchant=tblIaMERCHANT.objects.get(id=ttt.merchant.id)


    dddt = datetime.now()
    transdate= dddt.date()
    ttime = dddt.time()


    try:

        th = tblIathrift.objects.get(code=thrift_code)

        service_charge= th.service_charge
        thrift=int(th.thrift)
        card = th.purpose
        cycle=th.cycle
        year=th.year



        td = tblIamerchantBank.objects.filter(transac_id=transac_id)
        am = tblIasavings_trans.objects.filter(transac_id=transac_id)


        amount2 = amount - int(service_charge)
        number2 = int(number) - 1



        if staff.ceo == True:

            if td.count() == 0:
                tblIamerchantBank(branch=mybranch,
                    code = thrift_code,
                    merchant=merchant,
                    customer=customer1,
                    transdate=transdate,
                    product='Savings',
                    number=number,
                    wallet_type='Main',
                    description='Credit',
                    status='CR',
                    amount=amount,
                    cycle=cycle,
                    transac_id=transac_id,
                    purpose = card,
                    year=year,
                    ttime=ttime,
                    recdate=ttt.recdate,
                    approved_by=staff.email).save()


            if program == "X + Nj":

                am2 = am.filter(description='Account Maintenance')

                if am2.count() == 0:
                    tblIasavings_trans(branch=mybranch,
                        amount=service_charge,
                        code = thrift_code,
                        merchant=merchant,
                        customer=customer1,
                        transdate=transdate,
                        product='Savings',
                        number=1,
                        wallet_type='Main',
                        description='Account Maintenance',
                        status='CR',
                        purpose = card,
                        ttime=ttime,
                        transac_id=transac_id,
                        recdate=ttt.recdate,
                        cycle=cycle,
                        avalability='Not Available',
                        year=year).save()

                if amount2 > 0:
                    if am.count() <2: #the max count for transID is 2

                        tblIasavings_trans(branch=mybranch,
                            amount=amount2,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=transdate,
                            product='Savings',
                            number=number2,
                            wallet_type='Main',
                            description='Credit',
                            status='CR',
                            purpose = card,
                            ttime=ttime,
                            transac_id=transac_id,
                            recdate=ttt.recdate,
                            cycle=cycle,
                            avalability='Available',
                            year=year).save()


            elif program == "Nj":

                if am.count() == 0:
                    tblIasavings_trans(branch=mybranch,
                        amount=amount,
                        code = thrift_code,
                        merchant=merchant,
                        customer=customer1,
                        transdate=transdate,
                        product='Savings',
                        number=number,
                        wallet_type='Main',
                        description='Credit',
                        status='CR',
                        purpose = card,
                        ttime=ttime,
                        transac_id=transac_id,
                        recdate=ttt.recdate,
                        cycle=cycle,
                        avalability='Available',
                        year=year).save()


            ttt.status='Approved'
            ttt.save()


            total_save = contributed + int(number)

            after_deposit(th,total_save)


        return 'ok'
    except:

        msg = f"code is ..{thrift_code} month is ..{month} cycle is {cycle} wallet is..{customer1.customer.wallet}"
        return msg





def myrepost(staff,transaction_code,contributed):



    staffy = Userprofile.objects.get(email=staff)

    branch=staffy.branch.id
    mybranch=tblBRANCH.objects.get(id=branch)

    ttt = tblIafieldagent.objects.get(status='Unapproved',transac_id=transaction_code)

    program= ttt.programmm
    number = ttt.number
    thrift_code=ttt.code

    customer1= tblIaCUSTOMER.objects.get(id=ttt.customer.id)

    merchant=tblIaMERCHANT.objects.get(id=ttt.merchant.id)

    customer_code=customer1.code
    amount=int(ttt.amount)

    dddt = datetime.now()
    fdate= dddt.date()
    transdate=fdate
    ttime = dddt.time()


    th = tblIathrift.objects.get(code=thrift_code)
    service_charge= th.service_charge


    thrift=int(th.thrift)

    card = th.purpose
    cycle=th.cycle


    ddt=[]

    transac_id=ttt.transac_id
    td = tblIamerchantBank.objects.filter(transac_id=transac_id)
    am = tblIasavings_trans.objects.filter(transac_id=transac_id)


    amount2 = amount - int(service_charge)
    number2 = int(number) - 1



    if staffy.ceo ==1:

        if td.count() == 0:
            tblIamerchantBank(branch=mybranch,
                code = thrift_code,
                merchant=merchant,
                customer=customer1,
                transdate=fdate,
                product='Savings',
                number=number,
                wallet_type='Main',
                description='Credit',
                status='CR',
                amount=amount,
                cycle=cycle,
                transac_id=transac_id,
                purpose = card,
                year=fdate.year,
                ttime=ttime,
                recdate=ttt.recdate,
                approved_by=staff).save()


        if program == "X + Nj":

            am2 = am.filter(description='Account Maintenance')

            if am2.count() == 0:
                tblIasavings_trans(branch=mybranch,
                    amount=service_charge,
                    code = thrift_code,
                    merchant=merchant,
                    customer=customer1,
                    transdate=fdate,
                    product='Savings',
                    number=1,
                    wallet_type='Main',
                    description='Account Maintenance',
                    status='CR',
                    purpose = card,
                    ttime=ttime,
                    transac_id=transac_id,
                    recdate=ttt.recdate,
                    cycle=cycle,
                    avalability='Not Available',
                    year=fdate.year).save()

            if amount2 > 0:
                sav = am.filter(number=number2)

                if sav.count() == 0:
                    tblIasavings_trans(branch=mybranch,
                        amount=amount2,
                        code = thrift_code,
                        merchant=merchant,
                        customer=customer1,
                        transdate=fdate,
                        product='Savings',
                        number=number2,
                        wallet_type='Main',
                        description='Credit',
                        status='CR',
                        purpose = card,
                        ttime=ttime,
                        transac_id=transac_id,
                        recdate=ttt.recdate,
                        cycle=cycle,
                        avalability='Available',
                        year=fdate.year).save()


        elif program == "Nj":

            if am.count() == 0:
                tblIasavings_trans(branch=mybranch,
                    amount=amount,
                    code = thrift_code,
                    merchant=merchant,
                    customer=customer1,
                    transdate=fdate,
                    product='Savings',
                    number=number,
                    wallet_type='Main',
                    description='Credit',
                    status='CR',
                    purpose = card,
                    ttime=ttime,
                    transac_id=transac_id,
                    recdate=ttt.recdate,
                    cycle=cycle,
                    avalability='Available',
                    year=fdate.year).save()


        ttt.status='Approved'
        ttt.save()


        total_save = contributed + int(number)

        after_deposit(th,total_save)


    return 'ok'

def gen_reconciliation(branch,wallet,amount,staff,transaction_code):



    staffy = Userprofile.objects.get(email=staff)

    mybranch=tblBRANCH.objects.get(id=branch)

    memstaff = tblSTAFF.objects.get(branch=mybranch,email =staff)


    ttt = tblIbbfieldagent.objects.get(branch=mybranch, status='Unapproved',transac_id=transaction_code)

    customer= tblIaCUSTOMER.objects.get(id=ttt.customer.id)

    merchant=tblIaMERCHANT.objects.get(id=ttt.merchant.id)

    customer_code=ttt.customer.customer.code

    amount=int(amount)

    dddt = datetime.now()
    fdate= dddt.date()
    transdate=fdate
    ttime = dddt.time()



    if staffy.ceo ==1:

        tblIbbsavings_trans(
            branch= mybranch,
            amount= amount,
            merchant= merchant,
            customer=customer,
            recdate= ttt.recdate,
            transdate=dddt,
            ttime= ttime,
            status= 'CR',
            wallet_type='Main',
            transac_id = ttt.transac_id,
            description= 'Credit',
            avalability='Available',
            year=ttt.year).save()


        ttt.status='Approved'
        ttt.save()



    return 'ok'


def after_withdrawal(customer_code, thrift_code,varuser,total_withdrawn,cr,month,cycle):

    staff = Userprofile.objects.get(email=varuser,status=True, thrift1a=1)

    branch=staff.branch.id
    mybranch=tblBRANCH.objects.get(id=branch)

    customer1=tblIaCUSTOMER.objects.get(code =customer_code,status=True,branch=mybranch)

    th = tblIathrift.objects.get(branch=mybranch,customer=customer1,code=thrift_code,month=month,cycle=cycle)


    if th.is_overdraft == False :

        if cr == 31 :
            if cr == total_withdrawn:
                th.is_overdraft= False
                th.is_empty=True
                th.withdraw_status=True
                th.is_contributed= False
                th.save()

            elif total_withdrawn < cr :
                th.is_overdraft= False
                th.is_empty= False
                th.withdraw_status= False
                th.is_contributed=True
                th.save()

        elif cr < 31:

            if cr == total_withdrawn:
                th.is_overdraft= False
                th.is_empty=True
                th.complete_status=True
                th.withdraw_status= True
                th.is_contributed= False
                th.save()

            elif total_withdrawn < cr :
                th.is_overdraft= False
                th.is_empty= False
                th.complete_status=True
                th.withdraw_status= False
                th.is_contributed=True
                th.save()


    return 'ok'


def refresh(transac_id,staff):

    tt = tblIamerchantBank.objects.get(transac_id=transac_id)

    c1 = tt.code
    tf = tblIathrift.objects.get(code=c1)

    service_charge=tf.service_charge
    amount= tt.amount
    number= int(amount) / int(service_charge)

    number2 = number -1

    customer=tblCUSTOMER.objects.get(wallet=tf.customer.customer.wallet)
    customer_code=customer.code


    thrift_code=tf.code

    alsaves = tblIasavings_trans.objects.filter(code=c1)

    add_count = alsaves.aggregate(Sum('number'))
    add_count = int(add_count['number__sum'])

    total_save=add_count




    tv = tblIasavings_trans.objects.filter(transac_id=transac_id)
    if tv.count() == 1:
        tv1 = tv.get()
        if tv1.description=='Account Maintenance':
            tv1.number=1
            tv1.save()

            tt.number=1
            tt.save()


        elif tv1.description == 'Credit':
            tv1.number=number
            tv1.save()

            tt.number = number
            tt.save()

    elif tv.count() == 2:
        tv1 = tv.get(description='Account Maintenance')
        tv1.number=1
        tv1.save()

        tv2 = tv.get(description='Credit')
        tv2.number=int(number2)
        tv2.save()


    after_deposit(tf,total_save)



    return 'ok'





def repay_loan(branch,wallet,amount,thrift_code,staff,contributed,number,product):

    staffy = Userprofile.objects.get(email=staff)

    mybranch=tblBRANCH.objects.get(id=branch)

    memstaff = tblSTAFF.objects.get(branch=mybranch,email =staff)

    merchant=tblIaMERCHANT.objects.get(staff=memstaff,thrift1a=1)
    customer=tblCUSTOMER.objects.get(branch = mybranch, wallet=wallet,status=True)
    customer1=tblIaCUSTOMER.objects.get(customer=customer,status=True)
    customer_code=customer.code


    dddt = datetime.now()
    fdate= dddt.date()
    transdate=fdate
    ttime = dddt.time()


    th = tblIathrift.objects.get(branch=mybranch,code=thrift_code)
    service_charge= th.service_charge


    thrift=int(th.thrift)

    card = th.purpose
    cycle=th.cycle


    ddt=[]

    code=generate_trans_pin()

    amount2 = amount - int(service_charge)



    r= 0

    if staffy.ceo ==1:

        if tblIamerchantBank.objects.filter(branch=mybranch,
            code =thrift_code,
            merchant=merchant,
            customer=customer1,
            transdate=fdate,
            product=product,
            number=number,
            wallet_type='Main',
            description='Loan Repayment',
            status='CR').count() < 1:


            tblIamerchantBank(branch=mybranch,
                amount=amount,
                code = thrift_code,
                merchant=merchant,
                customer=customer1,
                transdate=fdate,
                product=product,
                number=number,
                wallet_type='Main',
                description='Loan Repayment',
                status='CR',

                cycle=cycle,
                transac_id=code,
                purpose = card,
                year=fdate.year,
                ttime=ttime,
                recdate=transdate,
                approved_by=staff).save()

            r=1

            sc = tblIasavings_trans.objects.filter(branch=mybranch,
                    amount=service_charge,
                    code = thrift_code,
                    customer=customer1,
                    wallet_type='Main',
                    description='Account Maintenance',
                    status='CR')


            if sc.count() == 0:
                r=1
                mj=9
                tblIasavings_trans(branch=mybranch,
                    amount=service_charge,
                    code = thrift_code,
                    merchant=merchant,
                    customer=customer1,
                    transdate=fdate,
                    product= 'Savings',
                    number=0,
                    wallet_type='Main',
                    description='Account Maintenance',
                    status='CR',
                    purpose = card,
                    ttime=ttime,
                    transac_id=code,
                    recdate=transdate,
                    cycle=cycle,
                    avalability='Not Available',
                    year=fdate.year).save()


                if amount2 > 0:

                    if tblIasavings_trans.objects.filter(branch=mybranch,
                            amount=amount2,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=fdate,
                            product=product,
                            number=number,
                            wallet_type='Main',
                            description='Loan Repayment',
                            status='CR').count() <1 :

                        tblIasavings_trans(branch=mybranch,
                            amount=amount2,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=fdate,
                            product=product,
                            number=number,
                            wallet_type='Main',
                            description='Loan Repayment',
                            status='CR',
                            purpose = card,
                            ttime=ttime,
                            transac_id=code,
                            recdate=transdate,
                            cycle=cycle,
                            avalability='Not Available',
                            year=fdate.year).save()

                        mj = 10


            elif sc.count() ==1:
                mj =8
                if tblIasavings_trans.objects.filter(branch=mybranch,
                        amount=amount,
                        code = thrift_code,
                        merchant=merchant,
                        customer=customer1,
                        transdate=fdate,
                        product=product,
                        number=number,
                        wallet_type='Main',
                        description='Loan repayment',
                        status='CR').count() <1:

                    tblIasavings_trans(branch=mybranch,
                        amount=amount,
                        code = thrift_code,
                        merchant=merchant,
                        customer=customer1,
                        transdate=fdate,
                        product=product,
                        number=number,
                        wallet_type='Main',
                        description='Loan Repayment',
                        status='CR',
                        purpose = card,
                        ttime=ttime,
                        transac_id=code,
                        recdate=transdate,
                        cycle=cycle,
                        avalability='Not Available',
                        year=fdate.year).save()

                    r=1

    elif staffy.thrift_officer==1:

        if contributed == 0:

            p = "X + Nj"

            l,kp = divmod(amount2,thrift)

            if kp == 0:
                if tblIafieldagent.objects.filter(branch=mybranch,
                    merchant=merchant,
                    wallet_type='Main',
                    amount=amount,
                    customer=customer1,
                    code=th.code,
                    recdate=transdate).count() <1 :

                    tblIafieldagent(branch=mybranch,
                        status='Unapproved',
                        merchant=merchant,
                        wallet_type='Main',
                        amount=amount,
                        customer=customer1,
                        code=th.code,
                        recdate=transdate,

                        number=number,
                        ttime=ttime,
                        transac_id=code,
                        purpose = card,
                        cycle=cycle,
                        is_declined= False).save()

                    r=1


        else:

            p="Nj"

            if tblIafieldagent.objects.filter(branch=mybranch,
                merchant=merchant,
                wallet_type='Main',
                number=number,
                customer=customer1,
                code=thrift_code,
                recdate=transdate).count() <1 :

                tblIafieldagent(branch=mybranch,
                    status='Unapproved',
                    merchant=merchant,
                    wallet_type='Main',
                    amount=amount,
                    customer=customer1,
                    code=thrift_code,
                    recdate=transdate,

                    number=number,
                    ttime=ttime,
                    transac_id=code,
                    cycle=cycle,
                    purpose = card,
                    is_declined= False).save()

                r=1


    if r == 1:
        total_save = contributed  + number

        after_loan_repay(customer_code,thrift_code,staff,total_save)

        my_balance = Loan_repaid_count(wallet,staff,thrift_code)

        bal = (my_balance['loan_repaid'] + my_balance['savings_cr'] - 31 )* thrift


        k = {'customer':customer1,
            'amount':amount,
            'date':fdate,
            'user':staff,
            'thrift':thrift,
            'count':number,
            'total':bal,
            'agent':memstaff,
            'card_type':card,
            'month':th,
            'time':ttime,
            'year':fdate.year}



        return k
    else:
        return 1



def Loan_repaid_count(wallet,user,code):


    details=tblCUSTOMER.objects.get(wallet=wallet,status=True)
    branch=details.branch.id
    mybranch= tblBRANCH.objects.get(id =branch)
    details=tblIaCUSTOMER.objects.get( customer=details,status=True)




    mont_every = tblIasavings_trans.objects.filter(branch=mybranch,
        customer=details,
        code = code,
        wallet_type='Main')


    mont_contribution = mont_every.filter(product='Savings')



    CR= mont_contribution.filter( status= 'CR')

    if CR.count() == 0:
        cr = 0
    else:
        cr  = CR.aggregate(Sum('number'))
        cr  = int(cr['number__sum'])



    DR = mont_contribution.filter(status='DR')


    if DR.count() == 0:
        dr = 0
    else:
        dr  = DR.aggregate(Sum('number'))
        dr  = int(dr['number__sum'])





    mont_Loan = mont_every.filter(product='Loan')




    CRL= mont_Loan.filter( status= 'CR')

    if CRL.count() == 0:
        crl = 0
    else:
        crl  = CRL.aggregate(Sum('number'))
        crl  = int(crl['number__sum'])


    DRL = mont_Loan.filter(status='DR')


    if DRL.count() == 0:
        drl = 0
    else:
        drl  = DRL.aggregate(Sum('number'))
        drl  = int(drl['number__sum'])



    res = {'savings_cr':cr,'savings_dr':dr,
        'loan':drl,'loan_repaid':crl}

    return res



def Loan_balance_amount(wallet,user,code):


    details=tblCUSTOMER.objects.get(wallet=wallet,status=True)
    branch=details.branch.id
    mybranch= tblBRANCH.objects.get(id =branch)
    details=tblIaCUSTOMER.objects.get( customer=details,status=True)


    mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,
        customer=details,
        code = code,
        wallet_type='Main').exclude(description='Account Maintenance')

    mont_contribution =mont_contribution.exclude(description='Interest on Loan')



    mont_contribution_credit= mont_contribution.filter( status= 'CR')

    if mont_contribution_credit.count() == 0:
        cr = 0
    else:
        cr  = mont_contribution_credit.aggregate(Sum('amount'))
        cr  = int(cr['amount__sum'])



    mont_contribution_debit = mont_contribution.filter(description='Debit')


    if mont_contribution_debit.count() == 0:
        dr = 0
    else:
        dr  = mont_contribution_debit.aggregate(Sum('amount'))
        dr  = int(dr['amount__sum'])



    mont_contribution_all_loan= mont_contribution.filter( description= 'Loan')

    if mont_contribution_all_loan.count() == 0:
        tt = 0
    else:
        tt  = mont_contribution_all_loan.aggregate(Sum('amount'))
        tt  = int(tt['amount__sum'])



    bal =  (cr - dr) - tt

    return bal


def after_loan_repay(customer_code, thrift_code,varuser,total_save):

    staff = Userprofile.objects.get(email=varuser,status=True, thrift1a=1)

    branch=staff.branch.id


    mybranch=tblBRANCH.objects.get(id=branch)


    customer1=tblIaCUSTOMER.objects.get(code =customer_code,status=True,branch=mybranch)


    th = tblIathrift.objects.get(branch=mybranch,customer=customer1,code=thrift_code)

    dddy = datetime.today()
    fdate = dddy.date()

    if total_save == 31 :
        th.is_contributed= False
        th.complete_status=1
        th.is_closed = 1 #closed to further deposit
        th.withdraw_status = 1
        th.is_empty=1
        th.is_overdraft=1
        th.is_done = 1
        th.overdraft_date_end = fdate
        th.save()

    else:
        th.is_contributed= False
        th.complete_status= False
        th.is_closed = False #closed to further deposit
        th.withdraw_status = 1
        th.is_empty=1
        th.is_overdraft=1
        th.is_done = False
        th.save()

    return 'ok'



"""
'your loan is repaid for the month of %s, %d' % (month, year)

in the future, msg should be more detailed, giving the present month and year, and
the number of months left or when the loan will be fully repaid

"%s is %d years old." % (name, age)

moreso, we can send html emails, where u can follow a link and view the repayment history a
among other details. This is called MIME emails.........woooow
"""

