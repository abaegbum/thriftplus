from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json



from num2words import num2words
from django.db.models import Max,Sum


from sms.models import *
from sysadmin.models import *
from sms.forms import*
from sms.utils import*
import requests



from Ia.models import *
from Ia.utils import *

from customer.forms import *
from calendar import monthrange


from datetime import *
import calendar
import random



def wellw(request):
	if  "userid" in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		all_cust = tblCUSTOMER.objects.filter(branch=mybranch)

		for k in all_cust:
			try:
				tblIaCUSTOMER.objects.get(customer=k)
				k.dc=1
				k.save()
			except:
				msg = 0

			for k in all_cust:
				try:
					tblIbCUSTOMER.objects.get(customer=k)
					k.ivb=1
					k.save()
				except:
					msg = 0

		msg= 'coming up next'
		# return render(request,'Ia/selectloan.html',{'varuser':varuser,'msg':msg})
		return render(request,'sms/selectloan.html',{'varuser':varuser,'msg':msg})
	else:
		return HttpResponseRedirect('/login/')


def well(request):
	if 'userid' in request.session:
		varuser = request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		branch_code=staff.branch.code
		mybranch=tblBRANCH.objects.get(code= branch_code)

		d=tblIathrift.objects.all()
		d.delete()




		if staff.ceo==0:
			return render(request,'404.html',{'company':mybranch, 'user':varuser})

		if request.method=='POST':

			amount=request.POST['amount']
			return render(request,'sms/funding.html',{'company':mybranch,'user':varuser,'amount':amount})

		
		else:
			buy = tblsmstrans.objects.filter(branch=mybranch)

			if buy.count() == 0:
				amount = 0

			else:

				df = [a.id for a in buy]
				buy=buy.get(id=df[-1])
				amount=buy.balance

			return render(request,'sms/buy_sms.html',{'company':mybranch,'user':varuser,'amount':amount})

	else:
		return HttpResponseRedirect('/login/')

def fundingdetails(request):
	if 'userid' in request.session:
		varuser = request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		branch_code=staff.branch.code
		mybranch=tblBRANCH.objects.get(code= branch_code)

		if staff.ceo==0:
			return render(request,'404.html',{'company':mybranch, 'user':varuser})



		if request.method=='POST':
			amount=int(request.POST['amount'])


			balance_data = get_termii_balance()

			# msg=f'{balance_data['balance']},{amount}'

			if balance_data['balance'] > amount:
				acc1=6836703720#, wema bank
				acc2=5306792616#, sterling bank
				msg=f'{acc1} show me thriftplus account'
			else:
				msg='show me termii account'

			return render(request,'sms/paydetails.html',{'company':mybranch,'user':varuser,'amount':msg})

		
		else:
			return render(request,'sms/buy_sms.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/')



