from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt






from sysadmin.models import *
from IIIb.models import *
from IIIb.forms import *
from IIIb.utils import *
from django.db.models import Case, When, Value, IntegerField, Sum
import calendar
from num2words import num2words
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json



# from thriftplus.settings import EMAIL_HOST_USER
# from django.core.mail import send_mail
# from calendar import monthrange
# from django.core.serializers.json import json
# from django.db.models import Max,Sum
# from customer.models import *
# import locale
# from datetime import *
# import random
# ddatt=date.today()
# from Ib.models import *




####HOW IT WORKS *****************************
def howitworks(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



		if staff.thrift3b_admin==1:
			return render(request,'IIIb/howitworks.html',{'company':mybranch, 'user':varuser})

		elif staff.thrift3b_cashier==1:
			return render(request,'IIIb/howitworks_c.html',{'company':mybranch, 'user':varuser})
			
		elif staff.thrift3b_officer==1:
			return render(request,'IIIb/howitworks_o.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')





#### COOPERATORS  *****************************
def stafflist(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id


		mybranch=tblBRANCH.objects.get(id=branch)

		if staff.ceo==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		stafflist = tblSTAFF.objects.filter(branch=mybranch,status=1)
		
		if staff.thrift3b==1:
			stafflist= tblIIIbcoop.objects.filter(branch=mybranch).order_by('staff__surname')
			return render(request,'IIIb/cooperators.html',{'company':mybranch, 'user':varuser,'list':stafflist})


	else:
		return HttpResponseRedirect('/login/user/')


# def adminwelcome(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff=Userprofile.objects.get(email=varuser, status=1)
# 		staffdet=staff.staffrec.id

# 		branch=staff.branch.id
# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id

# 		ourcompany=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

# 		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


# 		if staff.thrift3b_officer==0:
# 			return render(request,'IIIb/404loan.html',{'company':mybranch, 'user':varuser})

# 		return render(request,'IIIb/dashboardIIIb.html',{'company':mybranch, 'user':varuser,'pincode':staff})

# 	else:
# 		return HttpResponseRedirect('/login/user/')



########Settings**********************
def application_form(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)


		loans = tblstandardloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		fff= tblIIIIsubscriptionfee.objects.filter(branch=mybranch)

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			application_fee=request.POST['applicationfee']


			if not tblIIIIsubscriptionfee.objects.filter(branch=mybranch).exists():

				tblIIIIsubscriptionfee.objects.create(branch=mybranch,amount=application_fee)

				
			return render(request,'IIIb/settings_application_form2.html',{'company':mybranch, 'user':varuser})
		

		else:
			if fff.count() == 0:
				return render(request,'IIIb/settings_application_form.html',{'company':mybranch, 'user':varuser,'loans':loans})
			
			elif fff.count() ==1:
				fff=fff.get()
				return render(request,'IIIb/settings_application_form1.html',{'company':mybranch, 'user':varuser,'amount':fff})
	else :
		return HttpResponseRedirect('/login/user/')




def loan_setup(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)


		loans = tblstandardloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)



		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			description=request.POST['package']
			rate= request.POST['rate']
			fromm= request.POST['fromm']
			pack_count=loans.count()

			sss=tblIIIbcoop.objects.filter(staff=user)

			if sss.count() ==1:
				user=sss.get()


			if pack_count == 0 :
				tblstandardloanIIIB(staffrec=user,branch=mybranch,rate = 0 ,description='-----', 
					status=True,tenure  = 0 ).save()

				tblstandardloanIIIB(staffrec=user,branch=mybranch,rate = rate ,status= True, 
					description=description, tenure =fromm).save()
			else:

				tblstandardloanIIIB(staffrec=user,branch=mybranch,rate = rate ,status= True, 
					description=description, tenure =fromm).save()
			msg = "package added successfully"
			return render(request,'IIIb/settings_loan1.html',{'company':mybranch, 'user':varuser,'msg':msg})



		return render(request,'IIIb/settings_loan.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/user/')


def loan_limit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)


		loan_limit = tblmaxloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			rate=request.POST['rate']
			tblmaxloanIIIB(branch=mybranch,value=rate).save()

			return render(request,'IIIb/settings_loanlimit2.html',{'company':mybranch, 'user':varuser,'rate':rate})



		else:
			cv= {'company':mybranch, 'user':varuser}#,'loans':loan_limit}
			if loan_limit.count() > 0:
				cv['loans'] =loan_limit
				
				return render(request,'IIIb/settings_loanlimit1.html',cv)
			else:
				return render(request,'IIIb/settings_loanlimit.html',cv)
	else :
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def max_loan_pop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':
    		varuser = request.session['userid']
    		varerr =""
    		post = request.POST.copy()
    		acccode = post['userid']
    		f= tblmaxloanIIIB.objects.get(id=acccode)

    		return render(request,'IIIb/settings_loanlimit_pop.html',{'maxloan':f})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def max_loan_edit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		
		mybranch=tblBRANCH.objects.get(id=branch)

		if staff.thrift3b_admin==0 :
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			maxloan_index =int(request.POST['maxloanindex'])
			maxloan =request.POST['maxloan']

			g= tblmaxloanIIIB.objects.get(id=maxloan_index)
			g.value=maxloan
			g.save()

			
			return render(request,'IIIb/settings_loanlimit2.html',{'company':mybranch, 'user':varuser,'rate':maxloan})

			# return render(request,'IIIb/settings_loanlimit2.html',cv)




	else :
		return HttpResponseRedirect('/login/user/')



def savings_setup(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)


		loans = tblstandardsavingIIIB.objects.filter(branch=mybranch).order_by('active').reverse()

		user=tblSTAFF.objects.get(email=varuser)
		user=tblIIIbcoop.objects.get(branch=mybranch,staff=user)

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			description=request.POST['package']
			frommonth=int(request.POST['month_from'])
			tomonth=int(request.POST['month_to'])

			from_month_name = calendar.month_name[frommonth]
			to_month_name = calendar.month_name[tomonth]


			pack_count=loans.count()
			description=description.capitalize()

			if pack_count == 0 :

				tblstandardsavingIIIB(active = True, 
					description='Wallet', 
					staffrec=user,
					branch=mybranch,
					from_month='January',
					to_month='December').save()

				tblstandardsavingIIIB(active = True, 
					description=description, 
					staffrec=user,
					branch=mybranch,
					from_month=from_month_name,
					to_month=to_month_name).save()

			else:



				if not loans.filter(description=description).exists():

					tblstandardsavingIIIB.objects.create(active = True,
						description=description, 
						staffrec=user,
						branch=mybranch,
						from_month=from_month_name,
						to_month=to_month_name)


			msg = "package added successfully"
			return render(request,'IIIb/settings_savings1.html',{'company':mybranch, 'user':varuser,'msg':msg})

		else:
			# form = setsave()
			return render(request,'IIIb/settings_savings.html',{'company':mybranch, 
				'user':varuser,
				'loans':loans})
	else :
		return HttpResponseRedirect('/login/user/')



####Manage settings****************
def manage_setup(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)


		loans = tblstandardsavingIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = setsave(request.POST)
			if form.is_valid():
				description=request.POST['package']
				frommonth=form.cleaned_data['month_from']
				tomonth=form.cleaned_data['month_to']


				pack_count=loans.count()

				if pack_count == 0 :
					tblstandardsavingIIIB(description='-----', staffrec=user,branch=mybranch,status='ACTIVE',from_month=0,to_month=0).save()
					tblstandardsavingIIIB(active = True, description=description, staffrec=user,branch=mybranch,from_month=frommonth,to_month=tomonth).save()
				else:
					tblstandardsavingIIIB(active = True,description=description, staffrec=user,branch=mybranch,from_month=frommonth,to_month=tomonth).save()
				msg = "package added successfully"
				return render(request,'IIIb/addsavee.html',{'company':mybranch, 'user':varuser,'msg':msg})

		else:
			form = setsave()
		return render(request,'IIIb/settings_manage.html',{'company':mybranch, 'user':varuser,'loans':loans,'form':form})
	else :
		return HttpResponseRedirect('/login/user/')



####opening balance****************

def opening(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)


		loans = tblstandardloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			email=request.POST['email']
			try:
				staff = tblSTAFF.objects.get(branch=mybranch, email=email)
			except:
				msg = 'Invalid Email'
				return render(request,'IIIb/selectloan.html',{'msg':msg})

			staff2= tblIIIbcoop.objects.get(staff=staff)
			amt = tblIIIbsavingsaccount.objects.filter(branch=mybranch, staff=staff2, account_type='Wallet')
			amt =amt.aggregate(Sum('amount'))
			amt = amt['amount__sum']
			return render(request,'IIIb/settings_opening_bal.html',{'company':mybranch, 'user':varuser,'staff':staff,'tot':amt})


		return render(request,'IIIb/settings_opening.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/user/')


def uppld(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)

		loans = tblstandardloanIIIB.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		llgg = LGA.objects.all().count()

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			if request.FILES['input_excel']:

				if llgg < 1 :
					input_excel=request.FILES['input_excel']
					num = []
					rows = "testing"
					book = xlrd.open_workbook(file_contents=input_excel.read())
					sheet = book.sheet_by_index(0)
					for row_no in range(0, sheet.nrows):
						rows = sheet.row_values(row_no)
						num.append(rows)
					ncount = len(num)

					try:
						for k in num:
							j1 = k[0]
							j2 = k[1]
							savecon = LGA (state = j1,lga = j2)
							savecon.save()
						succ = "Record Uploaded !!!"
						return render(request,'IIIb/settings_upload.html',{'succ':succ})
					except:
						succ ="Uploading Error "
					return render(request,'IIIb/settings_upload.html',{'succ':succ})

		return render(request,'IIIb/settings_upload.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/user/')








	####*******My wallet*******************
def history(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		cid=coop.id
		

		amount= walletbalance(mybranch,coop)

		myothers= otherbalance(mybranch,coop)

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]

		bb = {'company':mybranch,
				'user':varuser,
				'year':yy,
				'msg':coop,
				'others':myothers,
				'amount':amount}


		if staff.thrift3b_admin==1:
			return render(request,'IIIb/mywallet_balance_adm.html',bb)

		elif staff.thrift3b_cashier==1:
			return render(request,'IIIb/mywallet_balance_cash.html',bb)

		elif staff.thrift3b_officer==1:
			return render(request,'IIIb/mywallet_balance_o.html',bb)

	else:
		return HttpResponseRedirect('/login/user/')


def statement(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)



		staffdet=staff.staffrec.id
		branch=staff.branch.id

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)



		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]
		

		month_order = Case(
		    When(month="January", then=Value(1)),
		    When(month="February", then=Value(2)),
		    When(month="March", then=Value(3)),
		    When(month="April", then=Value(4)),
		    When(month="May", then=Value(5)),
		    When(month="June", then=Value(6)),
		    When(month="July", then=Value(7)),
		    When(month="August", then=Value(8)),
		    When(month="September", then=Value(9)),
		    When(month="October", then=Value(10)),
		    When(month="November", then=Value(11)),
		    When(month="December", then=Value(12)),
		    output_field=IntegerField(),
		)

		statement=tblIIIbsavingsaccount.objects.filter(branch=mybranch,staff=coop).annotate(month_index=month_order
		).order_by('month_index','account_type')


		sav=statement.filter(status='CR')

		if sav.count()>0:

			add=sav.aggregate(Sum('amount'))
			add_cr = add['amount__sum']
		else:
			add_cr = 0


		sav_dr=statement.filter(status='DR') 


		if sav_dr.count()>0 :
			add=sav_dr.aggregate(Sum('amount'))
			add_dr = add['amount__sum']
		else:
			add_dr =0

		amount=add_cr - add_dr

		bv ={'company':mybranch,
				'user':varuser,
				'msg':coop,
				'year':yy,
				'statement':statement,
				'amount':amount}
		if staff.thrift3b_admin==1:
			return render(request,'IIIb/mywallet_statement.html',bv)

		elif staff.thrift3b_cashier==1:
			return render(request,'IIIb/mywallet_statement_c.html',bv)

		elif staff.thrift3b_officer==1:
			return render(request,'IIIb/mywallet_statement_o.html',bv)

	else:
		return HttpResponseRedirect('/login/user/')


def withdraw(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})



		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)


		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)



		if request.method=='POST':
			year = request.POST['year']
			source=request.POST['source']
			amount=request.POST['amount']

			datte = date.today()


			h= tblIIIbsavingsaccount.objects.filter(branch=mybranch,staff=coop,year=year,account_type=source)

			account_code=[a.account_code for a in h][0]

			ds = tblIIIIbscheme_withdrawal.objects.filter(branch=mybranch,staff=coop, year=year, description=source)

			# return render(request,'IIIb/selectloan.html',{'msg':account_code})

			if ds.count() == 1:
				ds2=ds.get()
				status=d2.status

				if status=='Disbursed':
					return render(request,'IIIb/mywallet_withdraw_disbursed_ajax.html',{
	        			'company':mybranch, 'user':varuser,
	        			'msg':allaplication,
	        			'status':source, 
	        			'year':year,
	        			'total':total})


			elif ds.count() == 0:

				tblIIIIbscheme_withdrawal.objects.create(branch=mybranch,
					staff=coop, 
					year=year,	
					description=source,
					scheme_authorization_code =account_code,
					transdate=datte,
					amount= amount,
					status='Awaiting Disbursal')


				return render(request,'IIIb/mywallet_withdraw_success.html',{
	    			'company':mybranch, 
	    			'user':varuser,
	    			'status':source,
	    			'year':year,
	    			'total':amount})


		else:
			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]

			myothers= otherbalance(mybranch,coop)

			
			repay = tblstandardsavingIIIB.objects.filter(branch=mybranch).exclude(description='Wallet')


			bn ={'company':mybranch,'user':varuser,	'msg':coop,'year':yy,
					'repay':repay, 
					'others':myothers}


			if staff.thrift3b_admin==1:
				return render(request,'IIIb/mywallet_withdraw_adm.html',bn)

			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/mywallet_withdraw_cash.html',bn)

			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/mywallet_withdraw_o.html',bn)

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def withdrawajax(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,source=acccode.split(":")


        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id

        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)


        		if source=='-':
        			msg='Select target account'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})



	        	datte =date.today()
	        	withdraw_month = datte.month
	        	withdraw_year = datte.year



        		allaplication = tblIIIbsavingsaccount.objects.filter(branch=mybranch,staff=kfw,
        			year=year, account_type =source)



	        	total_cr = allaplication.filter(status='CR').aggregate(total=Sum('amount'))['total'] or 0

	        	total_dr = allaplication.filter(status='DR').aggregate(total=Sum('amount'))['total'] or 0


	        	
	        	total=total_cr - total_dr
	        	

	        	bv= tblstandardsavingIIIB.objects.get(branch=mybranch, description=source)
	        	package_end_month =bv.to_month #month_name
	        	package_end_year = year

   

	        	month_order = { "January": 1, "February": 2,"March": 3,	"April": 4,	"May": 5,"June": 6,	"July": 7,	"August": 8,"September": 9,	"October": 10,	"November": 11,	"December": 12}

	        	#convert_package_end_month to index
	        	come_back = month_order[package_end_month]

	        	come_back_num= come_back + 1


	        	#converts come_back_num to month_name
	        	month_lookup = {v: k for k, v in month_order.items()}
	        	come_back_month = month_lookup[come_back_num]

	        

	        	if withdraw_year == int(package_end_year):

	        		if  withdraw_month < month_order[package_end_month] :
	        			p= "Withdrawable"
	        		else:
	        			p = f"The funds in your {source} account is LOCKED. It Will be withdrawable from {come_back_month}"
	        			# return render(request,'IIIb/selectloan.html',{'msg':p})

	        	elif withdraw_year > int(package_end_year):
	        		p= 'Withdrawable'



	        	ds = tblIIIIbscheme_withdrawal.objects.filter(branch=mybranch,staff=kfw, year=year,	description=source)


	        	# p= f"ds is {ds}"
	        	# return render(request,'IIIb/selectloan.html',{'msg':p})


        		if ds.count() > 0:

        			ds2=ds.get()
        			status=ds2.status

        			p = f"Your funds is {status}"


        		return render(request,'IIIb/mywallet_withdraw_ajax.html',{'company':mybranch, 'email':varuser,
        			'msg':allaplication,
        			'status':source, 
        			'year':year,
        			'p':p,
        			'total':total,'total_cr':total_cr,'total_dr':total_dr})

        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')



