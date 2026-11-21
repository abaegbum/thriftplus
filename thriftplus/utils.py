from partner.models import *
from business.models import *
from staff.models import *
from sysadmin.models import *

import random

def new_fresh(): ########PARTNER REGISTRATION*******************

    pp = 	tblPARTNER.objects.filter(status=1,email='p1@gmail.com')

    if pp.count() == 0:
    	tblPARTNER(status=1,code=99098007,surname='Chibugwu',
    		firstname='mathew',othername='Okechukwu',
    		email='p1@gmail.com').save()


    partner = pp.get(email='p1@gmail.com')

    cc	= tblCOMPANY.objects.filter(name='Chidemavian Partners',status=1,partner=partner)

    if cc.count() == 0:
    	tblCOMPANY(engine='tts',web='tp.com',code='377',
    		name='Chidemavian Partners',status=1,partner=partner,
    		ux = 0,	size=100,logo='company_logo/thrift.png').save()

    comp = cc.get(name='Chidemavian Partners')

    bb = 	tblBRANCH.objects.filter(company=comp)

    if bb.count()== 0:
    	tblBRANCH(status=1,code=989,currency_description='Naira',
    		company=comp,phone='07031009036',
    		types='Head',Address='park avenue, Mexico City',
    		currency_code='NGN').save()


    mybranch=bb.get(company = comp)

    ss =	tblSTAFF.objects.filter(branch=mybranch,email='p1@gmail.com')

    if ss.count() == 0:
    	tblSTAFF(status=1,branch=mybranch,code=22,surname='abaegbu',
    		firstname='mathew',
    		othername='Okechukwu',
    		photo='staff_pix/user.png',
    		email='p1@gmail.com',
    		ceo=0,
    		phone='07031009036',Address='Los Angeles',types='office').save()


    # staff = ss.get(branch= mybranch, email='p1@gmail.com')
    staff = ss.get(email='p1@gmail.com')


    uuu = 	Userprofile.objects.filter(staffrec=staff,partner=1,ceo=0,branch=mybranch,email='p1@gmail.com',status=1)


    if uuu.count() == 0 :
    	Userprofile(code=778,staffrec=staff,partner=1,
    		ceo=0,branch=mybranch,email='p1@gmail.com',status=1,
    		password='partner').save()


    q=	tblthriftpackages.objects.filter(package = '-----')
    if q.count() == 0:
    	tblthriftpackages(status=1, package = '-----', appendage='Trial', customer_count = 0, cost = 0, staff_count = 0).save()

    ob = tblthriftpackages.objects.filter(package='Onboarding')
    if ob.count()==0:
    	tblthriftpackages(weight=1,status=1,package='Onboarding', appendage='Trial',customer_count=5, cost=0 ,staff_count=2).save()

    sg = tblthriftpackages.objects.filter(package='Lite', appendage='Green')
    if sg.count() == 0:
    	tblthriftpackages(weight=2,status=1,package='Lite', appendage='Green', customer_count=200, cost=15785.44 ,staff_count=1).save()

    sp = tblthriftpackages.objects.filter(package='Starter', appendage='Peach')
    if sp.count() == 0:
    	tblthriftpackages(weight=3,status=1,package='Starter', appendage='Peach',customer_count=100000000, cost=21980.58 ,staff_count=1).save()

    wb = tblthriftpackages.objects.filter(package='Core',appendage='Bronze')
    if wb.count() == 0:
    	tblthriftpackages(weight=4,status=1,package='core',appendage='Bronze',customer_count=550, cost=33595.84 ,staff_count=3).save()

    ws = tblthriftpackages.objects.filter(package='Growth',appendage='Silver')

    if ws.count() == 0:
    	tblthriftpackages(weight=5,status=1,package='Growth',appendage='Silver',customer_count=100000000, cost=39953.93 ,staff_count=3).save()

    jg = tblthriftpackages.objects.filter(package='Jumbo', appendage='Gold')
    if jg.count()==0:
    	tblthriftpackages(weight=8,status=1,package='Jumbo', appendage='Gold',  customer_count=100000000, cost=25853.24 ,staff_count=100).save()

    wb = tblthriftpackages.objects.filter(package='Professional',appendage='Pearl')
    if wb.count() == 0:
        tblthriftpackages(weight=6,status=1,package='Professional',appendage='Pearl',customer_count=700, cost=59781.61 ,staff_count=5).save()

    ws = tblthriftpackages.objects.filter(package='Enterprise',appendage='Gem')

    if ws.count() == 0:
        tblthriftpackages(weight=7,status=1,package='Enterprise',appendage='Gem',customer_count=900, cost=79694.20 ,staff_count=7).save()


    es = tblmyproducts.objects.filter(product='Esusu')
    if es.count() == 0:
    	tblmyproducts(product='Esusu',code=798768).save()

    sa = tblmyproducts.objects.filter(product='Savings')
    if sa.count() == 0:
    	tblmyproducts(product='Savings',code=2356648).save()



    ppl = tblbusinesspresence.objects.filter(country = 'Nigeria')
    if ppl.count()==0:
        tblbusinesspresence(country='Nigeria',
            country_code='+234', currency_code='NGN',
            status=True,currency_description= 'Naira').save()



    return 'ok'