def sms_customer(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		# if staff.thrift_officer==0:
		if staff.ceo==0:
				return render(request,'404cr.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render(request,'404cr.html',{'company':mybranch, 'user':varuser})

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,status=1)
					form= smsform()
					return render(request,'sms/sms_reg.html',{
						'company':mybranch,
						'form':form,
						'user':varuser,
					'customer':details,
					'wallet':mywallet})

				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
		return render(request,'sms/sms.html',{
			'company':mybranch,
			'user':varuser,
			'form':form,
			'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def sms_history(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			app,package,user,wallet=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			if app== '-----' :
				msg = 'Select Category'
				return render(request,'sms/selectloan.html',{'msg':msg})

			if package == '-----' :
				msg = 'Select SMS Package'
				return render(request,'sms/selectloan.html',{'msg':msg})

			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)
			tbt = tblcustomersms.objects.filter(branch=mybranch,customer=customer)
			tbt__count = tbt.count()

			if tbt__count > 0 :
				ms=5
				all_sch = tblcustomersms.objects.get(branch=mybranch,customer=customer)
				schh = all_sch.S  #periodicity-----trans,week,month

				if schh=='trans':
					olschedule = tblcustomersmsperiodicity_transaction.objects.get(schedule=all_sch)
					olschedule= str(olschedule.alert_type)

				elif schh	== 'week' :
					olschedule=tblcustomersmsperiodicity_weekly.objects.get(schedule=all_sch)
					olschedule=str(olschedule.day_of_week)
					olschedule='weekly',olschedule

				elif schh == 'month' :
					olschedule=tblcustomersmsperiodicity_monthly.objects.get(schedule=all_sch)
					olschedule=str(olschedule.date_of_delivery)
					olschedule='monthly', olschedule
			else :
				ms = 1
				olschedule=''

			if app == 'Daily Contribution' :

				if package == 'Transactional' :
					if ms == 5 :
						try :
							my_schedule = tblcustomersmsperiodicity_transaction.objects.get(schedule=all_sch)
							schedule= str(my_schedule.alert_type)

							msg = 'your current preferrence is', schedule, ' Select other options to change'


							if  schedule=='Deposit':

								return render(request,'sms/transactional_rec.html',{
									'app':app,
									'wallet':wallet,
									'msg':msg,
									'schedule':schedule})

							elif schedule =='Withdraw':
								return render(request,'sms/transactional_withdraw.html',{
									'app':app,
									'wallet':wallet,
									'msg':msg,
									'schedule':schedule})

							elif schedule =='Both' :
								return render(request,'sms/transactional_both.html',{
									'app':app,
									'wallet':wallet,
									'msg':msg,
									'schedule':schedule})
						except:
							if schh=='week':
								hist ='weekly'
							elif schh=='month' :
								hist = 'monthly'

							msg ="Your current schedule is",  hist," Select from alert type to change"
					else :
						msg = 'No schedules found, select alert type to begin'

					return render(request,'sms/transactional.html',{
								'msg':msg,
								'app':app,
								'wallet':wallet})

				if package == 'Weekly' :
					if ms == 5 :
						if schh =='trans' :
							mysch = tblcustomersmsperiodicity_transaction.objects.get(schedule=all_sch)
							msg = str(mysch.alert_type)
							msg ="Your current schedule is", msg ," Select day of week to change"

						elif schh== 'week' :
							mysch=tblcustomersmsperiodicity_weekly.objects.get(schedule=all_sch)
							msg= str(mysch.day_of_week)
							msg ='Your current schedule is ', msg ,' Select day of week to change'
						else :
							msg ='Your current schedule is monthly. Select day of week to change'

					else :
						msg = 'No schedules found. Select day of week to begin'

					return render(request,'sms/weekly.html',{
						'user':user,
						'app':app,
						'msg':msg,
						'wallet':wallet})

				if package == 'Monthly' :

					if ms == 5 :
						try :
							mysch = tblcustomersmsperiodicity_monthly.objects.get(schedule=all_sch)
							schedule = str(mysch.date_of_delivery)

							if schedule== '2021-02-01' :
								msg ='Your current schedule is Firs of every month. Select your prefered delivery date to change'
								return render(request,'sms/monthly_first.html',{
									'app':app,
									'wallet':wallet,
									'msg':msg,
									'schedule':schedule})

							elif schedule == '2021-02-15':
								msg ='Your current schedule is mid month. Select your prefered delivery date to change'
								return render(request,'sms/monthly_mid.html',{
									'app':app,
									'wallet':wallet,
									'msg':msg,
									'schedule':schedule})

							elif schedule =='2021-07-29' :
								msg ='Your current schedule is month end. Select your prefered delivery date to change'
								return render(request,'sms/monthly_end.html',{
									'app':app,
									'wallet':wallet,
									'msg':msg,
									'schedule':schedule})

						except:
							if schh == 'trans' :
								histr = 'transactional'
							elif schh == 'week' :
								histr = 'weekly'
							msg ="Your current schedule is",  histr,", Select from alert type to change"

					else :
						msg = 'No schedules found. Select date of delivery to begin'

				return render(request,'sms/monthly_sms.html',{
								'user':user,
								'app':app,
								'msg':msg,
								'wallet':wallet
								})

			else:
				msg = 'No schedules Available'
				return render(request,'sms/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect('/login/')


def transactional(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift_officer==0:
				return render(request,'404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			schedule = request.POST['schedule']
			wallet = request.POST['wallet']
			app = request.POST['app']

			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)
			tbt = tblcustomersms.objects.filter(
				branch=mybranch,
				customer=customer)

			tbt__count = tbt.count()

			if tbt__count > 0 :
				ms=5
				all_sch = tblcustomersms.objects.get(branch=mybranch,customer=customer)
				schh = all_sch.S

			else :
				ms =1

			if ms == 5 :

				if schh == 'trans' :

					ssch = tblcustomersmsperiodicity_transaction.objects.get(schedule=all_sch)
					old = ssch.alert_type
					ssch.alert_type =  schedule
					ssch.save()
					new = schedule

				elif schh== 'week' :
					ssch = tblcustomersmsperiodicity_weekly.objects.get(schedule=all_sch).delete()
					ssch = tblcustomersmsperiodicity_transaction(schedule=all_sch,alert_type=schedule).save()
					all_sch.S = 'trans'
					all_sch.save()
					old= 'weekly'

				elif schh == 'month' :
					ssch = tblcustomersmsperiodicity_monthly.objects.get(schedule=all_sch).delete()
					ssch = tblcustomersmsperiodicity_transaction(schedule=all_sch,alert_type=schedule).save()
					all_sch.S = 'trans'
					all_sch.save()
					old = 'monthly'

				if schh != 'trans' :
					new = 'transactional'

				return render(request,'sms/transactional_edit_success.html',{
					'company':mybranch,
					'user':varuser,
					'old':old,
					'new':new,
					'wallet':wallet})

			elif ms ==1 :

				tblcustomersms(branch=mybranch,
					customer=customer,
					App =app,
					S = 'trans',
					balance = 0).save()

				tblcustomersms123 = tblcustomersms.objects.get(
					App=app,
					branch=mybranch,
					S = 'trans',
					customer=customer)

				tblcustomersmsperiodicity_transaction(
					schedule=tblcustomersms123,
					alert_type=schedule).save()

				return render(request,'sms/sub_success.html',{'company':mybranch,'user':varuser,'wallet':wallet})

	else:
		return HttpResponseRedirect('/login/')


def weeklysms(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift_officer==0:
				return render(request,'404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			dayofweek = request.POST['dayofweek']
			wallet = request.POST['wallet']
			app = request.POST['app']

			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)

			yhy = tblcustomersms.objects.filter(
				branch=mybranch,
				customer=customer,
				App =app)

			count_yhy = yhy.count()

			if count_yhy < 1 :
				tblcustomersms(branch=mybranch,
					customer=customer,
					App =app,
					balance = 0).save()
				mywk = tblcustomersms.objects.get(branch=mybranch,
					customer=customer,
					App =app,
					balance = 0)
				tblcustomersmsperiodicity_weekly(
					schedule=mywk,
					day_of_week = dayofweek).save()
				mywk.S='week'
				mywk.save()

				return render(request,'sms/sub_success.html',{
					'company':mybranch,
					'user':varuser,
					'wallet':wallet})

			else:
				yhy = tblcustomersms.objects.get(
				branch=mybranch,
				customer=customer,
				App =app)
				sccch= yhy.S

				if sccch == 'trans' :
					trans = tblcustomersmsperiodicity_transaction.objects.get(
						schedule=yhy)
					old='transactional'
					trans.delete()
					tblcustomersmsperiodicity_weekly(schedule=yhy,day_of_week=dayofweek).save()
					yhy.S='week'
					yhy.save()
					new='weekly'

				elif sccch == 'week' :
					tgt=tblcustomersmsperiodicity_weekly.objects.get(schedule=yhy)
					old = tgt.day_of_week
					tgt.day_of_week=dayofweek
					tgt.save()
					new = tgt.day_of_week

				elif sccch== 'month':
					mmnt= tblcustomersmsperiodicity_monthly.objects.get(schedule=yhy).delete()
					old='monthly'
					tblcustomersmsperiodicity_weekly(schedule=yhy,day_of_week=dayofweek).save()
					yhy.S='week'
					yhy.save()
					new ='weekly'

				return render(request,'sms/transactional_edit_success.html',{
					'company':mybranch,
					'user':varuser,
					'old':old,
					'new':new,
					'wallet':wallet})


	else:
		return HttpResponseRedirect('/login/')


def monthlysms(request):
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

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift_officer==0:
				return render(request,'404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			dateofdel = request.POST['dateofdel']
			wallet = request.POST['wallet']
			app = request.POST['app']


			if dateofdel == 'start' :
				dateofdel=date(2021,2,1)
				nick='First'
			elif dateofdel=='mid' :
				dateofdel=date(2021,2,15)
				nick='Mid Month'
			elif dateofdel== 'end' :
				dateofdel=date(2021,7,29)
				nick='Month End'


			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)

			yhy = tblcustomersms.objects.filter(
				branch=mybranch,
				customer=customer,
				App =app)

			count_yhy = yhy.count()

			if count_yhy < 1 :
				tblcustomersms(branch=mybranch,
					customer=customer,
					App =app,
					S= 'month',
					balance = 0).save()
				mywk = tblcustomersms.objects.get(branch=mybranch,
					customer=customer,
					App =app,
					S='month',
					balance = 0)
				tblcustomersmsperiodicity_monthly(
					schedule=mywk,
					nick = nick,
					date_of_delivery = dateofdel).save()


				return render(request,'sms/sub_success.html',{
					'company':mybranch,
					'user':varuser,
					'wallet':wallet})

			else: #record exist
				yhy = tblcustomersms.objects.get(
				branch=mybranch,
				customer=customer,
				App =app)
				sccch= yhy.S

				if sccch == 'trans' :
					trans = tblcustomersmsperiodicity_transaction.objects.get(
						schedule=yhy)
					old='Transactional'
					trans.delete()
					tblcustomersmsperiodicity_monthly(schedule=yhy,
						date_of_delivery =dateofdel,
						nick=nick).save()
					yhy.S='month'
					yhy.save()
					new ="monthly"

				elif sccch == 'week' :
					tgt=tblcustomersmsperiodicity_weekly.objects.get(schedule=yhy)
					old = 'weekly'
					tgt.delete()
					tblcustomersmsperiodicity_monthly(schedule=yhy,
						date_of_delivery=dateofdel,
						nick=nick).save()
					yhy.S='month'
					yhy.save()
					new ='monthly'

				elif sccch== 'month':

					mmnt= tblcustomersmsperiodicity_monthly.objects.get(schedule=yhy)
					old=mmnt.nick

					mmnt.date_of_delivery=dateofdel
					mmnt.nick=nick
					mmnt.save()

					mmnt= tblcustomersmsperiodicity_monthly.objects.get(schedule=yhy)
					new = mmnt.nick



				return render(request,'sms/transactional_edit_success.html',{
					'company':mybranch,
					'user':varuser,
					'old':old,
					'new':new,
					'wallet':wallet})


	else:
		return HttpResponseRedirect('/login/')



def sms_purchase(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.ceo==0:
			return render(request,'404cr.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render(request,'404cr.html',{
				'company':mybranch,
				'user':varuser})

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				smslist=[]

				try:
					customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,
						status=1)
					smsdetails = tblcustomersms.objects.get(branch=mybranch,
						customer=customer)

					bus= tblsmsappbusiness.objects.filter(branch=mybranch,
						status=1,App='Daily Contribution')

					if bus.count() > 0:
						myform = thriftform()
						bus= tblsmsappbusiness.objects.get(branch=mybranch,
						status=1,App='Daily Contribution')

						smsdic= {'balance':smsdetails.balance,
						'wallet':mywallet,
						'sender':bus.sender_ID,
						'surname':customer.surname,
						'firstname':customer.firstname,
						'othername':customer.othername}
						smslist.append(smsdic)

						return render(request,'sms/pay_sms.html',{'company':mybranch,
							'user':varuser,
							'wallet':mywallet,
							'smslist':smslist,
							})
					else:
						msg='hello, you have not subscribed for this service'
				except:
					msg='you havent subscribed for this service'
			else:
				msg='Incorrect entry'
		else:
			form=viewwalletform()
			msg = ''
		return render(request,'sms/buy_sms.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def unit(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			unit,user,wallet,amount=acccode.split(':')

			if unit != '' :
				unit= int(unit)

			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			sms_bal = tblsmsappbusiness.objects.get(status=1,branch=mybranch, App='Daily Contribution')
			balance=int(sms_bal.balance)

			if unit == '' :
				msg = 'enter sms unit'
				return render(request,'sms/selectloan.html',{'msg':msg})

			if balance - unit < 0 :
				msg = 'Sms Unit too large. Try reducing the unit of sms'
				return render(request,'sms/selectloan.html',{'msg':msg})

			else :
				form=thriftform()
				return render(request,'sms/funding.html',{'form':form,
					'unit':unit,
					'user':user,
					'amount':amount,
					})

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def pay4sms(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']

			funding,month,account_type,user,amount,unit,wallet = acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)


			if funding== '-----':
				msg = 'Select a funding source'
				return render(request,'sms/selectloan.html',{'msg':msg})

			if month== '-':
				msg = 'Select a month'
				return render(request,'sms/selectloan.html',{'msg':msg})

			if account_type== '-----' :
				msg = 'Select account type'
				return render(request,'sms/selectloan.html',{'msg':msg})


			if funding == 'Daily Contribution':
				money = tblthrift_trans.objects.filter(branch=mybranch,
					account_type=account_type,
					customer=customer,
					avalability='Available',
					reason='Available',
					recdate__month=month)

				if money.count() > 0 :
					add=money.aggregate(Sum('amount'))
					add = add['amount__sum']

					if int(add) - int(amount) > 0:

						return render(request,'sms/submit.html',{'funding':funding,
							'month':month,
							'account':account_type,
							'user':user,
							'unit':unit,
							'amount':amount,
							'wallet':wallet})

					else :
						amount=int(amount)
						msg = 'you have', add , 'but needs ', amount , ' for this transaction'
						return render(request,'sms/selectloan.html',{'msg':msg})


				else :
					msg = 'No record found. Try selecting another month / account type'
					return render(request,'sms/selectloan.html',{'msg':msg})


			else :
				msg='Cash funding not allowed'
				return render(request,'sms/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/dalogin/')



def buysms(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.ceo==0:
			return render(request,'404cr.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render(request,'404cr.html',{'company':mybranch, 'user':varuser})

		msg=memmerchant.id
		return render(request,'sms/selectloan.html',{'msg':msg})

		if request.method == 'POST':
			amount=request.POST['amount']
			unit=request.POST['unit']
			wallet=request.POST['wallet']

			month=request.POST['month']
			account=request.POST['account']
			user=request.POST['user']
			funding=request.POST['funding']

			unit=int(unit)

			fdate= datetime.today()

			month=fdate.month #in figures
			year=fdate.year
			dayy = fdate.day
			oydate=date(year,month,dayy)

			customer= tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1,
				merchant=memmerchant)

			bus_sms = tblsmsappbusiness.objects.get(branch=mybranch,
				status=1)

			sms_balance = int(bus_sms.balance)

			sms_bal= sms_balance - unit

			bus_sms.balance = sms_bal

			bus_sms.save()

			cus_sms =tblcustomersms.objects.get(branch=mybranch,
				customer=customer,
				App=funding)

			old_bal = int(cus_sms.balance)
			new_bal = old_bal + unit
			cus_sms.balance = new_bal

			cus_sms.save()

			merchant=memmerchant.id

			tblcustomersmspurchases(branch=mybranch,
				customer=customer,
				recdate = oydate,
				merchant=merchant,
				volume = unit,
				status='Unpaid',
				cost = amount).save()

			nn=unit+old_bal




			return render(request,'sms/sms_purchase_successful.html',{
				'account_type':account,
				'company':mybranch,
				'user':varuser,
				'wallet':wallet,
				'thrift':unit,
				 'nn':nn,
				'amount':amount})

		else :
			# return HttpResponseRedirect('/sms/daily_contribution/requests/buysms/')
			return HttpResponseRedirect('/sms/daily_contribution/balance/')

	else:
		return HttpResponseRedirect('/login/')




@csrf_exempt
def cussms(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			wallet = acccode

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.code


			mybranch=tblBRANCH.objects.get(code=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':user})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1)

			ccc=tblIaCUSTOMER.objects.get(customer=details)



			if details.phone == '':
				msg = f"Phone number not found. Click on {details.surname}  {details.firstname}'s profie to enter it"
				return render(request,'Ia/selectloan.html',{'msg':msg})


			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


			g = tblapp.objects.get(branch=mybranch)

			try:
				buy= tblsmscustmertrans.objects.filter(branch=mybranch,	customer=ccc)
				df = [a.id for a in buy]
				buy=buy.get(id=df[-1])
				amount=buy.balance
			except:
				amount=0



			buy = tblsmstrans.objects.filter(branch=mybranch)
			if buy.count()>0:
				df = [a.id for a in buy]
				sms_balance =buy.get(id=df[-1])

				gv = tblproductsname.objects.filter(branch=mybranch)
				ff = tblmyproducts.objects.filter()
				if gv.count() ==0:
					msg = 'You havent set names for your products'
					return render(request,'Ia/selectloan.html',{'msg':msg})
				else:

					return render(request,'sms/mysms.html',
						{
						'merchant':memmerchant,
						'user':varuser,
						'customer':details,
						'wallet':wallet,
						'naam':gv,
						'year':yy,
						'sub':g,
						'sta':ff,
						'balance':amount,
						'prod':gv,
						'company':mybranch,
						'id':mybranch.id,
						'sms_balance':sms_balance,
						'user':staff})

			else:
				msg= f"Bulk sms balance is 0"
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



def save_smsoptions(request):
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

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,   staff=memstaff,status=1, thrift1a=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)



		if request.method == 'POST':

			amount = int(request.POST['amount'])

			wallet=request.POST['wallet']
			customer=tblCUSTOMER.objects.get(wallet=wallet)
			cus2=tblIaCUSTOMER.objects.get(customer=customer)

			wors = num2words(int(amount))



			compsms = tblsmstrans.objects.filter(branch= mybranch)
			uy= [x.id for x in compsms]
			compsms=compsms.get(id=uy[-1])
			sms_balance = int(compsms.balance)



			if sms_balance > amount:
				year=request.POST['myyear']

				return render(request,'sms/smsdisplay.html',{'company':mybranch,
					'customer':cus2,
					'user':varuser,
					'wallet':wallet,
					'amount':amount,
					'words':wors })
			else:
				msg = 'insufficient sms balance,Contact Admin'

				return render(request,'sms/selectloan2.html',{'msg':msg})



		else:
			return HttpResponseRedirect('/fts/mycustomers/dashboard/+ wallet /')
	else:
		return HttpResponseRedirect('/login/user/')



def save_sms(request):
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

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,   staff=memstaff,status=1, thrift1a=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)



		if request.method == 'POST':

			amount = int(request.POST['amount'])

			wallet=request.POST['wallet']
			customer=tblCUSTOMER.objects.get(wallet=wallet)
			cus2=tblIaCUSTOMER.objects.get(customer=customer)



			compsms = tblsmstrans.objects.filter(branch= mybranch)
			uy= [x.id for x in compsms]
			compsms=compsms.get(id=uy[-1])

			sms_balance = int(compsms.balance)



			if sms_balance > amount:
				sms_trans_id = generate_trans_pin()

				fdate= datetime.today()
				ddate = fdate.date()
				ttime= fdate.time()


				sms_trans =  tblsmscustmertrans.objects.filter(branch=mybranch,	customer=cus2)


				sms = tblsmscustmerbuy.objects.filter(branch=mybranch,customer=cus2,date=ddate,amount=amount)

				if sms.count() == 0:

					tblsmscustmerbuy(branch=mybranch,
						amount= amount,
						merchant=memmerchant,
						customer=cus2,
						credited_status=False,
						sms_trans_id= sms_trans_id,
						date=ddate,	time=ttime).save()

				
				
				sms2 = sms.get()
				sms_credit  = sms_trans.filter(sms_trans_id= sms2.sms_trans_id)

				if sms_credit.count() == 0:
					if sms_trans.count() == 0:#first time purchase
						balance_before=0
						balance_after=amount
						balance= int(balance_before) + int(balance_after)

						
					else: # other purchases

						uy= [x.id for x in sms_trans]
						sms_history=sms_trans.get(id=uy[-1])

						
						balance_before=sms_history.balance
						balance_after=amount
						balance= int(balance_before) + int(balance_after)


					tblsmscustmertrans(branch=mybranch,
						customer=cus2,
						balance=balance,
						balance_before=balance_before,
						balance_after=balance_after,
						sms_trans_id= sms2.sms_trans_id,
						date=ddate,	time=ttime).save()


					df = sms.get(sms_trans_id=sms2.sms_trans_id)
					df.credited_status=True
					df.save()


					#deduct from sms volume of the branch

					balance_before=  compsms.balance
					balance_after= amount
					balance= int(balance_before) - balance_after

					tblsmstrans(branch=mybranch,
						balance=balance,
						balance_before=balance_before,
						balance_after =balance_after,
						sms_trans_id= sms_trans_id,
						date=ddate,
						time=ttime).save()

					
					msg = f'Your SMS purchase of {amount} was sucessfull'


				else:
					msg = f'you already purchased sms {amount} today'


			else:
				msg = 'sms balance too low' 


			return render(request,'sms/prodsucc.html',{'company':mybranch,
				'customer':cus2,
				'msg':msg,'wallet':wallet,'user':varuser})
		else:
			return HttpResponseRedirect('/fts/mycustomers/dashboard/'+ wallet +"/")
			
	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def cussmsactive(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			wallet = acccode

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.code


			mybranch=tblBRANCH.objects.get(code=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':user})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1)

			ccc=tblIaCUSTOMER.objects.get(customer=details)

			if details.phone == '':
				msg = f"Phone number not found. Click on {details.surname}  {details.firstname}'s profie to enter it"
				return render(request,'Ia/selectloan.html',{'msg':msg})



			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


			g = tblapp.objects.get(branch=mybranch)


			buy = tblsmstrans.objects.filter(branch=mybranch)
			if buy.count()>0:
				try:
					buy= tblsmscustmertrans.objects.filter(branch=mybranch,	customer=ccc)
					df = [a.id for a in buy]
					buy=buy.get(id=df[-1])
					amount=buy.balance
				except:
					amount=0


				apps = tblIaSMS.objects.filter(branch=mybranch, customer=ccc)

				if apps.count() ==0:
					tblIaSMS(branch=mybranch,customer=ccc).save()

				apps=apps.get()

				gv = tblproductsname.objects.filter(branch=mybranch)
				ff = tblmyproducts.objects.filter()
				if gv.count() ==0:
					msg = 'You havent set names for your products'
					return render(request,'Ia/selectloan.html',{'msg':msg})
				else:

					return render(request,'sms/myalert.html',
						{
						'company':mybranch,
						'sub':g,
						'merchant':memmerchant,
						'client':apps,
						'customer':details,
						'user':varuser,					
						'wallet':wallet,
						'naam':gv,
						'year':yy,
						
						'sta':ff,
						'balance':amount,
						'prod':gv,					
						'id':mybranch.id,
						'user':staff})

			else:
				msg= f"Bulk sms balance is 0"
				return render(request,'Ia/selectloan.html',{'msg':msg})



		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def save_smsactive(request):
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

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,   staff=memstaff,status=1, thrift1a=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)



		if request.method == 'POST':

			email = request.POST['email']

			year=request.POST['myyear']
			wallet=request.POST['wallet']
			customer=tblCUSTOMER.objects.get(wallet=wallet)
			cus2=tblIaCUSTOMER.objects.get(customer=customer)



			sms_trans_id = generate_trans_pin()

			fdate= datetime.today()
			ddate = fdate.date()
			ttime= fdate.time()

			cp = tblIaSMS.objects.get(branch=mybranch, customer=cus2)


			cp.esusu1a = 'esusu1a' in request.POST
			cp.esusu1aloan = 'esusu1aloan' in request.POST
			cp.savings1a = 'savings1a' in request.POST
			cp.loans1acash = 'loans1acash' in request.POST
			cp.loans1aitems = 'loans1aitems' in request.POST
			cp.fixeddepo1a = 'fixeddepo1a' in request.POST
			cp.targetsave1a = 'targetsave1a' in request.POST
			cp.ecomerce = 'ecomerce' in request.POST
			cp.thrift3b = 'thrift3b' in request.POST
			cp.save()

			msg = 'Service saved successfully'


			return render(request,'sms/prodsucc.html',{'company':mybranch,
				'customer':cus2,
				'msg':msg,'wallet':wallet,'user':varuser})
		
		else:
			return HttpResponseRedirect('/fts/mycustomers/dashboard/+ wallet /')
	else:
		return HttpResponseRedirect('/login/user/')