@csrf_exempt
def withdrawpop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':

    		varuser = request.session['userid']
    		varerr =""
    		post = request.POST.copy()
    		acccode = post['userid']
    		year,repay,total=acccode.split(":")

    		return render(request,'IIIb/mywallet_withdraw_pop.html',{'year':year,'status':repay,'amount':total})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


def acctno(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)


		if request.method=='POST':
			bank = request.POST['bank']
			accct =request.POST['accct']

			try:
				mybank=tblIIIb_bankdetail.objects.get(branch=mybranch, staff=coop,bank_name=bank,account_number=accct)
			except:
				mybank=tblIIIb_bankdetail(branch=mybranch, staff=coop,bank_name=bank,account_number=accct).save()

			if staff.thrift3b_admin==1:
				return render(request,'IIIb/mywallet_myacc_post_a.html',{'company':mybranch,
					'user':varuser,
					'msg':coop,
					'amount':mybank})

			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/mywallet_myacc_post_c.html',{'company':mybranch,
					'user':varuser,
					'msg':coop,
					'amount':mybank})

			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/mywallet_myacc_post_o.html',{'company':mybranch,
					'user':varuser,
					'msg':coop,
				'amount':mybank})

		else:

			mybank=tblIIIb_bankdetail.objects.filter(branch=mybranch, staff=coop)

			if mybank.count() == 1:
				mybank = mybank.get()
				

				if staff.thrift3b_admin==1:
					return render(request,'IIIb/mywallet_myacc_fe_a.html',{'company':mybranch,
						'user':varuser,
						'msg':coop,
						'amount':mybank})

				elif staff.thrift3b_cashier==1:
					return render(request,'IIIb/mywallet_myacc_fe_c.html',{'company':mybranch,
						'user':varuser,
						'msg':coop,
						'amount':mybank})

				elif staff.thrift3b_officer==1:
					return render(request,'IIIb/mywallet_myacc_fe_o.html',{'company':mybranch,
						'user':varuser,
						'msg':coop,
					'amount':mybank})

			else:

				if staff.thrift3b_admin==1:
					return render(request,'IIIb/mywallet_myacc_ne_a.html',{'company':mybranch,
						'user':varuser,
						'msg':coop})

				elif staff.thrift3b_cashier==1:
					return render(request,'IIIb/mywallet_myacc_ne_c.html',{'company':mybranch,
						'user':varuser,
						'msg':coop})

				elif staff.thrift3b_officer==1:
					return render(request,'IIIb/mywallet_myacc_ne_o.html',{'company':mybranch,
						'user':varuser,
						'msg':coop})



	else:
		return HttpResponseRedirect('/login/user/')




# #************************my savings wallet schemes***********************
def wallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)


		coop = tblIIIbcoop.objects.get(staff=find_staff,status=1)

		ppp = tblstandardsavingIIIB.objects.filter(branch=mybranch,active=True,description='Wallet')



	
		tdate= date.today()
		month=tdate.month #index of current month
		monthnam=calendar.month_name[tdate.month]


		
		if request.method=='POST':
			package=request.POST['savepack']
			amount=request.POST['amount']
			year=request.POST['businessyear']

			fig = num2words(int(amount))

			nb = {'company':mybranch, 
				'user':varuser,
				'coop':coop,
				'package':package,
				'fig':fig.capitalize(),
				'amount':amount,
				'month':monthnam,
				'year':year}


			if staff.thrift3b_admin==1:

				return render(request,'IIIb/mysavings_wallet_apply_display.html',nb)

			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/mysavings_wallet_apply_display_c.html',nb)

			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/mysavings_wallet_apply_display_o.html',nb)
		else:
			
			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]

			b={'company':mybranch, 
					'user':varuser,
					'msg':coop,
					'package':ppp,'year':yy}


			if staff.thrift3b_admin==1:
				return render(request,'IIIb/mysavings_wallet_apply_a.html',b)

			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/mysavings_wallet_apply_c.html',b)


			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/mysavings_wallet_apply_o.html',b)
					

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def eliibility(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,package=acccode.split(":")

        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id


        		mybranch=tblBRANCH.objects.get(id=branch)


        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)
        		mnm=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		tdate=datetime.today()
        		month=tdate.month #month_index
        		
        		year=tdate.year

        		
        		if package== '-----':
        			msg='select a savings scheme'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})
        		elif package== 'null':
        			msg='Account not set. Contacgt the Admin'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})        			
        		else:
        			gh = tblstandardsavingIIIB.objects.get(branch=mybranch,	description=package)

        			starts_month_name = gh.from_month
        			starts_index= list(calendar.month_name).index(starts_month_name)



        			stopp_month_name = gh.to_month
        			stopp_index = list(calendar.month_name).index(stopp_month_name)




        			if month < starts_index:
        				msg = 'This scheme is not yet open'
        				return render(request,'IIIb/selectloan.html',{'msg':msg})
        			
        			elif month > stopp_index:
        				msg = "This scheme is closed"
        				return render(request,'IIIb/selectloan.html',{'msg':msg})

        			else:

        				status= ['Running','Completed']

	        			f = tblIIIIbassets_authorization.objects.filter(branch=mybranch,
	        				staff=mnm,description=package,year=year,status__in = status)

	        			if f.count() ==1:
	        				# f=f.get()
	        				return render(request,'IIIb/mysavings_wallet_apply_ajax.html',{'company':mybranch, 'package':package,'msg':f})
	        			
	        			elif f.count()== 0:
	        				rt = tblIIIbprorations.objects.filter(branch=mybranch,month = stopp_month_name, year=year)


	        				if rt.count() ==1:
	        					msg='This scheme is already closed'
	        					return render(request,'IIIb/selectloan.html',{'msg':msg})
	        				else: 
	        					msg = f"Appication for {package} scheme"
	        					return render(request,'IIIb/mysavings_wallet_applypack.html',{'msg':msg})
        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')