def checksub(bbb,service):
    sd_history = tblsubscription.objects.filter(branch=bbb,app=service)

    sd_history_count = sd_history.count()


    if sd_history_count> 0:


        uy= [x.id for x in sd_history]


        # return sd_history.count()
        suhi=sd_history.get(id=uy[-1])

        if suhi.status =='Queing':
            history=sd_history.get(id=uy[-2])

        else:
            history=sd_history.get(id=uy[-1])

        details= {'status':history.status,
        'staff_count':history.package.staff_count,
        'customer_count':history.package.customer_count,
        'package':history.package.package,
        'subscription_receipt':history.receipt,
        'appendage':history.package.appendage,
        'service':service,
        'stop':history.end}

    else:
        details= {'status':0,
        'staff_count':0,
        'customer_count':0,
        'package':0,
        'appendage':0,
        'service':0,
        'stop':0}


    return details


def checkhighestsub(branch):

    yyapp = tblapp.objects.get(branch=branch)
    sss=[]
    sta=[]
    staf=[]

    if yyapp.thrift1a==True:
        if yyapp.esusu1a==True:
            app ='Esusu'
            history= checksub(branch,app)
            sss.append(int(history['customer_count']))
            sta.append((history['status']))
            staf.append((history['staff_count']))


        if yyapp.savings1a==True:
            app ='General Savings'
            history= checksub(branch,app)
            sss.append(int(history['customer_count']))
            sta.append((history['status']))
            staf.append((history['staff_count']))


        if yyapp.ecomerce==True:

            app ='Ecommerce'
            history= checksub(branch,app)
            sss.append(int(history['customer_count']))
            sta.append((history['status']))
            staf.append((history['staff_count']))



        if yyapp.investment==True:

            app ='Investment'
            history= checksub(branch,app)
            sss.append(int(history['customer_count']))
            sta.append((history['status']))
            staf.append((history['staff_count']))



        sorted_numbers_desc = sorted(sss, reverse=True)[0] #removes repeatition


        sta = sorted(sta, reverse=True)[0] #removes repeatition

        staf = sorted(staf, reverse=True)[0] #removes repeatition


        details= {'staff':staf,'status':sta,'numbers':sorted_numbers_desc}


    else:
        details= {'staff':0,'status':0,'numbers':0}



    return details



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







