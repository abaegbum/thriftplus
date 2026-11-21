
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from datetime import date,timedelta, datetime
from django.core.serializers.json import json

from django.views.decorators.csrf import csrf_exempt
from num2words import num2words
from django.db.models import Max,Sum, Count, F, IntegerField


from django.db.models.functions import RowNumber, Cast
from django.db.models.expressions import Window
import math


from Ia.utils import *
from Ia.models import *
from customer.models import *
from thriftplus.utils import  *
from thriftplus.forms import  *

def index(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=Userprofile.objects.filter(email=email,password=password,status=1)
        if user.count() ==1:
            user=user.get()
            request.session['userid'] = user.email
            varuser = request.session['userid']
            return  HttpResponseRedirect('/dashboard/')

        else:

            cc = tblCUSTOMER.objects.filter(wallet=email,status=1,phone=password)
            if cc.count==1:
                cc=cc.get()
                request.session['userid'] = email
                varuser = request.session['userid']
                return  HttpResponseRedirect('/home/')


        msg='Invalid login details'
        return render(request,'login.html',{'varerr':msg})


    else:
        # new_fresh()
        return render(request,'index.html')




def dashboard(request):
    if 'userid' in request.session:
        varuser = request.session['userid']
        staff = Userprofile.objects.get(email=varuser,status=1)
        branch_code=staff.branch.code
        mybranch=tblBRANCH.objects.get(code= branch_code)


        if staff.partner==0:
            app = tblapp.objects.get(branch=mybranch)

            if app.thrift1a==True:
                history= checkhighestsub(mybranch)

            elif app.thrift3b==True:
                app='Coop'




        mydate=date.today()  #######SWITCHING PROGRAM   FOR SUBSCRIPTION ****
        gh = tblswitchpro.objects.filter(datte=mydate,status=1)

        if gh.count() ==0:

            yesterdday = mydate - timedelta(days=1)
            cv =tblsubscription.objects.filter(status='Running')
            for k in cv:
                if k.end <= yesterdday:
                    k.status='Expired'
                    k.save()

            v2 =tblsubscription.objects.filter(status='Queing' ).order_by('start')
            for k in v2:
                if k.start <= mydate:
                    k.status='Running'
                    k.save()

            gh = tblswitchpro.objects.all().delete()
            tblswitchpro(datte=mydate, status=1).save()



        hp = tblrollover.objects.filter(branch=mybranch,year=mydate.year) #######SWITCHING PROGRAM  FOR ROLLOVOER ************************
        if hp.count() == 0:
            tblrollover.objects.filter(branch=mybranch).delete()
            tblbusinessyear(branch=mybranch,year=mydate.year).save()
            tblrollover(branch=mybranch,year=mydate.year,status=1).save()


        if staff.thrift3b ==1: #IIIB coporative
            return render(request,'IIIB/dashboardIIIb.html',{'user':varuser,'company':mybranch,
                'pincode':staff})

        elif staff.thrift1a ==1: #IA all other services

            if app.esusu1a==True: #checking if you named your esusu
                product= tblmyproducts.objects.get(product='Esusu')
                fp = tblproductsname.objects.filter(branch=mybranch,product=product)

                if fp.count()==0:
                    return render(request,'app.html',{'user':varuser,'company':mybranch})
                    # return render(request,'pro.html',{'msg':product.code})


            if app.savings1a==True:
                product= tblmyproducts.objects.get(product='Savings')
                fp = tblproductsname.objects.filter(branch=mybranch,product=product)
                if fp.count()==0:
                    return render(request,'app.html',{'user':varuser,'company':mybranch})

            return render(request,'thriftIa_dashboard.html',{'user':varuser,'company':mybranch,
                'pincode':staff,
                'history':history})

        elif staff.partner == 1: #partners
            return render(request,'partner_dashboard.html',{'company':mybranch, 'user':varuser})


        else: #no assigned potfolio
            return render(request,'404.html',{'company':mybranch, 'user':varuser})


    else:
        return HttpResponseRedirect('/login/user/')




def login(request):

    return render(request,'login.html')




def passreset(request):
    if request.method=='POST':
        email=request.POST['email']

        try:
            ppp = Userprofile.objects.get(email=email)

        except:
            msg= 'Invalid Email'
            return render(request,'forgot.html',{'varerr':msg})


        password= ppp.password
        branch=ppp.branch.id
        branch=tblBRANCH.objects.get(id=branch)
        company=branch.company.name

        passwordlink(email,password,company)

        msg="Check your email's inbox and SPAM folder for details"


            ##send email


        return render(request,'forgot.html',{'varerr':msg})


    else:
        return render(request,'forgot.html')


def logoutuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/user/')



def switchuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/user/')

def changepass(request):
    if 'userid' in request.session:
        varuser = request.session['userid']

        try:
            staff = Userprofile.objects.get(email=varuser,status=1)
        except:
            return HttpResponseRedirect('/login/user/')

        staffdet=staff.staffrec.id
        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompay=tblCOMPANY.objects.get(id=comp_code)
        mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

        if request.method=='POST':
            oldpass= request.POST['oldpass']
            newpass1=request.POST['newpass1']
            newpass2=request.POST['newpass2']

            if oldpass== staff.password :
                if newpass2 == newpass1:
                    msg= 'password change successfull'
                    rr=Userprofile.objects.filter(email=varuser,status=1).update(password=newpass1)
                    # switchuser()
                    return render(request,'success.html',{'user':varuser,'company':mybranch,
                        'menu':staff,'msg':msg})
                else:
                    msg = 'the passwords do not match'
            else:
                msg='your old pass is not correct'


        else :
            msg=''



        return render(request,'changepass.html',{'user':varuser,'company':mybranch,
                'menu':staff,'msg':msg})

    else:
        return HttpResponseRedirect('/login/user/')


def subscription(request):
    if 'userid' in request.session:
        varuser = request.session['userid']
        staff = Userprofile.objects.get(email=varuser,status=1)
        branch_code=staff.branch.code
        mybranch=tblBRANCH.objects.get(code= branch_code)


        if staff.ceo==0:
            return render(request,'404.html',{'company':mybranch, 'user':varuser})


        yyapp = tblapp.objects.get(branch=mybranch)
        kpq=[]

        if yyapp.thrift1a==True:
            if yyapp.esusu1a==True:
                app ='Esusu'
                history= checksub(mybranch,app)
                kpq.append(history)

            if yyapp.savings1a==True:
                app ='General Savings'
                history= checksub(mybranch,app)
                kpq.append(history)


            if yyapp.ecomerce==True:

                app ='Ecommerce'
                history= checksub(mybranch,app)
                kpq.append(history)



            if yyapp.investment==True:

                app ='Investment'
                history= checksub(mybranch,app)
                kpq.append(history)


        elif yyapp.thrift3b==True:
            yyapp='Coop'
            history= checksub(mybranch,app)
            kpq.append(history)



        return render(request,'subscription_detail.html',{'company':mybranch,
            'user':varuser,
            'comp':mybranch,
            'history':kpq})



    else:
        return HttpResponseRedirect('/login/user/')


@csrf_exempt
def renews(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            varuser=request.session['userid']
            post = request.POST.copy()
            vid = post['userid']



            g = tblsubscription.objects.filter(receipt=vid)
            if g.count() ==1:
                g=g.get()
                bb = g.branch.code
                mybranch=tblBRANCH.objects.get(code=bb)
                package= g.package.package
                package=tblthriftpackages.objects.get(package=package)
                sub = tblsubpending.objects.filter(branch=mybranch,package=package, status='Queing',app=g.app)

                if sub.count() == 1:
                    sub2 = sub.get()
                    return render(request,'renews_pending.html',{'g':g,'sub':sub2})

                elif sub.count() ==0:
                    if g.package.package=='Onboarding':

                        ksub = tblsubpending.objects.filter(branch=mybranch, status='Queing',app=g.app)

                        if ksub.count() ==1:
                            sub2 = ksub.get()
                            return render(request,'renews_pending.html',{'g':g,'sub':sub2})

                        ppp=tblthriftpackages.objects.filter(status=1).exclude(package='Onboarding').order_by("weight")
                        return render(request,'renews_upgrade.html',{'branch':bb, 'g':g,'user':varuser,'package':ppp})
                    else:
                        return render(request,'renews.html',{'g':g,'user':varuser})
                else:
                    d=94
            else:
                HttpResponseRedirect('/subscription/')


    else:
        return HttpResponseRedirect('/login/user/')


@csrf_exempt
def renewsub(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']

                service,package,duration=acccode.split(':')

                staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
                bb =staff.branch.code
                branch=tblBRANCH.objects.get(code=bb)
                currency=branch.currency_code


                if package == '1':
                    msg = 'Select appropriate package'
                    return render(request,'selectloan.html',{'msg':msg})



                if duration == '':
                    msg = 'Select appropriate duration'
                    return render(request,'selectloan.html',{'msg':msg})


                pack=tblthriftpackages.objects.get(id=package)


                unit_cost=pack.cost

                ttl=0
                deduction=0
                discounted=0



                ttl=float(unit_cost) * int(duration)


                ttl = round(ttl, 2)




                dis = tblplatformdiscount.objects.filter(package=pack,duration=duration,status=1)

                if dis.count() ==1:
                    dis =dis.get()
                    discount = dis.discount
                else:
                    discount=0




                deduction  = int(discount) * ttl / 100

                deduction = round(deduction, 2)



                discounted = (100 - int(discount)) *  ttl / 100

                discounted = round(discounted, 2)





                return render(request,'renews_drop.html',{'currency':currency,'pack':pack,
                    'total':ttl,
                    'unit':unit_cost,
                    'discount':deduction,
                    'duration':duration,
                    'service':service,
                    'amount':discounted})



            else:
                gdata = ""
                return render(request,'index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render(request,'getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')




def extension(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        staff=Userprofile.objects.get(email=varuser, status=1)
        staffdet=staff.staffrec.id
        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompay=tblCOMPANY.objects.get(id=comp_code)
        mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        # partnerfff=tblPARTNER.objects.get(email=varuser)


        if staff.ceo==0:
            return render(request,'404.html',{'company':mybranch, 'user':varuser})

        sub_history = tblsubscription.objects.filter(branch=mybranch,status='Active')


        return render(request,'subscription_extension.html',{'company':mybranch,
            'user':varuser,
            'comp':mybranch,
            'history':sub_history})

    else:
        return HttpResponseRedirect('/login/user/')


@csrf_exempt
def currentsubscription(request):
    if 'userid' in request.session:

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                kk=[]
                sdic={}

                app,category=acccode.split(':')

                staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

                branch_code=staff.branch.code
                bb=tblBRANCH.objects.get(code=branch_code)
                if app == '--':
                    d='i am me'

                else:
                    history= checksub(bb,app)
                    d = history['package'][0]

                # for j in d:
                #     # j = j.cycle
                #     s = {j:j}
                #     sdic.update(s)


                # klist = sdic.values()
                # for p in klist:
                #     kk.append(p)


                return HttpResponse(json.dumps(d), content_type='application/json')
            else:
                gdata = ""
                return render(request,'index.html',{'gdata':gdata})
        else:

            gdata = ""
            return render(request,'getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')





@csrf_exempt
def subty(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            post = request.POST.copy()
            acccode = post['userid']
            subtype,user=acccode.split(':')

            staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


            staffdet=staff.staffrec.id
            branch=staff.branch.id

            mycompany=staff.branch.company
            company=mycompany.name
            comp_code=mycompany.id
            ourcompany=tblCOMPANY.objects.get(id=comp_code)

            mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
            currency=mybranch.currency_code

            if subtype=='-----':
                msg = 'Select your preferred category'
                return render(request,'selectloan.html',{'msg':msg})

            else:
                sub = tblsubpending.objects.filter(branch=mybranch,status='Queing')

                if sub.count() > 0:
                    # sub1 = sub.get()
                    # code = sub1.receipt
                    return render(request,'subscription_que.html',{'sub':sub,'currency':currency})

                sub2 =tblsubscription.objects.filter(branch=mybranch,status='Queing')

                if sub2.count()>0:
                    # sub3=sub2.get()
                    return render(request,'subscription_pen.html',{'sub':sub2,'currency':currency})


                elif subtype=='standard':
                    aaa = tblapp.objects.get(branch=mybranch)
                    ads=[]

                    if aaa.thrift1a== True:
                        if aaa.esusu1a== True:
                            ads.append('Esusu')

                        if aaa.savings1a ==True:# or aaa.loans1acash== True or aaa.loans1aitems== True:
                            ads.append('General Savings')

                        if aaa.investment==True or aaa.fixeddepo1a==True or aaa.targetsave1a==True:
                            ads.append('Investment')
                        if aaa.ecomerce==True:
                            ads.append('e-commerce')

                    else:

                        if aaa.thrift3b==True:
                            ads.append('Coperative')


                    t = tblthriftpackages.objects.filter(status=1).exclude(appendage='Trial').order_by("weight")
                    return render(request,'subscription_extensionstandard.html',{'service':ads,'data':t,'category':subtype})

                elif subtype=='custom':
                    return render(request,'subscription_extensioncustom.html',{'user':user})


    else:
        return HttpResponseRedirect('/login/user/')

@csrf_exempt
def sendp(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            post = request.POST.copy()
            acccode = post['userid']
            package,duration,user=acccode.split(':')

            if package== '--' :
                msg = 'Select preferred  package'
                return render(request,'selectloan.html',{'msg':msg})

            if duration== '--' :
                msg = 'Select duration'
                return render(request,'selectloan.html',{'msg':msg})

            else :

                staff = Userprofile.objects.get(email=user,status=1)
                staffid = staff.staffrec.id
                mybranch=staff.branch.id
                mybranch=tblBRANCH.objects.get(id=mybranch,status=1)
                if staff.ceo ==0:
                    msg = 'user not approved'
                    return render(request,'selectloan.html',{'msg':msg})
                else:
                    return render(request,'subscription_extensionsend.html',{'user':user})

        else:
            return HttpResponseRedirect('/login/user/')
    else:
        return HttpResponseRedirect('/login/user/')


@csrf_exempt
def sendit(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            post = request.POST.copy()
            acccode = post['userid']
            user,package,duration=acccode.split(":")

            staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


            staffdet=staff.staffrec.id
            branch=staff.branch.id
            mybranch= tblBRANCH.objects.get(id=branch)
            currency = mybranch.currency_code

            mycompany=staff.branch.company
            company=mycompany.name
            comp_code=mycompany.id
            ourcompany=tblCOMPANY.objects.get(id=comp_code)

            if staff.ceo==0:
                msg ='user not approved'
                return render(request,'selectloan.html',{'msg':msg})
            else:
                kb = tblthriftpackages.objects.get(id =package)
                price = kb.cost
                amount= round(float(price) * float(duration),1)


                return render(request,'subscription_extensionpackprice.html',{'pack':kb,
                    'duration':duration,
                    'price':price,
                    'currency':currency,
                    'amount':amount})



        else:
            return HttpResponseRedirect('/login/user/')
    else:
        return HttpResponseRedirect('/login/user/')



def edit_sub(request):
    if 'userid' in request.session:
        varuser=request.session['userid']

        staff=Userprofile.objects.get(email=varuser, status=1)
        staffdet=staff.staffrec.id
        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompay=tblCOMPANY.objects.get(id=comp_code)
        mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


        currency=mybranch.currency_code


        if staff.ceo==0:
            return render(request,'404.html',{'company':mybranch, 'user':varuser})


        if request.method=='POST':
            package= request.POST['package']
            duration=request.POST['duration']
            amount=request.POST['amount']
            app=request.POST['app']
            pin =  generate_trans_pin()


            package=tblthriftpackages.objects.get(id=package)

            df = tblsubpending.objects.filter(status='Queing',branch=mybranch,package=package,app = app)

            if df.count() ==0:

                tblsubpending(status='Queing',branch=mybranch,receipt=pin,amount=amount,
                    package=package,duration=duration,app = app).save()


            sub = tblsubpending.objects.filter(branch=mybranch,status='Queing',app = app,package=package)

            if sub.count() ==1:
                sub1 = sub.get()

                return render(request,'subscription_extensionsus.html',{'company':mybranch,
                    'user':varuser,'k':sub1,'currency':currency,'receipt':pin,
                    'comp':mybranch})
            else:
                return HttpResponseRedirect('/subscription/')

        else:
            return HttpResponseRedirect('/subscription/')

    else:
        return HttpResponseRedirect('/login/user/')



def delsubappl(request):
    if 'userid' in request.session:
        varuser=request.session['userid']

        rct = request.POST['receipt']

        try:
            sub = tblsubpending.objects.filter(receipt=rct).delete()
        except:
            p=0

        return HttpResponseRedirect('/extension/')


    else:
        return HttpResponseRedirect('/login/user/')



def howitworks_return_deposits_greater_than_31(request):#

    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id

        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        branch_code=staff.branch.code

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


        year = 2026
        status_cr='CR'
        status_dr='DR'
        savings = tblIasavings_trans.objects.filter(branch=mybranch,year = year,status=status_cr)

        thrifts= tblIathrift.objects.filter(branch=mybranch,year=year)

        tc = thrifts.values_list('code',flat=True).distinct()


        rv =  (savings.filter(code__in=tc)
                # .values('code','customer__customer__wallet','cycle','customer__customer__surname','customer__customer__firstname','recdate__month')
                .values('code','customer__customer__wallet','recdate__month')
                .annotate(number_count=Cast(Sum('number'), IntegerField()))
                .filter(number_count__gt=30)
                .order_by('recdate__month','number_count'))






        return render(request,'howitworks.html',{'company':mybranch,
                    'user':varuser,"staff":staff,'msg':rv})

    else:
        return HttpResponseRedirect('/login/user/')

def howitworks_after_deposit(request):#

    if 'userid' in request.session:
        varuser=request.session['userid']
        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id

        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        branch_code=staff.branch.code

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



        year = 2026
        status='CR'
        savings = tblIasavings_trans.objects.filter(branch=mybranch,year = year,status=status)

        thrifts= tblIathrift.objects.filter(branch=mybranch,year=year)

        tc = thrifts.values_list('code',flat=True).distinct()


        thrift_map = {th.code: th for th in thrifts}

        # Aggregate and call function inline
        rv = []

        # tc=[792371158675000]
        sav =  (savings.filter(code__in=tc)
                .values('code','customer__customer__wallet','cycle','customer__customer__surname','customer__customer__firstname')
                .annotate(number_count=Cast(Sum('number'), IntegerField()))
                .filter(number_count__gt=30)
                .order_by('code','number_count'))




        # return render(request,'Ia/selectloan.html',{'msg':sav.count()})


        # for row in sav.iterator(chunk_size=50):

        #     code = row['code']
        #     count = row['number_count']
        #     th = thrift_map.get(code)

        #     if th:
        #         after_deposit(th, count)   # function call happens here
        #         rv.append({'thrift': th, 'number_count': count})


        return render(request,'howitworks.html',{'company':mybranch,
                    'user':varuser,"staff":staff,'msg':sav})


    else:
        return HttpResponseRedirect('/login/user/')


def howitworks_after_withdrawal(request):#

    if 'userid' in request.session:
        varuser=request.session['userid']
        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id

        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        branch_code=staff.branch.code

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



        year = 2026
        status='DR'
        savings = tblIasavings_trans.objects.filter(branch=mybranch,year = year,status=status)

        thrifts= tblIathrift.objects.filter(branch=mybranch,year=year)

        tc = thrifts.values_list('code',flat=True).distinct()


        thrift_map = {th.code: th for th in thrifts}

        # Aggregate and call function inline
        rv = []


        sav =  (savings.filter(code__in=tc)
                .values('code','customer__customer__wallet','cycle','customer__customer__surname','customer__customer__firstname','recdate__month')
                .annotate(number_count=Cast(Sum('number'), IntegerField()))
                .filter(number_count__gt=30)
                .order_by('recdate__month','number_count'))



        # for row in sav.iterator(chunk_size=50):

        #     code = row['code']
        #     count = row['number_count']
        #     th = thrift_map.get(code)

        #     if th:
        #         after_withdrawal(th, count)   # function call happens here
        #         rv.append({'thrift': th, 'number_count': count})


        return render(request,'howitworks.html',{'company':mybranch,
                    'user':varuser,"staff":staff,'msg':rv})


    else:
        return HttpResponseRedirect('/login/user/')

def howitworks(request):#_indi

    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id

        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        branch_code=staff.branch.code

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



        # wallet=6651284657
        # month='September'
        # cycle='cycle 11'

        # customer=tblCUSTOMER.objects.get(wallet=wallet)
        # customer=tblIaCUSTOMER.objects.get(customer=customer)
        # thrift = tblIathrift.objects.get(customer=customer,month=month,cycle=cycle)

        # thrift.is_contributed= True
        # thrift.withdraw_status = False
        # thrift.is_empty= False
        # thrift.save()




        return render(request,'howitworks.html',{'company':mybranch,
                    'user':varuser,"staff":staff})

    else:
        return HttpResponseRedirect('/login/user/')

def howitworks_rebuild_thrifts_from_Iafield(request):#

    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id

        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
        branch_code=staff.branch.code

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

        customer= tblIaCUSTOMER.objects.filter(branch=mybranch)

        year = 2026


        vc = tblIafieldagent.objects.filter(branch=mybranch,recdate__year= year)
        ttp = tblIathrift.objects.filter(branch=mybranch, year=year)



        mn = vc.values_list('code', flat=True).distinct()
        fp = ttp.values_list('code', flat=True).distinct()
        # Missing codes handled by the database
        missing_codes = mn.exclude(code__in=fp)


        d={'field':len(mn),'thrift':len(fp), 'missing':len(missing_codes)}
        return render(request,'howitworks.html',{'company':mybranch,
                    'user':varuser,"staff":staff,'msg':missing_codes,'d':d})

        # Stream missing codes in chunks of 10
        for code in missing_codes.iterator(chunk_size=50):
            # Instead of hitting DB again, just pull the first matching record from bn
            ttt = next((row for row in vc if row.code == code), None)
            if not ttt:
                continue

            number = ttt.number
            thrift_code = ttt.code
            amount = int(ttt.amount)
            cycle = ttt.cycle
            year_val = ttt.recdate.year
            monthindex_val = ttt.recdate.month
            month_name = calendar.month_name[monthindex_val]  # <-- this is the actual month name
            card = ttt.purpose

            service_charge = int(amount / int(number))
            customer1 = ttt.customer  # already prefetched

            tblIathrift(
                code=thrift_code,
                customer=customer1,
                month=month_name,          # <-- use month_name instead of undefined 'month'
                monthindex=monthindex_val, # <-- use monthindex_val instead of undefined 'monthindex'
                thrift=service_charge,
                service_charge=service_charge,
                year=year_val,
                cycle=cycle,
                purpose=card,
                branch=mybranch,
                is_contributed=True
            ).save()



        return render(request,'howitworks.html',{'company':mybranch,
                    'user':varuser,"staff":staff,'msg':mn})

    else:
        return HttpResponseRedirect('/login/user/')


# Wrapper to make a view handle both normal and api request
def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), content_type="application/json")

    return wrap

def namesearch(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                post = request.POST.copy()
                acccode = post['userid']
                if acccode=='':
                  return render(request,"namesearch.html")

                else:
                    data = tblCUSTOMER.objects.filter(branch=3, status=1, surname__contains=acccode)
                    return render(request,'serch.html',{'data':data})
            else:
                gdata = ""
                return render(request,'index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render(request,'serch.html',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/user/')



def cusdetailS(request):
    if request.is_ajax():
        if request.method == 'POST':
            post = request.POST.copy()
            acccode = post['userid']
            # state,trandate=acccode.split(':')
            customer=tblCUSTOMER.objects.get(wallet=acccode)

            return render(request,'walletdetails.html',{'details':customer})
        else:
            return HttpResponseRedirect('/login/user/')
    else:
        return HttpResponseRedirect('/login/user/')





#### **** LEDGER ENTRIES ****************


def integrity(request): #tv


    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id

        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


        allmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,status=1)

        realdet = tblapp.objects.get(branch=mybranch)

        yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()


        tdate= date.today()
        myy = []



        gb = tblproductsname.objects.filter(branch=mybranch)


        if realdet.esusu1a is True:
            hh= tblmyproducts.objects.get(product='Esusu')
            gb2=gb.get(product=hh)
            myy.append(gb2)



        if realdet.savings1a is True:
            hh= tblmyproducts.objects.get(product='Savings')
            gb2=gb.get(product=hh)
            myy.append(gb2.your_product_name)


        if request.method== 'POST':
            rep= request.POST['rep']


            g=tblIaMERCHANT.objects.filter(branch=mybranch,status=1)

            workers=[a.id for a in g]



            if rep =='view':
                ddd= request.POST['ddd']

                y,m,d=ddd.split("-")
                y=int(y)
                m=int(m)
                d=int(d)

                ddate =date(y,m,d) #python date object

                dy =factcheck(ddate,workers,mybranch)


                ddate7=ddate.strftime("%Y-%m-%d")

                if staff.ceo==1:
                    return render(request,'Ia/integrity4.html',{'company':mybranch,
                        'user':varuser,
                        'cutt':dy,
                        'datee2':ddate7,
                        'datee':ddate})

            elif rep == 'ferror':
                fffrom = request.POST['fromm']
                tttodate= request.POST['tto']

                dy =factcheck2(fffrom,tttodate,workers,mybranch)

                return render(request,'Ia/integrity3.html',{'company':mybranch, 'user':varuser,'msg':dy})

        else:


            if staff.ceo ==1:


                form=endofdayform()
                msg = ''
                detli=0
                toot=0


                return render(request,'integrity.html',{'company':mybranch,
                    'msg':msg,'user':varuser,
                    'toot':toot,
                    'year':yy,
                    'prod':myy,
                    'detli':detli})
            else:

                form=endofdayform()
                msg = ''
                detli=0
                toot=0


                return render(request,'integrityc.html',{'company':mybranch,
                    'msg':msg,'user':varuser,
                    'toot':toot,
                    'year':yy,
                    'prod':myy,
                    'detli':detli})


    else:
        return HttpResponseRedirect('/login/user/')



@csrf_exempt
def rrep(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']

                business_year,product,report,user=acccode.split(':')

                staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)
                mybranch=tblBRANCH.objects.get(id=staff.branch.id)



                if product == '':
                    msg = 'Select the appropriate product'
                    return render(request,'Ia/selectloan.html',{'msg':msg})


                elif report == "":
                    msg = 'Select the appropriate report'
                    return render(request,'Ia/selectloan.html',{'msg':msg})

                if report == 'view':

                    if product == 'Esusu':
                        return render(request,'integrity1.html',{'rep':report,'year':business_year,'product':product,'user':user})

                    elif product == 'Savings':
                        return render(request,'integritysave.html',{'rep':report})

                    #elif add other products


                elif report == 'ferror':

                    if product == 'Esusu':

                        stf = tblIafieldagent.objects.filter(branch = mybranch,
                            status='Approved',
                            is_declined=0)

                        v= stf.count()


                        cv = tblIatv.objects.filter(branch=mybranch,product='Ajo')


                        if cv.count() ==0:
                            s= stf[0].recdate #python version of the date
                            s1=str(stf[0].recdate) #str version of the date

                            xy,xm,xd=s1.split("-")
                            xy =int(xy)
                            xm=int(xm)
                            xd=int(xd)

                        elif cv.count() ==1:
                            cv=cv.get()
                            s=cv.ddate #python version of the date
                            s1=str(cv.ddate)#str version of the date



                            xy,xm,xd=s1.split("-")
                            xy =int(xy)
                            xm=int(xm)
                            xd=int(xd)
                            p = (monthrange(xy, xm))[-1]

                            if xd == p: #if its the last day of the month

                                if xm ==12: #if the month is december
                                    s= date(xy+1, 1,1) #python version of the date
                                    s1 = str(xy+1) + '-' +str(1) +'-'+str(1)  #str version of the date

                                else: #if the month is not december
                                    s = date(xy,(xm+1),1) #python version of the date
                                    s1 = str(xy) + '-' +str(xm+1) +'-'+str(1) #str  version of the date

                            elif xd < p:
                                s = date(xy,xm,(xd+1)) #python  version of the date
                                s1 = str(xy) + '-' +str(xm) +'-'+str(xd+1) #str  version of the date



                        s3=stf[(v-1)].recdate #python  version of the date
                        s2=str(stf[(v-1)].recdate) #str  version of the date






                        s = date(xy,2,(8)) #python  version of the frommm date ##clean up later
                        s1 = str(xy) + '-' +str(2) +'-'+str(8) #str  version of the date

                        s3 = date(xy,(2),8) #python version of the too date
                        s2 = str(xy) + '-' +str(2) +'-'+str(8) #str  version of the date  ##clean up later



                        if s3.year > xy:

                            s2=str(xy,12,31) #str  version of the date

                            s3=datee(xy,12,31) #python  version of the date

                        return render(request,'integrity2.html',{'rep':report,
                                'fromm1':s, #python verion of frrrom
                                'fromm':s1, #str verion of frrrom
                                'tto':s2,   #str verion of ttto
                                'tto1':s3}) #python verion of ttto

                    elif product == 'Savings':
                        return render(request,'integritysave.html',{'rep':report})



    return HttpResponseRedirect('/login/')






def ajointegrity(request): #tv


    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id

        ourcompany=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


        allmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,status=1)

        realdet = tblapp.objects.get(branch=mybranch)

        yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()


        tdate= date.today()
        myy = []



        if request.method== 'POST':
            rep= request.POST['rep']

            if staff.ceo == 1:
                g=tblIaMERCHANT.objects.filter(branch=mybranch,status=1)
            else:
                g=tblIaMERCHANT.objects.filter(branch=mybranch,staff =memstaff ,status=1)


            workers=[a.id for a in g]



            if rep =='view':
                ddd= request.POST['ddd']
                y,m,d=ddd.split("-")
                y=int(y)
                m=int(m)
                d=int(d)

                ddate =date(y,m,d) #python date object

                dy =factcheck(ddate,workers,mybranch)

                ddate7=ddate.strftime("%Y-%m-%d")

                if staff.ceo==1:
                    return render(request,'integrity4.html',{'company':mybranch,
                        'user':varuser,
                        'cutt':dy,
                        'datee2':ddate7,
                        'datee':ddate})
                else:
                    return render(request,'integrity41.html',{'company':mybranch,
                        'user':varuser,
                        'cutt':dy,
                        'datee2':ddate7,
                        'datee':ddate})

            elif rep == 'ferror':
                fffrom = request.POST['fromm']
                tttodate= request.POST['tto']

                dy =factcheck2(fffrom,tttodate,workers,mybranch)

                return render(request,'Ia/integrity3.html',{'company':mybranch, 'user':varuser,'msg':dy})

        else:
            return HttpResponseRedirect('/login/user/')


    else:
        return HttpResponseRedirect('/login/user/')





def repost(request): #REPOST

    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.code

        mybranch=tblBRANCH.objects.get(code=branch)

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


        if request.method=='POST':
            recdate=request.POST['datee2']

            vid= request.POST.getlist('selected_items')


            x,y,z=recdate.split('-')
            x=int(x)
            y=int(y)
            z=int(z)
            recdate=date(x,y,z)



            stf = tblIafieldagent.objects.filter(branch = mybranch, recdate=recdate,status="Approved", is_declined=0)
            bb= tblIamerchantBank.objects.filter(branch = mybranch,recdate=recdate,status='CR')
            cus= tblIasavings_trans.objects.filter(branch = mybranch,recdate=recdate,status='CR')
            allthrifts =tblIathrift.objects.filter(branch=mybranch)
            customer = tblIaCUSTOMER.objects.filter(branch=mybranch)
            product='Savings'

            for key in vid:
                merchant=tblIaMERCHANT.objects.get(code=key)
                s1 =stf.filter(merchant=merchant)

                for cust in s1:
                    card = cust.purpose
                    thrift_code =cust.code
                    transac_id=cust.transac_id
                    number= int(cust.number)
                    amount = cust.amount
                    ttime=cust.ttime
                    cycle=cust.cycle
                    customer1=customer.get(id=cust.customer.id)
                    customer_code= cust.customer.code
                    thrift = allthrifts.get(code=thrift_code)
                    cus_thrift = thrift.thrift
                    service_charge=thrift.service_charge
                    amount2 = int(cust.amount) - int(service_charge)
                    number2 = number - 1
                    check_service_charge = cus.filter(code=thrift_code,description='Account Maintenance')

                    if check_service_charge.count() > 1 :
                      check_service_charge=check_service_charge[0]
                      cust.programmm='Nj'
                      cust.save()

                    else:
                      if check_service_charge.count() ==1:
                          cust.programmm='Nj'
                          cust.save()

                      elif check_service_charge.count() ==0:
                          cust.programmm='X + Nj'
                          cust.save()



                    fff = cus.filter(code=thrift_code).delete()
                    ggg = bb.filter(code=thrift_code).delete()

                    tblIamerchantBank(branch=mybranch,
                        amount=amount,
                        code = thrift_code,
                        merchant=merchant,
                        customer=customer1,
                        transdate=recdate,
                        product=product,
                        number=number,
                        wallet_type='Main',
                        description='Credit',
                        status='CR',

                        cycle=cycle,
                        transac_id=transac_id,
                        purpose = card,
                        year=recdate.year,
                        ttime=ttime,
                        recdate=recdate,
                        approved_by=staff).save()

                    if cust.programmm == "X + Nj":

                        tblIasavings_trans(branch=mybranch,
                            amount=service_charge,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=recdate,
                            product= product,
                            number=1,
                            wallet_type='Main',
                            description='Account Maintenance',
                            status='CR',
                            purpose = card,
                            ttime=ttime,
                            transac_id=transac_id,
                            recdate=recdate,
                            cycle=cycle,
                            avalability='Not Available',
                            year=recdate.year).save()


                        if amount2 > 0:

                            tblIasavings_trans(branch=mybranch,
                                amount=amount2,
                                code = thrift_code,
                                merchant=merchant,
                                customer=customer1,
                                transdate=recdate,
                                product=product,
                                number=number2,
                                wallet_type='Main',
                                description='Credit',
                                status='CR',
                                purpose = card,
                                ttime=ttime,
                                transac_id=transac_id,
                                recdate=recdate,
                                cycle=cycle,
                                avalability='Available',
                                year=recdate.year).save()



                    elif cust.programmm == "Nj":

                        tblIasavings_trans(branch=mybranch,
                            amount=amount,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=recdate,
                            product=product,
                            number=number,
                            wallet_type='Main',
                            description='Credit',
                            status='CR',
                            purpose = card,
                            ttime=ttime,
                            transac_id=transac_id,
                            recdate=recdate,
                            cycle=cycle,
                            avalability='Available',
                            year=recdate.year).save()

                    else :

                        tblIasavings_trans(branch=mybranch,
                            amount=amount,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=recdate,
                            product=product,
                            number=number,
                            wallet_type='Main',
                            description='Credit',
                            status='CR',
                            purpose = card,
                            ttime=ttime,
                            transac_id=transac_id,
                            recdate=recdate,
                            cycle=cycle,
                            avalability='Available',
                            year=recdate.year).save()


            if staff.ceo==1:
                return render(request,'integrity5.html',{'company':mybranch,
                            'user':varuser,
                            # 'cutt':dy,
                            'details':dp,
                            'datee':recdate})


            elif staff.thrift_officer==1:
                return render(request,'integrity5.html',{'company':mybranch,
                            'user':varuser,
                            # 'cutt':dy,
                            # 'details':dp,
                            'datee':recdate})

    else:
        return HttpResponseRedirect('/login/user/')


def repost_ori(request): #REPOST

    if 'userid' in request.session:
        varuser=request.session['userid']

        try:
            staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
        except:
            return render(request,'Ia/404.html')

        staffdet=staff.staffrec.id

        branch=staff.branch.code

        mybranch=tblBRANCH.objects.get(code=branch)

        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


        if request.method=='POST':
            recdate=request.POST['datee2']

            vid= request.POST.getlist('selected_items')


            x,y,z=recdate.split('-')
            x=int(x)
            y=int(y)
            z=int(z)
            recdate=date(x,y,z)



            stf = tblIafieldagent.objects.filter(branch = mybranch, recdate=recdate,status="Approved", is_declined=0)
            bb= tblIamerchantBank.objects.filter(branch = mybranch,recdate=recdate,status='CR')
            cus= tblIasavings_trans.objects.filter(branch = mybranch,recdate=recdate,status='CR')
            allthrifts =tblIathrift.objects.filter(branch=mybranch)
            customer = tblIaCUSTOMER.objects.filter(branch=mybranch)
            product='Savings'

            for key in vid:
                merchant=tblIaMERCHANT.objects.get(code=key)
                s1 =stf.filter(merchant=merchant)

                for cust in s1:
                    card = cust.purpose
                    thrift_code =cust.code
                    transac_id=cust.transac_id
                    number= int(cust.number)
                    amount = cust.amount
                    ttime=cust.ttime
                    cycle=cust.cycle
                    customer1=customer.get(id=cust.customer.id)
                    customer_code= cust.customer.code
                    thrift = allthrifts.get(code=thrift_code)
                    cus_thrift = thrift.thrift
                    service_charge=thrift.service_charge
                    amount2 = int(cust.amount) - int(service_charge)
                    number2 = number - 1
                    check_service_charge = cus.filter(code=thrift_code,description='Account Maintenance')

                    if check_service_charge.count() > 1 :
                      check_service_charge=check_service_charge[0]
                      cust.programmm='Nj'
                      cust.save()

                    else:
                      if check_service_charge.count() ==1:
                          cust.programmm='Nj'
                          cust.save()

                      elif check_service_charge.count() ==0:
                          cust.programmm='X + Nj'
                          cust.save()



                    fff = cus.filter(code=thrift_code).delete()
                    ggg = bb.filter(code=thrift_code).delete()

                    tblIamerchantBank(branch=mybranch,
                        amount=amount,
                        code = thrift_code,
                        merchant=merchant,
                        customer=customer1,
                        transdate=recdate,
                        product=product,
                        number=number,
                        wallet_type='Main',
                        description='Credit',
                        status='CR',

                        cycle=cycle,
                        transac_id=transac_id,
                        purpose = card,
                        year=recdate.year,
                        ttime=ttime,
                        recdate=recdate,
                        approved_by=staff).save()

                    if cust.programmm == "X + Nj":

                        tblIasavings_trans(branch=mybranch,
                            amount=service_charge,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=recdate,
                            product= product,
                            number=1,
                            wallet_type='Main',
                            description='Account Maintenance',
                            status='CR',
                            purpose = card,
                            ttime=ttime,
                            transac_id=transac_id,
                            recdate=recdate,
                            cycle=cycle,
                            avalability='Not Available',
                            year=recdate.year).save()


                        if amount2 > 0:

                            tblIasavings_trans(branch=mybranch,
                                amount=amount2,
                                code = thrift_code,
                                merchant=merchant,
                                customer=customer1,
                                transdate=recdate,
                                product=product,
                                number=number2,
                                wallet_type='Main',
                                description='Credit',
                                status='CR',
                                purpose = card,
                                ttime=ttime,
                                transac_id=transac_id,
                                recdate=recdate,
                                cycle=cycle,
                                avalability='Available',
                                year=recdate.year).save()



                    elif cust.programmm == "Nj":

                        tblIasavings_trans(branch=mybranch,
                            amount=amount,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=recdate,
                            product=product,
                            number=number,
                            wallet_type='Main',
                            description='Credit',
                            status='CR',
                            purpose = card,
                            ttime=ttime,
                            transac_id=transac_id,
                            recdate=recdate,
                            cycle=cycle,
                            avalability='Available',
                            year=recdate.year).save()

                    else :

                        tblIasavings_trans(branch=mybranch,
                            amount=amount,
                            code = thrift_code,
                            merchant=merchant,
                            customer=customer1,
                            transdate=recdate,
                            product=product,
                            number=number,
                            wallet_type='Main',
                            description='Credit',
                            status='CR',
                            purpose = card,
                            ttime=ttime,
                            transac_id=transac_id,
                            recdate=recdate,
                            cycle=cycle,
                            avalability='Available',
                            year=recdate.year).save()



            return render(request,'Ia/selectloan.html',{'msg':'done'})




            stf = tblIafieldagent.objects.filter(branch = mybranch, recdate=recdate)
            bb= tblIamerchantBank.objects.filter(branch = mybranch,recdate=recdate)
            cus= tblIasavings_trans.objects.filter(branch = mybranch,recdate=recdate)

            dy=[]
            dp=[]

            for wk in workers:
                w=tblIaMERCHANT.objects.get(code=wk)

                g = stf.filter(merchant=w,recdate=recdate,status='Approved',is_declined=0)
                if g.count() >0:

                    stafff = g.aggregate(Sum('amount'))
                    stafff = int(stafff['amount__sum'])
                else:
                    stafff=0

                biz= bb.filter(merchant=w,
                                recdate=recdate,
                                status='CR',
                                description='Credit',
                                product='Savings')

                if biz.count() >0:

                    bzz = biz.aggregate(Sum('amount'))
                    bzz = int(bzz['amount__sum'])

                else:
                    bzz = 0


                cuzz= cus.filter(merchant=w,
                                 recdate=recdate,
                                 product='Savings',
                                 status='CR')

                if cuzz.count() >0:
                    ccc = cuzz.aggregate(Sum('amount'))
                    ccc = int(ccc['amount__sum'])
                else:
                    ccc=0


                vb= {'sss':stafff,'bbbb':bzz,'cus':ccc,'worker':w}

                dy.append(vb)



                details= {'field':g,'office':biz,'customer':cuzz}

                dp.append(details)

            if staff.ceo==1:
                return render(request,'Ia/integrity5.html',{'company':mybranch,
                            'user':varuser,
                            'cutt':dy,
                            'details':dp,
                            'datee':recdate})


            elif staff.thrift_officer==1:
                return render(request,'Ia/howitworks_t.html',{'company':mybranch, 'user':varuser})

    else:
        return HttpResponseRedirect('/login/user/')

def vintegrity(request): #tv
    varuser=request.session['userid']

    try:
        staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
    except:
        return render(request,'Ia/404.html')

    staffdet=staff.staffrec.id

    branch=staff.branch.id
    mycompany=staff.branch.company
    company=mycompany.name
    comp_code=mycompany.id

    ourcompany=tblCOMPANY.objects.get(id=comp_code)

    mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

    memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


    allmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,status=1)

    realdet = tblapp.objects.get(branch=mybranch)



    g=tblIaMERCHANT.objects.filter(branch=mybranch,status=1)

    workers=[a.id for a in g]



    ddd= request.POST['ddd']

    y,m,d=ddd.split("-")
    y=int(y)
    m=int(m)
    d=int(d)

    ddate =date(y,m,d) #python date object

    dy =factcheck(ddate,workers,mybranch)


    ddate7=ddate.strftime("%Y-%m-%d")

    if staff.ceo==1:
        return render(request,'Ia/integrity4.html',{'company':mybranch,
            'user':varuser,
            'cutt':dy,
            'datee2':ddate7,
            'datee':ddate})






    else:
        return HttpResponseRedirect('/login/user/')






#### **** END OF LEDGER ENTRIES ****************