def create_wallet_pack(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



		tdate= date.today()

		
		if request.method=='POST':
			amount=request.POST['amount']
			scheme =request.POST['scheme']
			year =request.POST['year']
			authurization_month_name =request.POST['month']
			coop_id =request.POST['coop']

			kfwf=tblIIIbcoop.objects.get(id = coop_id,status=1)

		
			authurization_month_index = list(calendar.month_name).index(authurization_month_name) #index to name



			bg = tblstandardsavingIIIB.objects.get(branch=mybranch,description=scheme)
			package_end_month_name =bg.to_month #this is in month_name



			#converts month_name to month_index
			package_end_month_index = datetime.strptime(package_end_month_name,"%B") 
			package_end_month_index=package_end_month_index.month


			mmm = 0
			rt = tblIIIbprorations.objects.filter(branch=mybranch,status='Executed',year=year)

			mmm = rt.count() + mmm


			authurization_month_index=authurization_month_index + mmm

			if authurization_month_index > 12 :
				authurization_month_index =authurization_month_index - 12
				year = year + 1

			authurization_month_name = calendar.month_name[authurization_month_index]





			asset_code = generate_trans_pin()

			fld= tblIIIbprorations_schedule.objects.filter(branch = mybranch,
					year=year,status='Awaiting Execution',
					scheme=scheme,account_type='Assets')


			if not tblIIIIbassets_authorization.objects.filter(branch=mybranch,
							staff=kfwf,
							description=scheme,
							year=year,
							month=authurization_month_name,
							status='Running').exists():

				d=tblIIIIbassets_authorization.objects.create(branch=mybranch,
					staff=kfwf,
					description=scheme,
					status='Running',
					month=authurization_month_name,
					asset_authorization_code=asset_code,
					year=year,
					amount=amount,
					transdate=tdate)
			else:
				d=tblIIIIbassets_authorization.objects.get(branch=mybranch,
					staff=kfwf,
					description=scheme,
					status='Running',
					month=authurization_month_name,
					year=year)
				


			if authurization_month_name == package_end_month_name: #month is current month, month4 is 
				msg='This scheme is no longer open'
				return render(request,'IIIb/selectloan.html',{'msg':msg})



			bg = []
			for x in range(authurization_month_index,package_end_month_index + 1):
				monthname = calendar.month_name[x]
				bg.append(monthname)

				code = generate_trans_pin()

				sls = fld.filter(staff =kfwf,month=monthname,account_type='Assets')

				if sls.count() == 0:
					tblIIIbprorations_schedule.objects.create(staff =kfwf,
						branch = mybranch,
						month=monthname,
						amount=amount,
						year=year,
						transID=code,
						status='Awaiting Execution',
						authorization_code=d.asset_authorization_code,
						scheme=scheme,
						account_type='Assets',
						transdate=tdate)


				#**configure email sending***********

			try:
				savingscheme_email(mybranch,varuser,surname,firstname,amount,year,package,bg[0],bg[-1])
			except:
				pl=0

			cv = {'company':mybranch, 'user':varuser, 'package':scheme}

			if staff.thrift3b_admin==1:
				return render(request,'IIIb/mysavings_wallet_success_a.html',cv)

			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/mysavings_wallet_success_c.html',cv)

			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/mysavings_wallet_success_o.html',cv)

		else:
			return HttpResponseRedirect('/IIIb/threeb/savings/wallet_packages/')
	else:
		return HttpResponseRedirect('/login/user/')






@csrf_exempt
def editsavepop(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
        		mnm=tblIIIbcoop.objects.get(staff=memstaff,status=1)


        		tdate= date.today()
        		year=tdate.year


        		sd =tblIIIIbassets_authorization.objects.filter(description=acccode,status='Running',staff=mnm,year=year)
        		
        		if sd.count() == 0:
        			return render(request,'IIIb/mysavingks_log_ajax.html',{'branch':mybranch,'email':varuser})
        		
        		else:
        			sd=sd.get()
        			return render(request,'IIIb/mysavings_pop.html',{'branch':mybranch,'email':varuser,'sd':sd,'package':acccode})
        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render(request,'lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/user/')



def editsave(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,status=1)


		tdate= date.today()
		year=tdate.year
	

		if request.method=='POST':


			package=request.POST['package']
			new=request.POST['new']

			sd =tblIIIIbassets_authorization.objects.filter(description=package,status='Running',staff=coop,year=year)

			sd.update(amount=new)

			pro = tblIIIbprorations_schedule.objects.filter(branch=mybranch,staff=coop,year=year,
						account_type='Assets',
						scheme=package,
						status='Awaiting Execution')

			pro.update(amount=new)


			if package == 'Wallet':
				return HttpResponseRedirect('/IIIb/threeb/savings/wallet_packages/')
			else:
				return HttpResponseRedirect('/IIIb/threeb/savings/save_packages/')
			
		else:
			return HttpResponseRedirect('/dashboard /')

	else:
		return HttpResponseRedirect('/login/user/')


# #************************my savings schemes***********************
def safepack(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,status=1)


		ppp = tblstandardsavingIIIB.objects.filter(branch=mybranch,active=True).exclude(description='Wallet')
		

		tdate= date.today()
		month=tdate.month #index of current month
		monthnam=calendar.month_name[tdate.month]


		if request.method=='POST':


			package=request.POST['savepack']
			amount=request.POST['amount']
			year=request.POST['businessyear']

			fig = num2words(int(amount)).capitalize()


			g= {'company':mybranch, 
					'user':varuser,
					'coop':coop,
					'package':package,
					'fig':fig,
					'month':monthnam,
					'year':year,
					'amount':amount}
			
			if staff.thrift3b_admin==1:

				return render(request,'IIIb/mysavings_savingscheme_display.html',g)

			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/mysavings_savingscheme_display_c.html',g)

			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/mysavings_savingscheme_display_o.html',g)
		else:
			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]
			
			vv={'company':mybranch, 
				'user':varuser,
				'msg':coop,
				'year':yy,
				'package':ppp}

			
			if staff.thrift3b_admin==1:


				return render(request,'IIIb/mysavings_savingscheme_apply.html',vv)

			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/mysavings_savingscheme_apply_c.html',vv)

			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/mysavings_savingscheme_apply_o.html',vv)

	else:
		return HttpResponseRedirect('/login/user/')



def save_pack_ori(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



		tdate= date.today()

		
		if request.method=='POST':
			amount=request.POST['amount']
			scheme =request.POST['scheme']
			year =request.POST['year']
			authurization_month_name =request.POST['month']
			coop_id =request.POST['coop']

			kfwf=tblIIIbcoop.objects.get(id = coop_id,status=1)

		
			authurization_month_index = list(calendar.month_name).index(authurization_month_name) #name from index



			bg = tblstandardsavingIIIB.objects.get(branch=mybranch,description=scheme)
			package_end_month_name =bg.to_month #this is in month_name



			#converts month_name to month_index
			package_end_month_index = datetime.strptime(package_end_month_name,"%B") 
			package_end_month_index=package_end_month_index.month


			mmm = 0
			rt = tblIIIbprorations.objects.filter(branch=mybranch,status='Executed',year=year)

			mmm = rt.count() + mmm


			authurization_month_index=authurization_month_index + mmm

			if authurization_month_index > 12 :
				authurization_month_index =authurization_month_index - 12
				year = year + 1

			authurization_month_name = calendar.month_name[authurization_month_index]



			asset_authorization_code = generate_trans_pin()

			fld= tblIIIbprorations_schedule.objects.filter(branch = mybranch,
					year=year,status='Awaiting Execution',
					scheme=scheme,account_type='Assets')


			if not tblIIIIbassets_authorization.objects.filter(branch=mybranch,
							staff=kfwf,
							description=scheme,
							year=year,
							month=authurization_month_name,
							status='Running').exists():

				d=tblIIIIbassets_authorization.objects.create(branch=mybranch,
					staff=kfwf,
					description=scheme,
					status='Running',
					month=authurization_month_name,
					asset_authorization_code=asset_authorization_code,
					year=year,
					amount=amount,
					transdate=tdate)
			else:
				d=tblIIIIbassets_authorization.objects.get(branch=mybranch,
					staff=kfwf,
					description=scheme,
					status='Running',
					month=authurization_month_name,
					year=year)
				




			if authurization_month_name == package_end_month_name: #month is current month, month4 is 
				msg='This scheme is no longer open'
				return render(request,'IIIb/selectloan.html',{'msg':msg})


			bg = []
			for x in range(authurization_month_index,package_end_month_index + 1):
				monthname = calendar.month_name[x]
				bg.append(monthname)

				code = generate_trans_pin()

				sls = fld.filter(staff =kfwf,month=monthname,account_type='Assets')

				if sls.count() == 0:
					tblIIIbprorations_schedule.objects.create(staff =kfwf,
						branch = mybranch,
						month=monthname,
						amount=amount,
						year=year,
						transID=code,
						status='Awaiting Execution',
						authorization_code=d.asset_authorization_code,
						scheme=scheme,
						account_type='Assets',
						transdate=tdate)


				#**configure email sending***********

			try:
				savingscheme_email(mybranch,varuser,kfwf,amount,year,scheme,bg[0],bg[-1])
			except:
				pl=0

			cv = {'company':mybranch, 'user':varuser, 'package':scheme}

			if staff.thrift3b_admin==1:
				return render(request,'IIIb/mysavings_savings_schemee_success_a.html',cv)

			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/mysavings_savings_schemee_success_c.html',cv)

			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/mysavings_savings_schemee_success_o.html',cv)

		else:
			return HttpResponseRedirect('/IIIb/threeb/savings/save_packages/')
	else:
		return HttpResponseRedirect('/login/user/')

def save_pack(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)



		tdate= date.today()

		

		if request.method == 'POST':
		    amount = request.POST['amount']
		    scheme = request.POST['scheme']
		    year = int(request.POST['year'])
		    auth_month_name = request.POST['month']
		    coop_id = request.POST['coop']

		    kfwf = tblIIIbcoop.objects.get(id=coop_id, status=1)

		    # Precompute month mapping
		    month_map = {m: i for i, m in enumerate(calendar.month_name) if m}
		    auth_month_index = month_map[auth_month_name]

		    bg = tblstandardsavingIIIB.objects.get(branch=mybranch, description=scheme)
		    package_end_month_index = datetime.strptime(bg.to_month, "%B").month

		    # Count executed prorations once
		    executed_count = tblIIIbprorations.objects.filter(branch=mybranch, status='Executed', year=year).count()
		    auth_month_index += executed_count

		    if auth_month_index > 12:
		        auth_month_index -= 12
		        year += 1

		    auth_month_name = calendar.month_name[auth_month_index]
		    asset_code = generate_trans_pin()

		    # Use get_or_create instead of exists + get/create
		    d, created = tblIIIIbassets_authorization.objects.get_or_create(
		        branch=mybranch,
		        staff=kfwf,
		        description=scheme,
		        month=auth_month_name,
		        year=year,
		        defaults={
		            'status': 'Running',
		            'asset_authorization_code': asset_code,
		            'amount': amount,
		            'transdate': tdate
		        }
		    )

		    # Early exit if scheme closed
		    if auth_month_name == bg.to_month:
		        msg = 'This scheme is no longer open'
		        return render(request, 'IIIb/selectloan.html', {'msg': msg})

		    # Fetch schedule records once
		    fld = tblIIIbprorations_schedule.objects.filter(
		        branch=mybranch,
		        year=year,
		        status='Awaiting Execution',
		        scheme=scheme,
		        account_type='Assets'
		    )

		    # Precompute month names
		    months = [calendar.month_name[x] for x in range(auth_month_index, package_end_month_index + 1)]

		    # Bulk create missing schedules
		    new_entries = []
		    for monthname in months:
		        if not fld.filter(staff=kfwf, month=monthname).exists():
		            new_entries.append(tblIIIbprorations_schedule(
		                staff=kfwf,
		                branch=mybranch,
		                month=monthname,
		                amount=amount,
		                year=year,
		                transID=generate_trans_pin(),
		                status='Awaiting Execution',
		                authorization_code=d.asset_authorization_code,
		                scheme=scheme,
		                account_type='Assets',
		                transdate=tdate
		            ))

		    if new_entries:
		        tblIIIbprorations_schedule.objects.bulk_create(new_entries)



		    try:
		     	savingscheme_email(mybranch,varuser,kfwf,amount,year,scheme,bg[0],bg[-1])
		    except:
		    	pl=0

		    cv = {'company':mybranch, 'user':varuser, 'package':scheme}


		    if staff.thrift3b_admin==1:
		    	return render(request,'IIIb/mysavings_savings_schemee_success_a.html',cv)

		    elif staff.thrift3b_cashier==1:
		    	return render(request,'IIIb/mysavings_savings_schemee_success_c.html',cv)

		    elif staff.thrift3b_officer==1:
		    	return render(request,'IIIb/mysavings_savings_schemee_success_o.html',cv)

		else:
			return HttpResponseRedirect('/IIIb/threeb/savings/save_packages/')
	else:
		return HttpResponseRedirect('/login/user/')


# #************************my savings log***********************
def savelog(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,status=1)
		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]

		vx = {'company':mybranch, 'user':varuser,'msg':coop,'year':yy}
		
		if staff.thrift3b_admin==1:
			return render(request,'IIIb/mysavings_log_a.html',vx)
		elif staff.thrift3b_cashier==1:
			return render(request,'IIIb/mysavings_log_c.html',vx)
		elif staff.thrift3b_officer==1:
			return render(request,'IIIb/mysavings_log_o.html',vx)

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def deplogs(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,status=acccode.split(":")

        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
        		mnm=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if status== '-----':
        			msg='select transaction type'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})
        		else:


        			month_order = Case(
					    When(month='January', then=Value(1)),
					    When(month='February', then=Value(2)),
					    When(month='March', then=Value(3)),
					    When(month='April', then=Value(4)),
					    When(month='May', then=Value(5)),
					    When(month='June', then=Value(6)),
					    When(month='July', then=Value(7)),
					    When(month='August', then=Value(8)),
					    When(month='September', then=Value(9)),
					    When(month='October', then=Value(10)),
					    When(month='November', then=Value(11)),
					    When(month='December', then=Value(12)),
					    output_field=IntegerField(),)


        			req = tblIIIbprorations_schedule.objects.filter(
					    branch=mybranch,
					    staff=mnm,
					    account_type='Assets',
					    year=year,
					    status=status).order_by(month_order)




        			return render(request,'IIIb/mysavings_log_ajax.html',{'branch':mybranch,'email':varuser,'req':req})
        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render(request,'lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/user/')



def walletupload(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)



		if staff.ceo == 0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			excel_file = request.FILES['excel']
			
			myusers=tblSTAFF.objects.filter(branch=mybranch)
			lg= Userprofile.objects.filter(branch=mybranch, status=1)

			address='lagos'

			photo = 'staff-pix/user.png'


			#Expected columns: s/n, email, wallet, christmass

			for _, row in df.iterrows():
				serial_no = row.get('s/n')
				email = row.get('email')
				wallet = row.get('Wallet')
				christmass = row.get('Christmas Savings')

				amount=row.get('Wallet')
				scheme ='Wallet'
				year = 2026
				authurization_month_name = 'September'

				coop_id =request.POST['coop']


				kfwf=tblIIIbcoop.objects.get(staff__email=email)


				authurization_month_index = list(calendar.month_name).index(authurization_month_name) #index to name

				scheme = 'Wallet'

				bg = tblstandardsavingIIIB.objects.get(branch=mybranch,description=scheme)
				package_end_month_name =bg.to_month #this is in month_name


				#converts month_name to month_index

				package_end_month_index = datetime.strptime(package_end_month_name,"%B") 

				package_end_month_index=package_end_month_index.month





				mmm = 0
				rt = tblIIIbprorations.objects.filter(branch=mybranch,status='Executed',year=year)

				mmm = rt.count() + mmm




				authurization_month_index=authurization_month_index + mmm

				if authurization_month_index > 12 :
					authurization_month_index =authurization_month_index - 12
					year = year + 1


					authurization_month_name = calendar.month_name[authurization_month_index]



					asset_code = generate_trans_pin()


					fld= tblIIIbprorations_schedule.objects.filter(branch = mybranch,
					year=year,status='Awaiting Execution',
					scheme=scheme,account_type='Assets')



				if not tblIIIIbassets_authorization.objects.filter(branch=mybranch,
								staff=kfwf,
								description=scheme,
								year=year,
								month=authurization_month_name,
								status='Running').exists():

					d=tblIIIIbassets_authorization.objects.create(branch=mybranch,
						staff=kfwf,
						description=scheme,
						status='Running',
						month=authurization_month_name,
						asset_authorization_code=asset_code,
						year=year,
						amount=amount,
						transdate=tdate)

				else:
					d=tblIIIIbassets_authorization.objects.get(branch=mybranch,
						staff=kfwf,
						description=scheme,
						status='Running',
						month=authurization_month_name,
						year=year)


				if authurization_month_name == package_end_month_name: #month is current month, month4 is
					msg='This scheme is no longer open'
					return render(request,'IIIb/selectloan.html',{'msg':msg})



				bg = []
				for x in range(authurization_month_index,package_end_month_index + 1):
					monthname = calendar.month_name[x]
					bg.append(monthname)

					code = generate_trans_pin()

					sls = fld.filter(staff =kfwf,month=monthname,account_type='Assets')

					if sls.count() == 0:
						tblIIIbprorations_schedule.objects.create(staff =kfwf,
							branch = mybranch,
							month=monthname,
							amount=amount,
							year=year,
							transID=code,
							status='Awaiting Execution',
							authorization_code=d.asset_authorization_code,
							scheme=scheme,
							account_type='Assets',
							transdate=tdate)


				#**configure email sending***********


				try:
					savingscheme_email(mybranch,varuser,surname,firstname,amount,year,package,bg[0],bg[-1])
				except:
					pl=0


                # Example: insert into your model
				tblIIIIbassets_authorization.objects.create(
                    staff_email=email,
                    wallet=wallet,
                    description="Christmas Savings",
                    status="Running",
                    month="December",
                    asset_authorization_code=f"AUTH-{serial_no}",
                    year=2026,
                    amount=christmass)




			messages.success(request, f"  Data uploaded successfully.")
			
			return redirect(massReg) #function redirect,name redirect,url redirect
			# return redirect('success_page')

			return render(request, 'upload.html')



			return render(request,'staff/success.html',{'company':mybranch,'user':varuser,'email':email})



		if staff.thrift3b==1:
			return render(request,'IIIb/mysavings_upload.html',{'company':mybranch, 'user':varuser,'msg':msg})
		else:
			return render(request,'staff/massreg.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')

# #**********************My LOANs**************************************

def reqloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)


		if staff.thrift3b_officer == 0 :
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})


		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		cid=coop.id
		surname=coop.staff.surname
		firstname=coop.staff.firstname
		cop_man = Userprofile.objects.get(branch=mybranch,thrift3b_admin=1)
		cop_man = f"{cop_man.staffrec.surname}  {cop_man.staffrec.firstname}"



		amount=walletbalance(mybranch,coop) #***********************####  ACCOUNT BALANCE************************

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


		vgg = {'company':mybranch,'name':find_staff,'user':varuser,'year':yy}


		if amount ==0 :
			vgg['msg'] =' Your wallet is empty.'
			
			if staff.thrift3b_admin==1:
				return render(request,'IIIb/myloans_apply_a1.html',vgg)
			
			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/myloans_apply_c1.html',vgg)
			else:
				return render(request,'IIIb/myloans_apply_o1.html',vgg)




		mmx =tblmaxloanIIIB.objects.filter(branch=mybranch) ##**************###MAX LOAN***********************
		if mmx.count() == 0:
			vgg['msg']='maximum loan limit not set. Contact the manager'
			return render(request,'IIIb/myloans_apply_limit.html',vgg)

		mmx=mmx.get()
		mx_loan = mmx.value
		mx_loan=int(mx_loan)
		mx_loan=mx_loan * amount / 100
		mx_loan= int(round(mx_loan,2))


		applyy  = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch)	

		mycoop = [a.id for a in applyy.filter(staff =coop)]

		if len(mycoop) > 0:
			app = applyy.filter(staff=coop, id=mycoop[-1])
			app2 = app.get()
			status = app2.status
		else:
			status=0
			app=0


		if request.method == 'POST':

			total_repayment=request.POST['repayment']
			principal= request.POST['principal']
			package=request.POST['package']
			grace_period=request.POST['grace_period']
			interest=request.POST['interest']
			monthly_deduction=request.POST['monthly_deduction']

			fdate= datetime.today()
			month=fdate.month
			current_month_index=fdate.month
			year=fdate.year

			todayy=date(fdate.year,fdate.month,fdate.day)

			loan_package = tblstandardloanIIIB.objects.get(description=package, branch=mybranch)

			month_name = calendar.month_name[current_month_index]


			if current_month_index > 12:
				current_month_index = current_month_index - 12
				year=year + 1


			current_month_name =calendar.month_name[current_month_index]


			code=generate_trans_pin()


			lloan = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,staff=coop,status='Awaiting Approval')
			
			if lloan.count() ==0:

				app = tblIIIIbliabilities_authorization.objects.create(branch=mybranch,
							staff=coop,
							package=loan_package,
							application_date =todayy,
							status='Awaiting Approval',
							year=year,
							approval_date=fdate,
							disbursal_date=fdate,							
							principal=principal,
							thrift=monthly_deduction,
							interest=interest,
							total_repayment=total_repayment,
							grace_period= grace_period,
							application_code=code,description='Loan')


			
			try: ##********Sending email notifications*************
				loanbook_email(mybranch,varuser,surname,firstname,amount,cop_man)
			except:
				pl=0


			gg ={'company':mybranch, 'user':varuser,'customer':0}

			if staff.thrift3b_admin==1:
				return render(request,'IIIb/myloans_post_a.html',gg)
			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/myloans_post_c.html',gg)
			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/myloans_post_o.html',gg )

		else:
			msg=''
			loans =  tblstandardloanIIIB.objects.filter(branch=mybranch, status=True)

			if loans.count() == 0:
				vgg['msg']='loan types not set. Contact the manager'
				return render(request,'IIIb/myloans_apply_limit.html',vgg)
			
			vv={'company':mybranch,
				'name':find_staff,
				'user':varuser,
				'max' :mx_loan,
				'loan':loans,
				'amount':amount,
				'year':yy,
				'msg':msg,
				'myloan':app}				


			if status == 'Awaiting Approval' or status == 'Declined' or status =='Awaiting Disbursal' or status == 'Running':
				if status == 'Running': 
					vv['msg'] = f" You have a {status} loan"
				else:
					vv['msg']=f"Your application is {status}"


				if staff.thrift3b_admin==1:
					return render(request,'IIIb/myloans_apply_a1.html',vv)
				elif staff.thrift3b_cashier==1:
					return render(request,'IIIb/myloans_apply_c1.html',vv)
				elif staff.thrift3b_officer == 1:
					return render(request,'IIIb/myloans_apply_o1.html',vv)
			else:

				if staff.thrift3b_admin==1:
					return render(request,'IIIb/myloans_apply_a.html',vv)
				elif staff.thrift3b_cashier==1:
					return render(request,'IIIb/myloans_apply_c.html',vv)
				elif staff.thrift3b_officer == 1:
					return render(request,'IIIb/myloans_apply_o.html',vv)

					
	else:
		return HttpResponseRedirect('/login/user/')