def programatic_reposting(biz): #factor in direct crediting

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


        thriftrec = tblIathrift.objects.filter(branch=mybranch,monthindex=6)#[:20]

        kl = thriftrec.count()

        a=[]
        [a.append(b.code) for b in thriftrec]

        gp =[]
        [gp.append(p) for p in a if p not in a]
        kl = len(gp),len(a),

        stf = tblIafieldagent.objects.filter(branch=mybranch,status="Approved",is_declined=0)
        bz= tblIamerchantBank.objects.filter(branch=mybranch)
        cz= tblIasavings_trans.objects.filter(branch=mybranch)


        customer = tblIaCUSTOMER.objects.filter(branch=mybranch)
        merchant2= tblIaMERCHANT.objects.filter(branch=mybranch)

        product ='Savings'


        for code in a:
            s1 = stf.filter(code=code)
            s2 = bz.filter(code=code,status='CR').delete()
            s3 = cz.filter(code=code,status='CR').delete()

            for cust  in s1:
                mid =cust.merchant.id
                merchant = merchant2.get(id= mid)
                recdate= cust.recdate

                card = cust.purpose
                thrift_code =code
                transac_id=cust.transac_id
                number= int(cust.number)
                amount = cust.amount
                ttime=cust.ttime
                cycle=cust.cycle
                customer1=customer.get(id=cust.customer.id)
                customer_code= cust.customer.code
                thrift = thriftrec.get(code=thrift_code)
                cus_thrift = thrift.thrift
                service_charge=thrift.service_charge
                amount2 = int(cust.amount) - int(service_charge)
                number2 = number - 1


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


                s21 = cz.filter(code=code,status='CR')

                if s21.count() == 0:
                    if number ==1:
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

                    else:
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

                    cust.programmm='X + Nj'
                    cust.save()
                else:

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

                    cust.programmm='Nj'
                    cust.save()

        return render(request,'howitworks.html',{'company':mybranch,
                    'user':varuser,"staff":staff,'msg':kl})

    else:
        return HttpResponseRedirect('/login/user/')


def program_after_deposite(bb): #programmatic after_deposit

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




        year=2025
        thrifts = tblIathrift.objects.filter(branch=mybranch,year=year)
        stf = tblIafieldagent.objects.filter(branch=mybranch,status="Approved",is_declined=0,year=year)


        for mn in range(2,7):

            thriftrec = thrifts.filter(monthindex=mn)

            a=[]
            [a.append(b.code) for b in thriftrec]

            for code in a:
                customer_code= thrifts.get(code = code).customer.code

                tb = stf.filter(code=code)
                if tb.count() > 0:

                    ws = tb.aggregate(Sum('number'))
                    total_save = int(ws['number__sum'])
                    after_deposit(customer_code, code,varuser,total_save)




def rename_cycle(mn):

	ttp = thrift.filter(cycle=cycle ).values_list('code',flat=True)

	f = fa.get(code=mn.code)

	sd = cus.filter(code__in = ttp,status = 'CR')

	cc = ofi.filter(code__in = ttp,status = 'CR')

	g= {'staff':f,'customer':sd,'office':cc,'thrift':thrift}
	s=[]
	s.append(g)


	thrift_count = thrift.count() + 2

	thriftcode = thriftcode
	cycle2= f"cycle {thrift_count}"


	cus.filter(code=thriftcode).update(cycle = cycle2)
	ofi.filter(code=thriftcode).update(cycle = cycle2)
	fa.filter(code=thriftcode).update(cycle = cycle2)
	thrift.filter(code=thriftcode).update(cycle = cycle2)



def rename_cycle(row, fa, cus, ofi, thrift):
    yr = row['year']
    month = row['month']
    cycle = row['cycle']
    customer = row['customer']

    thr = thrift.filter(customer=customer,month=month,year=yr)

    cycles = [int(t.cycle.split()[-1]) for t in thr]

    missing = sorted(set(range(1, max(cycles)+1)) - set(cycles))


    thr2 = thr.filter(cycle=cycle)

    if thr2.count() == 2:

        th = thr2.filter(cycle=cycle).first()

        thrift_count = thr.count() + 1

        if len(missing) == 0:

            cycle2 = f"cycle {thrift_count}"
        else:

            cycle2 = f"cycle {missing[0]}"


        thriftcode = th.code


        # Update cycle field across related tables
        customer = cus.filter(code=thriftcode)
        cus = customer.update(cycle = cycle2)

        office = ofi.filter(code=thriftcode)
        ofi = office.update(cycle = cycle2)

        field = fa.filter(code=thriftcode)
        fa = field.update(cycle = cycle2)

        th.cycle= cycle2
        th.save()

        d = f"thrift_count is {thrift_count}, cycle2 is {cycle2}, thriftcode is {thriftcode}, customer count is {customer.count()}, office count is  {office.count()}, field  count is {field.count()}, th count is {th.cycle}"




    return d