@csrf_exempt
def getstandardloan(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				# post = request.POST.copy()
				# acccode = post['userid']

				staff = Userprofile.objects.get(email=varuser,status=1)
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompay=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(id=branch)
				t1= tblstandardloanIIIB.objects.filter(branch=mybranch)
				sdic={}
				kk=[]

				for j in t1:
					j = j.description
					s = {j:j}
					sdic.update(s)
					klist = sdic.values()
				for p in klist:
					kk.append(p)
				kk.sort()
			else :
				kk.append('NO LOAN PACKAGES FOUND')
			
			return HttpResponse(json.dumps(kk), content_type='application/json')
		else:
			gdata = ""
			return render(request,'index.html',{'gdata':gdata})




@csrf_exempt
def loandetails(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		maxi,loan_package,principal=acccode.split(":")

        		

        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id


        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
        		memstaff = tblIIIbcoop.objects.get(staff=memstaff,branch=mybranch,status=1)

        		if principal== '':
        			msg='enter loan amount'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})
        			
        		elif loan_package == '-----':
        			msg='select a loan package'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})


        		

        		if float(principal) <= float(maxi) :
        			det = tblstandardloanIIIB.objects.get(description=loan_package, branch=mybranch)

        			loan_rate = int(det.rate)
        			principal=int(principal)
        			duration = int(det.tenure)

        			thrift  = (100 + loan_rate )
        			thrift = thrift / 100

        			repayment = round(thrift * principal ,2)
        			repayment_words = num2words(int(repayment)).capitalize()


        			monthly_deduction=  repayment / duration
        			monthly_deduction = round(monthly_deduction, 2)
        			monthly_deduction_word = num2words(int(monthly_deduction)).capitalize()

        			interest= round(repayment - principal,2)
        			interest_words = num2words(int(interest)).capitalize()


        			# return render(request,'IIIb/selectloan.html',{'msg':loank})

        

        			return render(request,'IIIb/myloans_view_ajax.html',{'company':mybranch,
						'principal':principal,
						'loan':loan_package,
						'lending_rate':loan_rate,
						'repayment':repayment,'repayment_words':repayment_words,
						'duration':duration,'thrift':thrift,
						'interest':interest,'interest_words':interest_words,
						'monthly_deduction':monthly_deduction,'monthly_deduction_word':monthly_deduction_word})

        		else:

        			msg = ' You have exceeded your permisible volume. To proceed, kindly reduce the amount'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})

        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render(request,'lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/user/')


def loanperformance(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		find_staff = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)


		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]

		p=[]

		allloan= tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,staff=find_staff)
		dp=[a.id for a in allloan]




		if len(dp)>0:


			loanss=allloan.get(id=dp[-1])
			if loanss.status == 'Awaiting Approval':
				return redirect(loanhistory)
				
			
			else:
				loan_detail =  tblIIIbprorations_schedule.objects.filter( branch=mybranch,
					account_type='Liabilities',authorization_code=loanss.application_code,
					staff=find_staff)

				cc = loan_detail.filter(status='Awaiting Execution')
				

				tt=cc.aggregate(Sum('amount'))
				total = tt['amount__sum']

				# return render(request,'IIIb/selectloan.html',{'msg':loan_detail})

		else:
			loan_detail=[]
			total=0

		

		gh={'p':loan_detail,'company':mybranch,'name':find_staff,'user':varuser,'year':yy,'total':total}

		if staff.thrift3b_admin==1:
			return render(request,'IIIb/myloans_performance_a.html',gh)

		elif staff.thrift3b_cashier == 1 :
			return render(request,'IIIb/myloans_performance_c.html',gh)
		
		elif staff.thrift3b_officer == 1 :
			return render(request,'IIIb/myloans_performance_o.html',gh)



	else:
		return HttpResponseRedirect('/login/user/')

def loanhistory(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		find_staff = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		loan_list = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,staff=find_staff)

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]
		df= {'company':mybranch,'name':find_staff,'user':varuser,'list':loan_list,'year':yy}

		if staff.thrift3b_admin==1:
				return render(request,'IIIb/myloans_log_a.html',df)
		
		elif staff.thrift3b_cashier==1:
			return render(request,'IIIb/myloans_log_c.html',df)
		
		elif staff.thrift3b_officer==1:
			return render(request,'IIIb/myloans_log_o.html',df)

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def editloanpop(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
        		mnm=tblIIIbcoop.objects.get(staff=memstaff,status=1)


        		sd =tblIIIIbliabilities_authorization.objects.get(application_code=acccode)
        		return render(request,'IIIb/myloans_edit_pop.html',{'branch':mybranch,'email':varuser,'sd':sd,'application_code':acccode})
        	
        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render(request,'lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/user/')


def delloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,status=1)
	

		if request.method=='POST':

			application_code=request.POST['application_code']
			# new=request.POST['new']

			sd =tblIIIIbliabilities_authorization.objects.filter(application_code=application_code)
			sd.delete()

			return HttpResponseRedirect('/IIIb/threeb/staff/request_loan/')

			
		else:
			return HttpResponseRedirect('/dashboard /')

	else:
		return HttpResponseRedirect('/login/user/')




# #**********************My Commodities**************************************

def reqcomm(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)


		if staff.thrift3b_officer == 0 :
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})


		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		cid=coop.id
		surname=coop.staff.surname
		firstname=coop.staff.firstname
		cop_man = Userprofile.objects.get(branch=mybranch,thrift3b_admin=1)
		cop_man = f"{cop_man.staffrec.surname}  {cop_man.staffrec.firstname}"



		amount=walletbalance(mybranch,coop) #***********************####  ACCOUNT BALANCE************************

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


		vgg = {'company':mybranch,'name':find_staff,'user':varuser,'year':yy}


		if amount ==0 :
			vgg['msg'] =' Your wallet is empty.'
			
			if staff.thrift3b_admin==1:
				return render(request,'IIIb/myloans_apply_a1.html',vgg)
			
			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/myloans_apply_c1.html',vgg)
			else:
				return render(request,'IIIb/myloans_apply_o1.html',vgg)




		mmx =tblmaxloanIIIB.objects.filter(branch=mybranch) ##**************###MAX LOAN***********************
		if mmx.count() == 0:
			vgg['msg']='maximum loan limit not set. Contact the manager'
			return render(request,'IIIb/myloans_apply_limit.html',vgg)

		mmx=mmx.get()
		mx_loan = mmx.value
		mx_loan=int(mx_loan)
		mx_loan=mx_loan * amount / 100
		mx_loan= int(round(mx_loan,2))


		applyy  = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch)	

		mycoop = [a.id for a in applyy.filter(staff =coop)]

		if len(mycoop) > 0:
			app = applyy.filter(staff=coop, id=mycoop[-1])
			app2 = app.get()
			status = app2.status
		else:
			status=0
			app=0


		if request.method == 'POST':

			total_repayment=request.POST['repayment']
			principal= request.POST['principal']
			package=request.POST['package']
			grace_period=request.POST['grace_period']
			interest=request.POST['interest']
			monthly_deduction=request.POST['monthly_deduction']

			fdate= datetime.today()
			month=fdate.month
			current_month_index=fdate.month
			year=fdate.year

			todayy=date(fdate.year,fdate.month,fdate.day)

			loan_package = tblstandardloanIIIB.objects.get(description=package, branch=mybranch)

			month_name = calendar.month_name[current_month_index]


			if current_month_index > 12:
				current_month_index = current_month_index - 12
				year=year + 1


			current_month_name =calendar.month_name[current_month_index]


			code=generate_trans_pin()


			lloan = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,staff=coop,status='Awaiting Approval')
			
			if lloan.count() ==0:

				app = tblIIIIbliabilities_authorization.objects.create(branch=mybranch,
							staff=coop,
							package=loan_package,
							application_date =todayy,
							status='Awaiting Approval',
							year=year,
							approval_date=fdate,
							disbursal_date=fdate,							
							principal=principal,
							thrift=monthly_deduction,
							interest=interest,
							total_repayment=total_repayment,
							grace_period= grace_period,
							application_code=code,description='Loan')


			
			try: ##********Sending email notifications*************
				loanbook_email(mybranch,varuser,surname,firstname,amount,cop_man)
			except:
				pl=0


			gg ={'company':mybranch, 'user':varuser,'customer':0}

			if staff.thrift3b_admin==1:
				return render(request,'IIIb/myloans_post_a.html',gg)
			elif staff.thrift3b_cashier==1:
				return render(request,'IIIb/myloans_post_c.html',gg)
			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/myloans_post_o.html',gg )

		else:
			msg=''
			loans =  tblstandardloanIIIB.objects.filter(branch=mybranch, status=True)

			if loans.count() == 0:
				vgg['msg']='loan types not set. Contact the manager'
				return render(request,'IIIb/myloans_apply_limit.html',vgg)
			
			vv={'company':mybranch,
				'name':find_staff,
				'user':varuser,
				'max' :mx_loan,
				'loan':loans,
				'amount':amount,
				'year':yy,
				'msg':msg,
				'myloan':app}				


			if status == 'Awaiting Approval' or status == 'Declined' or status =='Awaiting Disbursal' or status == 'Running':
				if status == 'Running': 
					vv['msg'] = f" You have a {status} loan"
				else:
					vv['msg']=f"Your application is {status}"

				if staff.thrift3b_admin==1:
					return render(request,'IIIb/mycommodities_apply_a1.html',vv)
				elif staff.thrift3b_cashier==1:
					return render(request,'IIIb/mycommodities_apply_c1.html',vv)
				elif staff.thrift3b_officer == 1:
					return render(request,'IIIb/mycommodities_apply_o1.html',vv)
			else:

				if staff.thrift3b_admin==1:
					return render(request,'IIIb/mycommodities_apply_a.html',vv)
				elif staff.thrift3b_cashier==1:
					return render(request,'IIIb/mycommodities_apply_c.html',vv)
				elif staff.thrift3b_officer == 1:
					return render(request,'IIIb/mycommodities_apply_o.html',vv)

					
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def getstandardloan(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				# post = request.POST.copy()
				# acccode = post['userid']

				staff = Userprofile.objects.get(email=varuser,status=1)
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompay=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(id=branch)
				t1= tblstandardloanIIIB.objects.filter(branch=mybranch)
				sdic={}
				kk=[]

				for j in t1:
					j = j.description
					s = {j:j}
					sdic.update(s)
					klist = sdic.values()
				for p in klist:
					kk.append(p)
				kk.sort()
			else :
				kk.append('NO LOAN PACKAGES FOUND')
			
			return HttpResponse(json.dumps(kk), content_type='application/json')
		else:
			gdata = ""
			return render(request,'index.html',{'gdata':gdata})




@csrf_exempt
def loandetails(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		maxi,loan_package,principal=acccode.split(":")

        		

        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id


        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
        		memstaff = tblIIIbcoop.objects.get(staff=memstaff,branch=mybranch,status=1)

        		if principal== '':
        			msg='enter loan amount'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})
        			
        		elif loan_package == '-----':
        			msg='select a loan package'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})


        		

        		if float(principal) <= float(maxi) :
        			det = tblstandardloanIIIB.objects.get(description=loan_package, branch=mybranch)

        			loan_rate = int(det.rate)
        			principal=int(principal)
        			duration = int(det.tenure)

        			thrift  = (100 + loan_rate )
        			thrift = thrift / 100

        			repayment = round(thrift * principal ,2)
        			repayment_words = num2words(int(repayment)).capitalize()


        			monthly_deduction=  repayment / duration
        			monthly_deduction = round(monthly_deduction, 2)
        			monthly_deduction_word = num2words(int(monthly_deduction)).capitalize()

        			interest= round(repayment - principal,2)
        			interest_words = num2words(int(interest)).capitalize()


        			# return render(request,'IIIb/selectloan.html',{'msg':loank})

        

        			return render(request,'IIIb/myloans_view_ajax.html',{'company':mybranch,
						'principal':principal,
						'loan':loan_package,
						'lending_rate':loan_rate,
						'repayment':repayment,'repayment_words':repayment_words,
						'duration':duration,'thrift':thrift,
						'interest':interest,'interest_words':interest_words,
						'monthly_deduction':monthly_deduction,'monthly_deduction_word':monthly_deduction_word})

        		else:

        			msg = ' You have exceeded your permisible volume. To proceed, kindly reduce the amount'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})

        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render(request,'lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/user/')


def loanperformance(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		find_staff = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)


		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]

		p=[]

		allloan= tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,staff=find_staff)
		dp=[a.id for a in allloan]




		if len(dp)>0:


			loanss=allloan.get(id=dp[-1])
			if loanss.status == 'Awaiting Approval':
				return redirect(loanhistory)
				
			
			else:
				loan_detail =  tblIIIbprorations_schedule.objects.filter( branch=mybranch,
					account_type='Liabilities',authorization_code=loanss.application_code,
					staff=find_staff)

				cc = loan_detail.filter(status='Awaiting Execution')
				

				tt=cc.aggregate(Sum('amount'))
				total = tt['amount__sum']

				# return render(request,'IIIb/selectloan.html',{'msg':loan_detail})

		else:
			loan_detail=[]
			total=0

		

		gh={'p':loan_detail,'company':mybranch,'name':find_staff,'user':varuser,'year':yy,'total':total}

		if staff.thrift3b_admin==1:
			return render(request,'IIIb/myloans_performance_a.html',gh)

		elif staff.thrift3b_cashier == 1 :
			return render(request,'IIIb/myloans_performance_c.html',gh)
		
		elif staff.thrift3b_officer == 1 :
			return render(request,'IIIb/myloans_performance_o.html',gh)



	else:
		return HttpResponseRedirect('/login/user/')

def loanhistory(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		find_staff = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)
		loan_list = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,staff=find_staff)

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]
		df= {'company':mybranch,'name':find_staff,'user':varuser,'list':loan_list,'year':yy}

		if staff.thrift3b_admin==1:
				return render(request,'IIIb/myloans_log_a.html',df)
		
		elif staff.thrift3b_cashier==1:
			return render(request,'IIIb/myloans_log_c.html',df)
		
		elif staff.thrift3b_officer==1:
			return render(request,'IIIb/myloans_log_o.html',df)

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def editloanpop(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
        		mnm=tblIIIbcoop.objects.get(staff=memstaff,status=1)


        		sd =tblIIIIbliabilities_authorization.objects.get(application_code=acccode)
        		return render(request,'IIIb/myloans_edit_pop.html',{'branch':mybranch,'email':varuser,'sd':sd,'application_code':acccode})
        	
        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

        else:
        	getdetails = tblcontents.objects.filter(topic=id)
        	return render(request,'lesson/entersub.html',{'gdata':getdetails})
    else:
    	return HttpResponseRedirect('/login/user/')


def delloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,status=1)
	

		if request.method=='POST':

			application_code=request.POST['application_code']
			# new=request.POST['new']

			sd =tblIIIIbliabilities_authorization.objects.filter(application_code=application_code)
			sd.delete()

			return HttpResponseRedirect('/IIIb/threeb/staff/request_loan/')

			
		else:
			return HttpResponseRedirect('/dashboard /')

	else:
		return HttpResponseRedirect('/login/user/')

#########PRORATIONS*************************

def proration_ori(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


		if request.method == 'POST':
			current_month_index =int(request.POST['month_index'])
			year =request.POST['year']

		
			month_name = calendar.month_name[current_month_index]

			fdate=date.today()



			stan_save = tblstandardsavingIIIB.objects.filter(branch=mybranch)



			coop=tblIIIbcoop.objects.filter(branch=mybranch,status=1)
		
			sss= tblIIIbsavingsaccount.objects.filter(branch=mybranch,month=month_name,year=year)


			all_prorations  = tblIIIbprorations.objects.filter(branch=mybranch, year=year,status='Executed')

			prorated_months=[a.month for a in all_prorations] #month_name

			prorated_months_indexes = sorted([list(calendar.month_name).index(m.capitalize()) for m in prorated_months])



			if not prorated_months:
				last_month_index=0
			else:#
				last_month_index = prorated_months_indexes[-1]

			pro_diff =   current_month_index - int(last_month_index )


			allsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch,	month=month_name,	year=year)
			

			awaiting = allsenario.filter(status='Awaiting Execution')

			if awaiting.count() > 0:

				if pro_diff == 1 or pro_diff == current_month_index:

					tt=awaiting.aggregate(Sum('amount'))
					total = tt['amount__sum']


					for k in awaiting:
						coopy = coop.get(id = k.staff.id)

						ds = sss.filter(account_code=k.authorization_code,status='CR')

						if ds.count() == 0:
							tblIIIbsavingsaccount.objects.create(branch=mybranch,
									month=month_name,
									staff=coopy,
									year=k.year,
									transID=k.transID,
									account_type=k.scheme,
									account_code=k.authorization_code,
									amount=k.amount,
									status='CR')
						k.status='Executed'
						k.save()

					pl=tblIIIIbassets_authorization.objects.filter(branch=mybranch,status='Running',year=year)		

					for j in pl:
						description=j.description
						scheme = stan_save.get(description=description)
						expiration_month_name = scheme.to_month #month_name

						expiration_month_index = list(calendar.month_name).index(expiration_month_name)

						df=coop.get(id=j.staff.id)

						gh=allsenario.filter(scheme=scheme,staff=df,status='Running')

						if gh.count() <1:
							if expiration_month_index == current_month_index:
								j.status='Completed'
								j.save()


					prp= all_prorations.filter(month=month_name)
					
					if prp.count() ==0:

						tblIIIbprorations.objects.create(branch=mybranch,
							staff=coop.get(staff=staffdet),
							status='Executed',
							month=month_name,
							transdate=fdate,
							amount=total,
							year=year)


					return render(request,'IIIb/proration_approv.html',{'company':mybranch, 
						'user':varuser,
						'year':year,
						'month':month_name})


				else:
					msg = f"you cannot SKIP a Month "
					return render(request,'IIIb/proration_fail.html',{'company':mybranch, 'user':varuser,'year':yy,'msg':msg})

			else:
				msg = f"YOU ALREADY PRORATED FOR {month_name}, {year} "
				return render(request,'IIIb/proration_fail.html',{'company':mybranch, 'user':varuser,'year':yy,'msg':msg})
		
		else:
			
			return render(request,'IIIb/proration.html',{'company':mybranch, 
				'user':varuser,'year':yy})

	else:
		return HttpResponseRedirect('/login/user/')
def proration(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


		if request.method == 'POST':
			current_month_index =int(request.POST['month_index'])
			year =request.POST['year']

		
			month_name = calendar.month_name[current_month_index]
			fdate=date.today()
			stan_save = tblstandardsavingIIIB.objects.filter(branch=mybranch)
			stan_loans = tblstandardloanIIIB.objects.filter(branch=mybranch)


			assets_authorization =tblIIIIbassets_authorization.objects.filter(branch=mybranch,status='Running',year=year)

			liabilities_authorization = tblIIIIbliabilities_authorization.objects.filter(branch = mybranch,	status = 'Running')


			coop=tblIIIbcoop.objects.filter(branch=mybranch,status=1)
			sss= tblIIIbsavingsaccount.objects.filter(branch=mybranch,month=month_name,year=year)
			all_prorations  = tblIIIbprorations.objects.filter(branch=mybranch, year=year,status='Executed')
			prorated_months=[a.month for a in all_prorations] #month_name
			prorated_months_indexes = sorted([list(calendar.month_name).index(m.capitalize()) for m in prorated_months])
			if not prorated_months:
				last_month_index=0
			else:#
				last_month_index = prorated_months_indexes[-1]

			pro_diff =   current_month_index - int(last_month_index )

			allsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch,	year=year)


			awaiting = allsenario.filter(month=month_name,status='Awaiting Execution')
			if awaiting.count() > 0:
				if pro_diff == 1 or pro_diff == current_month_index:
					tt=awaiting.aggregate(Sum('amount'))
					total = tt['amount__sum']
					for k in awaiting:
						coopy = coop.get(id = k.staff.id)
						ds = sss.filter(account_code=k.authorization_code,status='CR')
						if ds.count() == 0:
							tblIIIbsavingsaccount.objects.create(branch=mybranch,
									month=month_name,
									staff=coopy,
									year=k.year,
									transID=k.transID,
									account_type=k.scheme,
									account_code=k.authorization_code,
									amount=k.amount,
									status='CR')

						k.status='Executed'
						k.save()

						if k.account_type == 'Assets':
							gh=allsenario.filter(account_type='Assets', scheme=k.scheme,staff=coopy,status='Awaiting Execution')
							if gh.count() <1:
								pl = assets_authorization.get(asset_authorization_code=k.authorization_code)
								pl.status='Completed'
								pl.save()

						

						elif k.account_type == 'Liabilities':

							gh=allsenario.filter(account_type='Liabilities', scheme=k.scheme,staff=coopy,status='Awaiting Execution')
							if gh.count() <1:
								pl = liabilities_authorization.get(application_code = k.authorization_code)
								pl.status='Completed'
								pl.save()


					prp= all_prorations.filter(month=month_name)					
					if prp.count() ==0:
						tblIIIbprorations.objects.create(branch=mybranch,
							staff=coop.get(staff=staffdet),
							status='Executed',
							month=month_name,
							transdate=fdate,
							amount=total,
							year=year)
					return render(request,'IIIb/proration_approv.html',{'company':mybranch, 
						'user':varuser,
						'year':year,
						'month':month_name})


				else:
					msg = f"you cannot SKIP a Month "
					return render(request,'IIIb/proration_fail.html',{'company':mybranch, 'user':varuser,'year':yy,'msg':msg})

			else:
				msg = f"YOU ALREADY PRORATED FOR {month_name}, {year} "
				return render(request,'IIIb/proration_fail.html',{'company':mybranch, 'user':varuser,'year':yy,'msg':msg})
		
		else:
			
			return render(request,'IIIb/proration.html',{'company':mybranch, 
				'user':varuser,'year':yy})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def loanscene(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,month,status=acccode.split(":")


        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id

        		mybranch=tblBRANCH.objects.get(id=branch)


        		if month=='-':
        			msg='Select valid Month'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})

        		if status=='-':
        			msg='Select status'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})

        		month=int(month)
        		monthnam = calendar.month_name[month]




        		allschedules = tblIIIbprorations_schedule.objects.filter(branch=mybranch,year=year,
        			month=monthnam).order_by('staff__staff__surname')


        		scsenario = allschedules.filter(status=status)


        		#Total sum across all records
        		total_amount = scsenario.aggregate(total=Sum('amount'))['total']

        		#Subtotals grouped by staff
        		staff_totals = scsenario.values('staff__staff__surname',
					'staff__staff__firstname','staff__staff__othername','staff__id').annotate(staff_total=Sum('amount')).order_by('staff__staff__surname')




        		total = scsenario.aggregate(total=Sum('amount'))['total']


        		context = {'company':mybranch,
		        			'month':monthnam,
		        			'total_amount':total_amount,
		        			'staff_totals': staff_totals,
		        			'total':total,
		        			'year':year}


	        	if status == 'Awaiting Execution':
	        		context['status']= status
	        		return render(request,'IIIb/proration_ajax.html',context)


        		elif status == 'Declined' :
        			context['status']= status
	        		

        		elif status=='Executed':
        			context['status']= 'Proration'

	        	
	        	return render(request,'IIIb/proration_done.html',context)



        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')


@csrf_exempt
def proratepop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		year,month=acccode.split(':')
    		month=int(month)
    		monthnam = calendar.month_name[month]

    		return render(request,'IIIb/proration_pop.html',{
    			'month':monthnam,'year':year,
    			'month_index':month})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')


@csrf_exempt
def proratedetailspop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		vid,year,month,status=acccode.split(':')
    		coop=tblIIIbcoop.objects.get(id=vid)

    		month=int(month)
    		monthnam = calendar.month_name[month]

    		prop = tblIIIbprorations_schedule.objects.filter(staff=coop,year=year,month=monthnam,status=status)
    		j=[a.branch.id for a in prop][0]
    		

    		# msg=list(dict.fromkeys(j))[0]
    		return render(request,'IIIb/proration_details.html',{'prop': prop,
    			'month':monthnam,'year':year,'coop':coop,
    			'month_index':month})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')

    	


def prorateallrequests(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		fdate=date.today()

		if staff.thrift3b_admin==0 :
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			month =request.POST['month12']
			pack =request.POST['pack13']
			year =request.POST['year']

			month=int(month)
			monthnam = calendar.month_name[month]


			account_type=pack
			status='Awaiting Execution'


			coop=tblIIIbcoop.objects.filter(branch=mybranch,status=1)
		
			sss= tblIIIbsavingsaccount.objects.filter(branch=mybranch,month=monthnam,year=year)

			prp= tblIIIbprorations.objects.filter(branch=mybranch,status='Executed',
					month=monthnam,description=pack,year=year)



			allsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch,
				month=monthnam,
				year=year, account_type=account_type)

			awaiting = allsenario.filter(status=status)

			if awaiting.count() > 0 :
				tt=awaiting.aggregate(Sum('amount'))
				total = tt['amount__sum']


				for k in awaiting:
					coopy = k.staff.id
					coopy=coop.get(id=coopy)


					ds = sss.filter(account_code=k.authorization_code,status='CR')

					if ds.count() == 0:
						
						tblIIIbsavingsaccount.objects.create(branch=mybranch,
						month=monthnam,
						staff=coopy,
						year=k.year,
						transID=k.transID,
						account_type=k.scheme,
						account_code=k.authorization_code,
						amount=k.amount,
						status='CR')


					k.status='Executed'
					k.save()

			elif awaiting.count() ==0:
				Executed = allsenario.filter(status='Executed')


				if Executed.count() > 0 :
					tt=Executed.aggregate(Sum('amount'))
					total = tt['amount__sum']


			if prp.count() ==0:

				tblIIIbprorations.objects.create(branch=mybranch,
					staff=coop.get(staff=staffdet),
					status='Executed',
					month=monthnam,
					description=pack,
					transdate=fdate,
					amount=total,
					year=year)

			if pack=='package':
				
				pl=tblIIIIbassets_authorization.objects.filter(branch=mybranch,
					status='Running',year=year)		

				for j in pl:
					df = j.staff.id
					df=coop.get(id=df)					
					
					gh=tblIIIbprorations_schedule.objects.filter(branch=mybranch,
						scheme=j.description,
						staff=df,
						status=status, #status = 'awaiting execution'
						year=j.year)


					if gh.count() <1:
						j.status='Completed'
						j.save()


			return render(request,'IIIb/proration_approv.html',{'company':mybranch, 
				'user':varuser,
				'status':pack,
				'year':year,
				'month':monthnam})
		
		else:
			return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login/user/')





###############Aprovals*****************

def loan_approvals(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)
		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


		datte= date.today()
		jk=datte.month


		vf={'company':mybranch, 'user':varuser,'year':yy}

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',vf)



		if request.method == 'POST':
			year = request.POST['year']
			status =request.POST['status']

			transdate=date.today()
			
			coop = tblIIIbcoop.objects.get(staff =staffdet)

			


			selected_items_str = request.POST.get("selected_items", "")

			selected_items = selected_items_str.split(",") if selected_items_str else []





			allscsenario = tblIIIIbliabilities_authorization.objects.filter(application_code__in= selected_items)
			# return render(request,'IIIb/selectloan.html',{'msg':allscsenario})

			allscsenario.update(status='Awaiting Disbursal',approval_date=transdate)


			return render(request,'IIIb/approvalloan.html',{'company':mybranch, 
				'user':varuser,
				'year':year })


			return render(request,'IIIb/approval_loan_error.html',{'msg':msg})



		else:
			form=approveform()
			vf['msg']=''

			return render(request,'IIIb/approvals.html',vf)

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def myloanpreviews(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,status,option=acccode.split(":")


        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id

        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)


        		if status=='-':
        			msg='Select valid Status'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})

        		if option=='-':
        			msg='Select valid Option'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})

        		
        		if status =='Awaiting Approval' or status == 'Declined':
        			status2 = [status]
        		
        		elif status =='Approved':
        			status2=['Awaiting Disbursal', 'Running']
        		

        		allaplication = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,status__in=status2)

        		total=allaplication.aggregate(total=Sum('principal'))['total']



	        	if option == 'detail':


	        		return render(request,'IIIb/approval_loan_ajax.html',{'company':mybranch, 'email':varuser,
	        			'msg':allaplication,
	        			'status':status, 
	        			'year':year,
	        			'total':total})

	        	elif option == 'summary':
	        		return render(request,'IIIb/approval_loan_ajax_summary.html',{'company':mybranch, 'email':varuser,
	        			'msg':allaplication,
	        			'status':status, 
	        			'year':year,
	        			'total':total})

        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')






@csrf_exempt
def requestdetails(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		coop=acccode
    		
    		g= tblIIIIbliabilities_authorization.objects.get(application_code=coop)
    		customer=tblIIIbcoop.objects.get(id=g.staff.id)
    		mybranch=g.branch

    		return render(request,'IIIb/approve_loandetails.html',{'company':mybranch,
    			'state':coop,'k':g,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



@csrf_exempt
def declinepop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		coop=acccode
    		g= tblIIIIbliabilities_authorization.objects.get(application_code=coop)
    		customer=tblIIIbcoop.objects.get(id=g.staff.id)
    		mybranch=g.branch
    		return render(request,'IIIb/approve_loan_decline_pop.html',{
    			'state':coop,'k':g,'hhh':customer})
    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def yesdeclineloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)
	
		if staff.thrift3b_admin==0 :
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			state =request.POST['state123']

			status='Awaiting Approval'

			tblIIIIbliabilities_authorization.objects.filter(branch=mybranch, application_code =state,status=status).update(status='Declined')

			return HttpResponseRedirect('/IIIb/threeb/approvals/')

		
		else:
			return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def apprvepop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            post = request.POST.copy()
            acccode = post['userid']
            year, status = acccode.split(":")
            selected_items = post.get('items', '')
            selected_list = selected_items.split(",") if selected_items else []

            return render(request, 'IIIb/approve_loan_pop.html', {
                'year': year,
                'status': status,
                'selected_items': selected_list
            })
        else:
            return HttpResponseRedirect('/login/user/')
    else:
        return HttpResponseRedirect('/login/user/')








#####*******************DISBURSALS ******************


def loan_disburse(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id


		mybranch=tblBRANCH.objects.get(id=branch)
		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]

		if staff.thrift3b_admin==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		if staff.thrift3b_admin==1:
	
			if request.method == 'POST':
				year =int(request.POST['year'])
				status =request.POST['status']
				source=request.POST['source']

				transdate=date.today()

				allcoop=tblIIIbcoop.objects.filter(branch=mybranch,status=True)
				sav_account = tblIIIbsavingsaccount.objects.filter(branch = mybranch,year=year)

				coop = tblIIIbcoop.objects.get(staff =staffdet)
				
				selected_items_str = request.POST.get("selected_items", "")
				selected_items = selected_items_str.split(",") if selected_items_str else []


				if source == "Loans and Commodities": 

				
					current_month_month_index = transdate.month

					current_month_name = calendar.month_name[transdate.month]
					
					allscsenario = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,application_code__in= selected_items)
			
					
					ffl = tblIIIbprorations_schedule.objects.filter(branch=mybranch,status='Awaiting Execution',
							account_type='Liabilities',
							# scheme='Loan Repayment',
							year=year)

					for vp in allscsenario:
						coop=allcoop.get(id=vp.staff.id)
						loan_application=allscsenario.get(staff=coop)
						application_code = vp.application_code
						package_end_month_index = vp.package.tenure
						grace_period =vp.grace_period #30 0r 60
						loan_package= vp.package.description

						scheme=vp.description

						df = sav_account.filter(account_code=vp.application_code)

						transID = generate_trans_pin()

						# return render(request,'IIIb/selectloan.html',{'msg':type(grace_period)})

						if df.count() == 0: #1 debit savings account
							# gp=0
							df = tblIIIbsavingsaccount.objects.create(branch=mybranch, 
										staff =coop,
										month=current_month_name,
										year=year,status='DR',
										amount=vp.total_repayment,
										transdate=transdate,
										account_type=vp.description,
										account_code=application_code,
										transID=transID)

					
						monthly_deduction = round(float(vp.thrift), 2)



						if grace_period==30:

							repay_month_month_index = 	current_month_month_index +  2

							if repay_month_month_index > 12:
								repay_month_month_index=repay_month_month_index - 12
								repay_year = year + 1 
							else:
								repay_year = year
								

						elif grace_period==60:
							repay_month_month_index = 	current_month_month_index +  3

							if repay_month_month_index > 12:
								repay_month_month_index=repay_month_month_index - 12
								repay_year = year + 1 
							else:
								repay_year = year

						repay_month_month_name = calendar.month_name[repay_month_month_index]


						package_end_month_index = repay_month_month_index + package_end_month_index



						for x in range(repay_month_month_index,package_end_month_index):

							if x > 12:
								p=x-12
								repay_year=year + 1
							else:
								p =x
								repay_year=repay_year

							schedule_month = calendar.month_name[p]
							
							transID = generate_trans_pin()

							sls = ffl.filter( month= schedule_month,staff=coop)

							if sls.count() == 0:
								tblIIIbprorations_schedule.objects.create(staff =coop,
									branch = mybranch,
									month=schedule_month,
									amount=monthly_deduction,
									year=repay_year,
									transID=transID,
									status='Awaiting Execution',
									authorization_code=application_code,
									scheme = f"{scheme} repayment",
									account_type='Liabilities',
									transdate=transdate)
								

							vp.status='Running'
							vp.disbursal_date=transdate
							vp.save()

						####Sending email notifications****************
					
				elif source == "Other Savings":
					savings=request.POST['savings']

					month_index= transdate.month
					current_month_name= calendar.month_name[month_index]

					w = tblIIIIbscheme_withdrawal.objects.filter(branch=mybranch)



					staff_totals = (sav_account
					    .filter(account_code__in=selected_items)
					    .values('staff__id', 'account_code')
					    .annotate(staff_total=Sum('amount')))



					for row in staff_totals:
						transID = generate_trans_pin()

						obj, created = tblIIIbsavingsaccount.objects.get_or_create(
					        branch=mybranch,
					        staff_id=row['staff__id'],
					        status="DR",                     # fixed status
					        account_type = savings,
					        account_code=row['account_code'],  # actual code from selection
					        amount = row['staff_total'],
					        defaults={
					        	"year": year,
					            "month": current_month_name,
					            "transdate": transdate,						            
					            "transID": transID })


						c = w.get(staff=row['staff__id'], 
									year= year, 
									scheme_authorization_code =row['account_code'],
									description = savings)

						c.status="Disbursed"
						c.save()



					    ########Sendig emails*********************
				
				return render(request,'IIIb/disburse_succces.html',{'company':mybranch,'user':varuser, 'year':year,'month':current_month_name})
			
			else:

				return render(request,'IIIb/disburse.html',{'company':mybranch, 'user':varuser,'year':yy})

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def setsource_ajax(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,source=acccode.split(":")


        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id 		
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.filter(branch=mybranch,status=1)

        		if source=='-':
        			msg='Select a status'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})

        		if source == 'Loans and Commodities':
        			return render(request,'IIIb/disburse_source_ajax.html',{'status':source,'year':year})
        		
        		elif source == 'Other Savings':
        			sav = tblstandardsavingIIIB.objects.filter(branch=mybranch).exclude(description='Wallet')
        			
        			return render(request,'IIIb/disburse_source_other_savings_ajax.html',{'status':source,'year':year,'savings':sav})


        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')

@csrf_exempt
def setsave_ajax(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,savings,status=acccode.split(":")


        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id 		
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.filter(branch=mybranch,status=1)



        		bank =tblIIIb_bankdetail.objects.filter(branch=mybranch)

        		

        		if savings=='-':
        			msg='Select a saving scheme'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})


        		if status=='-':
        			msg='Select application status'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})



        		ds = tblIIIIbscheme_withdrawal.objects.filter(branch=mybranch,year=year,
        			description=savings,status=status)

        		total=ds.aggregate(total=Sum('amount'))['total']


        		#checking if bank details are entered
        		m=[]
        		for l in ds:
        			pu= bank.filter(staff= l.staff)
        			if pu.count() ==0:
        				m.append(l)

        		if len(m)>0:
        			return render(request,'IIIb/disburse_missing_ajax.html',{'msg':m})

        		
        				


        		c=[]

        		for k in ds:
        			b=bank.get(staff=k.staff)
        			ff={'bank':b,'coop':k}
        			c.append(ff)


        		bb = {'company':mybranch, 'status':status,'year':year,'bank':bank,'savings':savings,'msg':c,'total':total}

        		if status== 'Awaiting Disbursal':
        			return render(request,'IIIb/disburse_ajax2.html',bb)
        		elif status== 'Disbursed':
        			return render(request,'IIIb/disburse_ajax.html',bb)


        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')




@csrf_exempt
def withpopajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.method == 'POST':
            post = request.POST.copy()
            acccode = post['userid']
            year, status,source,savings = acccode.split(":")
            selected_items = post.get('items', '')
            selected_list = selected_items.split(",") if selected_items else []

            return render(request, 'IIIb/disburse_scheme_pop.html', {
                'year': year,
                'status': status,
                'source':source,
                'savings':savings,
                'selected_items': selected_list
            })
        else:
            return HttpResponseRedirect('/login/user/')
    else:
        return HttpResponseRedirect('/login/user/')



@csrf_exempt
def disburse_ajax(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,status=acccode.split(":")


        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id 		
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.filter(branch=mybranch,status=1)

        		bank_details = tblIIIb_bankdetail.objects.filter(branch=mybranch) 


        		if status=='-':
        			msg='Select a status'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})



        		allaplication = tblIIIIbliabilities_authorization.objects.filter(branch=mybranch,status=status)
        		


        		if allaplication.count()>0:

	        		tt=allaplication.aggregate(Sum('principal'))
	        		total = int(tt['principal__sum'])
	        	else:

	        		total=0


	        	if status=='Awaiting Disbursal':
		        	return render(request,'IIIb/disburse_loan_ajax.html',{'company':mybranch,'email':varuser,
		    			'msg':allaplication,
		    			'status':status,
		    			'year':year,
		    			'total':total})


		        elif status=='Running':

	        		p=[]

	        		for k in allaplication:
	        			staff =k.staff.id
	        			staff=kfw.get(id =staff)
	        			try:
	        				g=bank_details.get(staff=staff)
	        			except:
	        				g='N/A'
	        			jk ={'staff':k,'bank':g}
	        			p.append(jk)




        			return render(request,'IIIb/disbursed_request_ajax.html',{'company':mybranch,
		    			'msg':p,
		    			'status':status,
		    			'year':year,
		    			'total':total})


        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')


@csrf_exempt
def disbursepop(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,status,source=acccode.split(":")

        		selected_items = post.get('items', '')
        		selected_list = selected_items.split(",") if selected_items else []
        		return render(request,'IIIb/disburse_loan_pop.html',{'year':year,
        			'selected_items': selected_list,
        			'status':status,'source':source})

        else:
        	return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')




####***********MY deductions********************************
def dedopts(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


		form = approveform()

		fv= {'company':mybranch, 'user':varuser,'form':form,'year':yy,'msg':coop}
		
		if staff.thrift3b_admin==1:
			return render(request,'IIIb/sosdeduct.html',fv)
		elif staff.thrift3b_cashier==1:
			return render(request,'IIIb/sosdeduct_c.html',fv)
		elif staff.thrift3b_officer==1:
			return render(request,'IIIb/sosdeduct_o.html',fv)


	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def ajaxded(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)


        		if month=='-':
        			msg='Select valid Month'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]

        		tdate=date.today()
        		year=tdate.year

        		status='Executed'


        		scsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch,
        			month=monthnam,
        			year=year,
        			staff=kfw,
        			status=status)

        		tt=scsenario.aggregate(Sum('amount'))
        		total = tt['amount__sum']

        		return render(request,'IIIb/dedajax.html',{'email':user,
        			'msg':scsenario,
        			'status':status, 
        			'month':monthnam,
        			'total':total,
        			'year':year})

        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')




##############################REPORTS********************************
def hr(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_cashier==0:
			return render(request,'IIIb/404.html',{'company':branch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]



		# form = mysavingsform()
		if staff.thrift3b_cashier==1:
			return render(request,'IIIb/hr_income.html',{'company':mybranch,
				'user':varuser,
				# 'form':form,
				'year':yy,
				'msg':coop})

	else:
		return HttpResponseRedirect('/login/user/')

@csrf_exempt
def reportajaxx(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		year,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id

        		mybranch=tblBRANCH.objects.get(id=branch)


        		if month=='-':
        			msg='Select valid Month'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]

        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')


def deductions(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_cashier==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id



		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff,branch=mybranch,status=1)

		yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]



		form = approveform()
		if staff.thrift3b_cashier==1:
			return render(request,'IIIb/hr_deduct.html',{'company':mybranch,
				'user':varuser,
				'form':form,
				'year':yy,
				'msg':coop})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def deajax(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")


        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.filter(branch=mybranch,status=1)

	

        		if month=='-':
        			msg='Select valid Month'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]
        		tdate=date.today()
        		year=tdate.year

        		status='Executed'



	        	scsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch, month=monthnam,	status=status)

	        	allmoney = scsenario.aggregate(total=Sum('amount'))['total'] or 0




        		deductions = scsenario.values('staff__staff__surname',
					'staff__staff__firstname','staff__staff__othername','staff__id').annotate(staff_total=Sum('amount')).order_by('staff__staff__surname')



		
        		return render(request,'IIIb/hr_deduct_ajax.html',{
        			'deductions':deductions,
        			'status':status, 
        			'month':monthnam,
        			'year':year,
        			# 'total':total,
        			'pack':allmoney})


        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')



@csrf_exempt
def trailded(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		month,vid=acccode.split(":")


        		staff = Userprofile.objects.get(email=varuser,status=1)
        		branch=staff.branch.id
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(id =vid)


        		if month=='-':
        			msg='Select valid Month'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})


        		month=int(month)
        		monthnam = calendar.month_name[month]

        		tdate=date.today()
        		year=tdate.year

        		status='Executed'


        		scsenario = tblIIIbprorations_schedule.objects.filter(
        			branch=mybranch,
        			month=monthnam,
        			year=year,
        			staff=kfw,
        			status=status)

        		tt=scsenario.aggregate(Sum('amount'))
        		total = tt['amount__sum']


        		return render(request,'IIIb/dedajax.html',{
        			'msg':scsenario,
        			'status':status, 
        			'month':monthnam,
        			'total':total,
        			'year':year})

        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')



		




# #*******************My Savings*******************************

def cash_deposit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)
		coop = tblIIIbcoop.objects.get(staff=find_staff, status=1)
		

		if request.method=='POST':
			month=request.POST['month']
			amount=request.POST['amount']

			if month == '---':
				msg = 'select month'
				return render(request,'IIIb/selectloan.html',{'msg':msg})

			else:
				fig = num2words(int(amount))
				yyear=ddatt.year

				if staff.thrift3b_admin==1:
					return render(request,'IIIb/deposit.html',{'company':mybranch, 
						'user':varuser,
						'msg':coop,
						'month':month,
						'fig':fig,
						'amount':amount,
						'year':yyear})

				if staff.thrift3b_cashier==1:
					return render(request,'IIIb/deposit_c.html',{'company':mybranch, 
						'user':varuser,
						'msg':coop,
						'month':month,
						'fig':fig,
						'amount':amount,
						'year':yyear})

				if staff.thrift3b_officer==1:
					return render(request,'IIIb/deposit_o.html',{'company':mybranch, 
						'user':varuser,
						'msg':coop,
						'month':month,
						'fig':fig,
						'amount':amount,
						'year':yyear})



		else:


			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]

			if staff.thrift3b_admin==1:
				return render(request,'IIIb/cashdepo.html',{'company':mybranch,
					'user':varuser,
					'msg':coop,
					'year':yy})

			elif staff.thrift3b_cashier==1:

				return render(request,'IIIb/cashdepo_c.html',{'company':mybranch, 
					'user':varuser,
					'msg':coop,
					'year':yy})

			elif staff.thrift3b_officer==1:
				return render(request,'IIIb/cashdepo_o.html',{'company':mybranch,
					'user':varuser,
					'msg':coop,
					'year':yy})

	else:
		return HttpResponseRedirect('/login/user/')





@csrf_exempt
def destination_acc(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']

 
				staff = tblSTAFF.objects.get(email=varuser,status=1)
				bra=staff.branch.id
				mybranch=tblBRANCH.objects.get(id=bra)

				post = request.POST.copy()
				acccode = post['userid']

				tdate= date.today()
				month=tdate.month
				monthname = calendar.month_name[month]
				year=tdate.year

				state = acccode
				kk = []
				sdic = {}

				t= tblstandardsavingIIIB.objects.filter(branch=mybranch)
				for k in t:
					kk.append(k.description)
				kk.append('Application Form')
				kk.append('Subscription')
				kk.append('Loan Repaymrnt')
				kk.append('Commodities Repaymrnt')




				return HttpResponse(json.dumps(kk), content_type='application/json')
			
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:
			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def checkdep(request):
    if  "userid" in request.session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        	if request.method == 'POST':
        		varuser = request.session['userid']
        		varerr =""
        		post = request.POST.copy()
        		acccode = post['userid']
        		user,month=acccode.split(":")

        		staff = Userprofile.objects.get(email=user,status=1)
        		branch=staff.branch.id
        		mycompany=staff.branch.company
        		company=mycompany.name
        		comp_code=mycompany.id
        		ourcompay=tblCOMPANY.objects.get(id=comp_code)
        		mybranch=tblBRANCH.objects.get(id=branch)
        		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

        		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

        		if month=='---':
        			msg='Select valid Month'
        			return render(request,'IIIb/selectloan.html',{'msg':msg})

        		tdate= date.today()
        		year=tdate.year

        		account_type='Wallet'

        		try:

	        		yt= tblIIIbprorations.objects.get(branch=mybranch,
	        			month=month,
	        			year=year,
	        			description=account_type)

	        		msg='Applications are closed for this month'
	        		return render(request,'IIIb/selectloan.html',{'msg':msg})

	        	except:

	        		scsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch,
	        			month=month,
	        			staff=kfw,
	        			year=year,
	        			account_type=account_type)

	        		if scsenario.count() > 0:
	        			msg='you have an application already'
	        			return render(request,'IIIb/selectloan.html',{'msg':msg})
	    
	        		else:
	        			msg = f"make a one time deposit into your cooperative wallet"

		        		return render(request,'IIIb/sss.html',{'msg':msg})
        	else:
        		gdata = ""
        		return render(request,'index.html',{'gdata':gdata})

    else:
    	return HttpResponseRedirect('/login/user/')




def save_deposit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift3b_officer==0:
			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		kfwf=tblIIIbcoop.objects.get(staff=memstaff,branch=mybranch,status=1)

		surname=kfwf.staff.surname
		firstname=kfwf.staff.firstname


		year=ddatt.year
		code = generate_trans_pin()

		amount=request.POST['amount']
		month =request.POST['month']

		if not tblIIIbprorations_schedule.objects.filter(staff =kfwf,
			branch = mybranch,
			month=month,
			year=year,
			status='Awaiting Execution',
			account_type='Wallet',
			scheme	='Wallet').exists():


			tblIIIbprorations_schedule.objects.create(staff =kfwf,
				branch = mybranch,
				month=month,
				year=year,
				amount=amount,
				status='Awaiting Execution',
				authorization_code=code,
				account_type='Wallet',
				scheme	='Wallet',
				transdate=ddatt)

			#**configure email sending***********

		try:
			savingscheme_email(mybranch,varuser,surname,firstname,amount,year,package,bg[0],bg[-1])
		except:
			pl=0

		if staff.thrift3b_admin==1:
			return render(request,'IIIb/saving_success.html',{'company':mybranch, 'user':varuser, 'amount':amount,'month':month,'year':year})

		elif staff.thrift3b_cashier==1:
			return render(request,'IIIb/saving_success_c.html',{'company':mybranch, 'user':varuser, 'amount':amount,'month':month,'year':year})
						
		elif staff.thrift3b_officer==1:
			return render(request,'IIIb/saving_success_o.html',{'company':mybranch, 'user':varuser, 'amount':amount,'month':month,'year':year})

	else:
		return HttpResponseRedirect('/login/user/')

# @csrf_exempt
# def prooneoffpop(request):
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#     	if request.method == 'POST':
#     		post = request.POST.copy()
#     		acccode = post['userid']
#     		year=date.today().year
#     		# year=year.year
#     		month,pack=acccode.split(':')
#     		month=int(month)
#     		monthnam = calendar.month_name[month]

#     		return render(request,'IIIb/proratewwall.html',{
#     			'month':monthnam,'year':year,
#     			'month_index':month, 'pack':pack})
#     	else:
#     		return HttpResponseRedirect('/login/user/')
#     else:
#     	return HttpResponseRedirect('/login/user/')




# def prorateoneoff(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff = Userprofile.objects.get(email=varuser,status=1)

# 		staffdet=staff.staffrec.id
# 		branch=staff.branch.id

# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id
# 		ourcompay=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(id=branch)
# 		f= datetime.today()
# 		year=f.year
# 		fdate=date(year,f.month,f.day)

# 		if staff.thrift3b_admin==0 :
# 			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

# 		if request.method == 'POST':
# 			month =request.POST['month12']
# 			pack =request.POST['pack13']

# 			month=int(month)
# 			monthnam = calendar.month_name[month]

# 			account_type=pack
# 			status='Awaiting Execution'
		
# 			scsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch,
# 				month=monthnam,
# 				year=year,
# 				account_type=account_type,
# 				status=status)

# 			tt=scsenario.aggregate(Sum('amount'))
# 			total = tt['amount__sum']

			
# 			for k in scsenario:
# 				staff = k.staff.id
# 				staff=tblIIIbcoop.objects.get(id=staff,branch=mybranch,status=1)

# 				tblIIIbsavingsaccount(branch=mybranch,
# 				month=monthnam,
# 				staff=staff,
# 				year=k.year,
# 				account_type=k.scheme,
# 				code=k.code,
# 				amount=k.amount,
# 				status='CR').save()

# 				k.status='Executed'
# 				k.save()

# 			# scsenario.update(status='Executed')


# 			tblIIIbprorations(branch=mybranch,
# 				staff=staff,
# 				status='Executed',
# 				month=monthnam,
# 				description=pack,
# 				transdate=fdate,
# 				amount=total,
# 				year=year).save()

# 			return render(request,'IIIb/walapprov.html',{'company':mybranch, 
# 				'user':varuser,
# 				'status':pack,
# 				'year':year,
# 				'month':monthnam})
		
# 		else:
# 			return HttpResponseRedirect('/dashboard/')
# 	else:
# 		return HttpResponseRedirect('/login/user/')










# def changepass(request):
# 	if 'userid' in request.session:
# 		varuser = request.session['userid']

# 		try:
# 			staff = Userprofile.objects.get(email=varuser,status=1)
# 		except:
# 			return HttpResponseRedirect('/login/user/')

# 		staffdet=staff.staffrec.id
# 		branch=staff.branch.id
# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id
# 		ourcompay=tblCOMPANY.objects.get(id=comp_code)
# 		mybranch=tblBRANCH.objects.get(id=branch)

# 		if request.method=='POST':
# 			oldpass= request.POST['oldpass']
# 			newpass1=request.POST['newpass1']
# 			newpass2=request.POST['newpass2']

# 			if oldpass== staff.password :
# 				if newpass2 == newpass1:
# 					msg= 'password change successfull'
# 					rr=Userprofile.objects.filter(email=varuser,status=1).update(password=newpass1)

# 					return render(request,'IIIb/changepass_success.html',{'user':varuser,'company':mybranch,
# 						'menu':staff,'msg':msg})
# 				else:
# 					msg = 'the passwords do not match'
# 			else:
# 				msg='your old pass is not correct'
# 		else :
# 			msg=''
# 		return render(request,'IIIb/changepass.html',{'user':varuser,'company':mybranch,
# 				'menu':staff,'msg':msg})

# 	else:
# 		return HttpResponseRedirect('/login/user/')


# def massReg(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff=Userprofile.objects.get(email=varuser, status=1)
# 		staffdet=staff.staffrec.id

# 		branch=staff.branch.id
# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id

# 		ourcompany=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

# 		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


# 		if staff.thrift3a_cashier==0:
# 			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

# 		return render(request,'IIIb/adminwelcome.html',{'company':mybranch, 'user':varuser})

# 	else:
# 		return HttpResponseRedirect('/login/user/')



# def massReg(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff = Userprofile.objects.get(email=varuser,status=1)


# 		staffdet=staff.staffrec.id

# 		branch=staff.branch.id
# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id

# 		ourcompany=tblCOMPANY.objects.get(id=comp_code)
# 		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

# 		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
# 		try:
# 			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
# 		except:
# 			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

# 		msg = ''

# 		if request.method == 'POST':
# 			surname=request.POST['surname']

# 			try :


# 				acc_cus=tblCUSTOMER.objects.get(surname=surname,firstname=firstname,othername=othername,
# 					phone=phone,Address=address,wallet=wallet,code=68768,email=email,
# 					UX=0,branch=mybranch,merchant=memmerchant,status=1,
# 					online=0,sms=0,get_email=0)

# 				tblsavingsaccount(customer=acc_cus,branch=mybranch,UX=0,status=1,online=0,sms=0,get_email=0,withdr_status=1).save()

# 				return render(request,'thrift/success.html',{'company':mybranch,'user':varuser,'wallet':wallet})

# 			except:
# 				msg = 'Incomplete phone number'

# 		return render(request,'staff/massreg.html',{'company':mybranch, 'user':varuser,'msg':msg})

# 	else:
# 		return HttpResponseRedirect('/login/user/')




# def newregistration(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff = Userprofile.objects.get(email=varuser,status=1)


# 		staffdet=staff.staffrec.id

# 		branch=staff.branch.id
# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id

# 		ourcompany=tblCOMPANY.objects.get(id=comp_code)
# 		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

# 		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


# 		if request.method == 'POST':
# 			surname=request.POST['surname']
# 			firstname= request.POST['firstname']
# 			othername=request.POST['othername']
# 			phone=request.POST['phone']
# 			address=request.POST['address']
# 			email = request.POST['email']

# 			phone=phone.split(' ')
# 			phone = str(phone[0]+phone[1]+phone[2])

# 			if 'photo' in request.FILES:
# 				photo=request.FILES['photo']
# 			else:
# 				photo = 'staff_pix/user.png'


# 			try:
# 				phone1=int(phone)


# 				try:
# 					msg = 'Eimail already in use'
# 					countt=tblSTAFF.objects.get(email=email,phone=phone)

# 				except:
# 					k = random.randint(0,9)
# 					y = random.randint(0,9)
# 					x = random.randint(0,9)
# 					z = random.randint(0,9)
# 					a = random.randint(0,9)
# 					pin =  str(k) + str(y) + str(x) + str(z)+ str(a)

# 					tblSTAFF(code = pin, status=1, branch=mybranch,surname=surname,
# 						firstname=firstname,othername=othername,
# 						Address=address,types='Office', phone=phone,photo=photo, email=email).save()

# 					new_staff = tblSTAFF.objects.get(email=email)
# 					name = new_staff.surname + " " + new_staff.firstname + " " + new_staff.othername


# 					Userprofile(branch =mybranch, password='cooperative', staffrec=new_staff,code =pin, status=1, email=email,thrift3b=1,thrift3b_officer=1).save()

# 					email=[email]
# 					sendMailMembership(email)

# 				return render(request,'IIIb/success.html',{'company':mybranch,'user':varuser,'name':name})

# 			except:
# 				msg = 'Incomplete phone number'
# 		else:
# 			msg=''

# 		return render(request,'IIIb/registration.html',{'company':mybranch, 'user':varuser,'msg':msg})

# 	else:
# 		return HttpResponseRedirect('/login/user/')










# @csrf_exempt
# def declineoptions(request):
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#     	if request.method == 'POST':
#     		post = request.POST.copy()
#     		acccode = post['userid']
#     		state,month,package=acccode.split(':')#month in index form
#     		customer=tblIIIbcoop.objects.get(id=state,status=1)

#     		return render(request,'IIIb/decline_opt.html',{
#     			'state':state,'month':month,'package':package,'hhh':customer})
#     	else:
#     		return HttpResponseRedirect('/login/user/')
#     else:
#     	return HttpResponseRedirect('/login/user/')


# def yesdecline(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff = Userprofile.objects.get(email=varuser,status=1)

# 		staffdet=staff.staffrec.id
# 		branch=staff.branch.id

# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id
# 		ourcompay=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(id=branch)
# 		f= datetime.today()
# 		mday=f.day
# 		mmonth =f.month
# 		myear=f.year
# 		fdate=date(myear,mmonth,mday)

# 		if staff.thrift3b_admin==0 :
# 			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

# 		if request.method == 'POST':
# 			month =request.POST['month123']
# 			pack =request.POST['pack123']
# 			state =request.POST['state123']

# 			status='Awaiting Execution'

# 			customer=tblIIIbprorations_schedule.objects.filter(id=state,status=status).update(status='Declined')

# 			month=int(month)
# 			monthnam = calendar.month_name[month]

# 			account_type=pack


# 			scsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch,
# 				month=monthnam,
# 				account_type=account_type,
# 				status=status)

# 			tt=scsenario.aggregate(Sum('amount'))
# 			total = tt['amount__sum']

# 			return render(request,'IIIb/decredirect.html',{'company':mybranch,
# 				'user':varuser,
# 				'msg':scsenario,
# 				'status':status,
# 				'state':state,
# 				'total':total,
# 				'month':monthnam,
# 				'month_index':month,
# 				'pack':pack})
		
# 		else:
# 			return HttpResponseRedirect('/dashboard/')
# 	else:
# 		return HttpResponseRedirect('/login/user/')



# def lr(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff = Userprofile.objects.get(email=varuser,status=1)

# 		staffdet=staff.staffrec.id
# 		branch=staff.branch.id

# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id
# 		ourcompay=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(id=branch)

# 		if staff.thrift3b_admin==0:
# 			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

# 		if request.method == 'POST':
# 			form =savingsform(request.POST)

# 			if form.is_valid():
# 				staff =form.cleaned_data['email']

# 				try:
# 					memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)
# 					kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)
# 				except:
# 					raise e
# 			else:
# 				msg = 'enter valid email'
# 				return render(request,'IIIb/selectloan.html',{'msg':msg})

# 		else:
# 			msg=''
# 		return render(request,'IIIb/app_loan.html',{'company':mybranch, 'user':varuser,'msg':msg})

# 	else:
# 		return HttpResponseRedirect('/login/user/')


# @csrf_exempt
# def loanscene_old(request):
#     if  "userid" in request.session:
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         	if request.method == 'POST':
#         		varuser = request.session['userid']
#         		varerr =""
#         		post = request.POST.copy()
#         		acccode = post['userid']
#         		user,funding=acccode.split(":")


#         		staff = Userprofile.objects.get(email=user,status=1)
#         		branch=staff.branch.id
#         		mycompany=staff.branch.company
#         		company=mycompany.name
#         		comp_code=mycompany.id
#         		ourcompay=tblCOMPANY.objects.get(id=comp_code)
#         		mybranch=tblBRANCH.objects.get(id=branch)
#         		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

#         		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

#         		if funding=='-----':
#         			msg='Select a source of fund for this transaction'
#         			return render(request,'IIIb/selectloan.html',{'msg':msg})
#         		elif funding=='salary':
#         			form=approveform()
#         			return render(request,'IIIb/salary.html',{'form':form,'user':user})

#         		elif funding=='myself':
#         			form=savingsform()
#         			return render(request,'IIIb/self.html',{'form':form,'user':user})

#         	else:
#         		gdata = ""
#         		return render(request,'index.html',{'gdata':gdata})

#     else:
#     	return HttpResponseRedirect('/login/user/')


# @csrf_exempt
# def loandem(request):
#     if  "userid" in request.session:
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#         	if request.method == 'POST':
#         		varuser = request.session['userid']
#         		varerr =""
#         		post = request.POST.copy()
#         		acccode = post['userid']
#         		user,month=acccode.split(":")


#         		staff = Userprofile.objects.get(email=user,status=1)
#         		branch=staff.branch.id
#         		mycompany=staff.branch.company
#         		company=mycompany.name
#         		comp_code=mycompany.id
#         		ourcompay=tblCOMPANY.objects.get(id=comp_code)
#         		mybranch=tblBRANCH.objects.get(id=branch)
#         		memstaff = tblSTAFF.objects.get(email=user,branch=mybranch,status=1)

#         		kfw=tblIIIbcoop.objects.get(staff=memstaff,status=1)

#         		if month=='-':
#         			msg='Select a month'
#         			return render(request,'IIIb/selectloan.html',{'msg':msg})



#         		month=int(month)
#         		monthnam = calendar.month_name[month]

#         		ddd=date.today()
#         		year=ddd.year

#         		status='Awaiting Execution'

#         		sbbh= tblIIIbprorations_schedule.objects.filter(branch=mybranch,
#         			month=monthnam,
#         			year=year,
#         			account_type='Loan',
#         			status=status)


#         		tt=sbbh.aggregate(Sum('amount'))
#         		total = tt['amount__sum']


#         		return render(request,'IIIb/loanded.html',{'email':user,
#     				'total':total,
#     				'msg':sbbh,
#     				'year':year,
#     				'status':status, 'month':monthnam})


#         	else:
#         		gdata = ""
#         		return render(request,'index.html',{'gdata':gdata})

#         else:
#         	getdetails = tblcontents.objects.filter(topic=id)
#         	return render(request,'lesson/entersub.html',{'gdata':getdetails})
#     else:
#     	return HttpResponseRedirect('/login/user/')



# @csrf_exempt
# def loanprooptions(request):
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#     	if request.method == 'POST':
#     		post = request.POST.copy()
#     		acccode = post['userid']
#     		year= date.today().year
#     		month,pack=acccode.split(':')
#     		month=int(month)
#     		monthnam = calendar.month_name[month]

#     		return render(request,'IIIb/loanproopt.html',{
#     			'month':monthnam,'year':year,
#     			'month_index':month, 'pack':pack})
#     	else:
#     		return HttpResponseRedirect('/login/user/')
#     else:
#     	return HttpResponseRedirect('/login/user/')




# def proallloan(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff = Userprofile.objects.get(email=varuser,status=1)

# 		staffdet=staff.staffrec.id
# 		branch=staff.branch.id

# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id
# 		ourcompay=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(id=branch)
# 		f= datetime.today()
# 		year=f.year
# 		fdate=date(year,f.month,f.day)

# 		if staff.thrift3b_admin==0 :
# 			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

# 		if request.method == 'POST':
# 			month =request.POST['month12']
# 			pack =request.POST['pack13']

# 			month=int(month)
# 			monthnam = calendar.month_name[month]

# 			account_type=pack
# 			status='Awaiting Execution'

		
# 			scsenario = tblIIIbprorations_schedule.objects.filter(branch=mybranch,
# 				month=monthnam,
# 				year=year,
# 				account_type='Loan',
# 				status=status)

# 			tt=scsenario.aggregate(Sum('amount'))
# 			total = tt['amount__sum']

			
# 			for k in scsenario:
# 				k.status='Executed'
# 				k.save()

# 			sttt = tblSTAFF.objects.get(id=staffdet)
# 			staffff=tblIIIbcoop.objects.get(staff=sttt)

# 			tblIIIbprorations(branch=mybranch,
# 				staff=staffff,
# 				status='Executed',
# 				month=monthnam,
# 				description='Loan',
# 				transdate=fdate,
# 				amount=total,
# 				year=year).save()



# 			return render(request,'IIIb/prroloan.html',{'company':mybranch, 
# 				'user':varuser,
# 				'status':pack,
# 				'year':year,
# 				'month':monthnam})
		
# 		else:
# 			return HttpResponseRedirect('/dashboard/')
# 	else:
# 		return HttpResponseRedirect('/login/user/')


# def staffwelcome(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff=Userprofile.objects.get(email=varuser, status=1)
# 		staffdet=staff.staffrec.id

# 		branch=staff.branch.id
# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id

# 		ourcompany=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
# 		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


# 		if staff.thrift3b_officer==0:
# 			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

# 		return render(request,'IIIb/welcome.html',{'company':mybranch, 'user':varuser})
# 	else:
# 		return HttpResponseRedirect('/login/user/')



# # def apply(request):
# # 	if 'userid' in request.session:
# # 		varuser=request.session['userid']
# # 		staff = Userprofile.objects.get(email=varuser,status=1)


# # 		staffdet=staff.staffrec.id
# # 		branch=staff.branch.id

# # 		mycompany=staff.branch.company
# # 		company=mycompany.name
# # 		comp_code=mycompany.id

# # 		ourcompay=tblCOMPANY.objects.get(id=comp_code)

# # 		mybranch=tblBRANCH.objects.get(id=branch)

# # 		if staff.thrift3b_officer==0: 
# # 			return render(request,'IIIb/404loan.html',{'company':mybranch, 'user':varuser})


# # 		find_staff = tblSTAFF.objects.get(email=varuser,branch=mybranch,status=1)

# # 		if request.method == 'POST':
# # 			thrift=request.POST['thrift']
# # 			amount= request.POST['amount']
# # 			package=request.POST['package']
# # 			repay=request.POST['repay']

# # 			if repay=='-----':
# # 				msg = 'Select appropriate repayment month'
# # 				return render(request,'IIIb/selectloan.html',{'msg':msg})

# # 			fdate= datetime.today()
# # 			todayy=date(fdate.year,fdate.month,fdate.day)

# # 			loan_package = tblstandardloanIIIB.objects.get(description=package, branch=mybranch)

# # 			try:
# # 				etwtwer
# # 			except:

# # 				tblIIIIbliabilities_authorization(branch=mybranch,staffrec=find_staff,package=loan_package,
# # 					volume=amount,status='Not Approved', date= todayy,thrift=thrift).save()

# # 				email = [varuser]
# # 				# sendMailapplyloan(email)

# # 				if staff.thrift3b_cashier==1:
# # 					return render(request,'IIIb/booking_cashier.html',{'company':mybranch, 'user':varuser,'customer':0})
# # 				else:
# # 					return render(request,'IIIb/booking_officer_success.html',{'company':mybranch, 'user':varuser,'customer':0})


# # 	else:
# # 		return HttpResponseRedirect('/login/user/')







# # def repay(request):
# # 	if 'userid' in request.session:
# # 		varuser=request.session['userid']

# # 		staff = Userprofile.objects.get(email=varuser,status=1)

# # 		staffdet=staff.staffrec.id

# # 		branch=staff.branch.id
# # 		mycompany=staff.branch.company
# # 		company=mycompany.name
# # 		comp_code=mycompany.id

# # 		ourcompany=tblCOMPANY.objects.get(id=comp_code)
# # 		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


# # 		if staff.thrift3b_cashier==0:
# # 				return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})


# # 		if request.method == 'POST':
# # 			email=request.POST['email']
# # 			p=[]

# # 			try :
# # 				memstaff = tblSTAFF.objects.get(branch=mybranch,email=email)
# # 				lln=tblIIIIbliabilities_authorization.objects.get(staffrec=memstaff,branch=mybranch,
# # 					status='Running')

# # 				ltrans = tblIIIbloantransaction.objects.filter(transaction_source=lln)

# # 				for k in ltrans:
# # 					month= k.start_date
# # 					year,month,day=month.split('-')
# # 					year=str(year)
# # 					month =str(month)
# # 					month =int(month)
# # 					monthnam = calendar.month_name[month]
# # 					det = {'month':monthnam, 'year':year,'amount':k.amount,'status':k.status,'id':k.id}
# # 					p.append(det)

# # 				return render(request,'IIIb/repay_hist.html',{'name':memstaff,'email':email,'company':mybranch,'user':varuser,'p':p})

# # 			except:

# # 				msg='no loan to repay'

# # 				return render(request,'IIIb/repay1.html',{'company':mybranch,'user':varuser,'msg':msg})

# # 		else:
# # 			msg = ''
# # 			return render(request,'IIIb/repay1.html',{'company':mybranch,'user':varuser,'msg':msg})

# # 	else:
# # 		return HttpResponseRedirect('/login/user/')


# @csrf_exempt
# def optionx(request):
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#     	if request.method == 'POST':
#     		post = request.POST.copy()
#     		acccode = post['userid']
#     		acccode,email=acccode.split(':')
#     		myloan=tblIIIbloantransaction.objects.get(id=acccode)
#     		mydate = int(myloan.start_date.split('-')[1])
#     		monthnam = calendar.month_name[mydate]

#     		return render(request,'IIIb/repayopt.html',{'code':acccode,'hhh':myloan,'date':monthnam,'email':email})
#     	else:
#     		return HttpResponseRedirect('/login/user/')
#     else:
#     	return HttpResponseRedirect('/login/user/')


# def yesrepayloan(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		staff = Userprofile.objects.get(email=varuser,status=1)

# 		staffdet=staff.staffrec.id
# 		branch=staff.branch.id

# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id
# 		ourcompay=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(id=branch)
# 		f= datetime.today()
# 		mday=f.day
# 		mmonth = f.month
# 		myear=f.year
# 		fdate=date(myear,mmonth,mday)

# 		if staff.thrift3b_cashier==0 or staff.thrift3b_admin==0 or staff.thrift3b_officer==0:
# 			return render(request,'IIIb/404.html',{'company':mybranch, 'user':varuser})

# 		if request.method == 'POST':
# 			email =request.POST['email']
# 			loan_code=request.POST['myid']
# 			myloan=tblIIIbloantransaction.objects.get(id= loan_code)
# 			myloan.status="CR"
# 			myloan.save()
# 			y,m,d =myloan.start_date.split("-")
# 			month = calendar.month_name[int(m)]
# 			email=[email]

# 			sendMailrepayloan(email,mmonth,y)

# 			soou = myloan.transaction_source.id
# 			loandet = tblIIIIbliabilities_authorization.objects.get(id=soou)

# 			myloancount=tblIIIbloantransaction.objects.filter(transaction_source=loandet, status="DR")

# 			if myloancount.count() < 1:
# 				tblIIIIbliabilities_authorization.objects.filter(status='Running').update(status= 'Fully Paid')
# 				sendMailfullypaid(email)
# 			return HttpResponseRedirect('/dashboard/')

# 		else:
# 			return HttpResponseRedirect('/dashboard/')

# 	else:
# 		return HttpResponseRedirect('/login/user/')


















# #***********************####  ACCOUNT BALANCE************************

# 		if request.method == 'POST':
# 			form = loanreqform(request.POST)
# 			if form.is_valid():

# 				thrift=request.POST['thrift']
# 				amount= request.POST['amount']
# 				package=request.POST['package']
# 				repay=request.POST['repay']

# 		else:
# 			form = loanreqform()
# 			# f=tblIIIbcommapplications.objects.get(branch=mybranch,staffrec=coop)

# 			if staff.thrift3b_admin==1:
# 				return render(request,'IIIb/recq_com_admin.html',{'company':mybranch,
# 					'name':find_staff,'user':varuser,'form':form})


# 	else:
# 		return HttpResponseRedirect('/login/user/')
