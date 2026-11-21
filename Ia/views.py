from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json


from thriftplus.settings import EMAIL_HOST_USER

from django.core.mail import send_mail


from sysadmin.models import *
from customer.models import *


from thriftplus.utils import *

from Ia.models import *
from Ia.utils import *
from Ia.forms import *

from num2words import num2words
from datetime import *


import calendar
from calendar import monthrange


from django.db.models import Max,Sum

import random

# import customer.utils

from customer.utils import *


# from django.contrib.sessions.models import Session
# Session.objects.all().delete()


# import south.models
# # MigrationHisory.objects.all().delete()

# import south
# from south.models import *
# MigrationHistory.objects.all().delete()






####CUSTOMER DAHBOARD S*****************************

def straighttocus(request):   ##DIRECT*************************
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




		if request.method=='POST':
			wallet = request.POST['wallet']

			return HttpResponseRedirect('/fts/mycustomers/dashboard/'+ wallet +"/")

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')




def cusboard(request,vid):  ##aINDIRECT*************************



	if  "userid" in request.session:
		varuser = request.session['userid']


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

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1).count()

		cuscus = tblCUSTOMER.objects.filter(branch=mybranch,wallet= vid)

		g = tblapp.objects.get(branch=mybranch)

		if cuscus.count()==1:
			getdetails=cuscus.get()
			getdetails = tblIaCUSTOMER.objects.get(customer=getdetails)

			return render(request,'Ia/cccccc.html',{'company':mybranch,
				'user':varuser,'getdetails':getdetails,'vid':vid,'staff':staff})
		else:
			msg='wrong wallet address'


			return render(request,'Ia/cccccc2.html',{'company':mybranch, 'user':varuser,'msg':msg})


	else:
		return HttpResponseRedirect('/login/user/')




####HOW IT WORKS*****************************



def adminuserguide_delete_BackOffice(request):


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


		if staff.ceo==1:
			return render(request,'Ia/howitworks.html',{'company':mybranch, 'user':varuser})
			# return render(request,'Ia/howitworks.html',{'company':mybranch, 'user':varuser,'cut':ppp})


		elif staff.thrift_officer==1:
			return render(request,'Ia/howitworks_t.html',{'company':mybranch, 'user':varuser})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')





####CREDIT OFFICERS****************
def regfieldagent(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')


		staffdet=staff.staffrec.id
		branch_code=staff.branch.code
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,code=branch_code)

		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		mystafflist = tblSTAFF.objects.filter(status=1, branch=mybranch).count()


		if request.method== 'POST':
			form = fieldofficerfform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']
				mystaff = tblSTAFF.objects.filter(email=email,status=1, branch=mybranch) #check status
				mycount=mystaff.count()

				if mycount == 1: #user is a staff
					querry_email = mystaff.get(email=email)
					g = tblapp.objects.get(branch=mybranch)


					gh = tblIaMERCHANT.objects.filter(branch=mybranch,status=True)
					gh_count=gh.count()

					appy = gh.filter(branch = mybranch,staff=querry_email,status=1)

					appy_count = appy.count()

					if appy_count == 1:
						apps = appy.get()

						myy =[]

						if apps.esusu1a is True:
							esu= 'checked'

						else:
							esu='unchecked'


						if apps.esusu1aloan is True:
							esuloan= 'checked'

						else:
							esuloan='unchecked'


						if apps.savings1a is True:
							sav= 'checked'
						else:
							sav='unchecked'


						if apps.loans1acash is True:
							loans= 'checked'
						else:
							loans='unchecked'

						if apps.loans1aitems is True:
							loansi= 'checked'
						else:
							loansi='unchecked'


						if apps.fixeddepo1a is True:
							fxd= 'checked'
						else:
							fxd='unchecked'

						if apps.targetsave1a is True:
							tagg= 'checked'
						else:
							tagg='unchecked'



						s= {'id':mybranch,
						'esu':esu,
						'esuloan':esuloan,
						'sav':sav,
						'loancash':loans,
						'loanitem':loansi,
						'tag':tagg,
						'fxd':fxd}

						myy.append(s)

						return render(request,'Ia/credit_activate_post.html',{
							'company':mybranch,
							'id':mybranch.id,
							'msg':querry_email,
							'products':g,
							'co':apps,
							'list':myy,
							'user':varuser})

					elif appy_count==0:


						history = checksub(mybranch,'Esusu')

						ddt = date.today()

						if history['status'] == 'Running':
							if ddt > history['stop'] :

								msg = 'you cannot proceed beyond this point, until you do something about your subscription'
								return render(request,'Ia/selectloan2.html',{'company':mybranch,'msg':msg})

							else:

								if int(gh_count) < int(history['staff_count']):
									form =fieldofficerfform()
									msg=''


									return render(request,'Ia/actCO2.html',{
										'company':mybranch,
										'id':mybranch.id,
										'msg':querry_email,
										'products':g,
										'user':varuser})


								else:
									msg= 'You have reached the maximum number of credit officer(s) allowed for your package'
									return render(request,'Ia/selectloan2.html',{'company':mybranch,'msg':msg})

						else:
							msg = 'you cannot proceed beyond this point, until you do something about your subscription'
							return render(request,'Ia/selectloan2.html',{'company':mybranch,'msg':msg})



				elif mycount == 0:
					msg = 'THIS EMAIL IS NOT REGISTERED'
					return render(request,'Ia/selectloan2.html',{'company':mybranch,'msg':msg})
			else:
				return HttpResponseRedirect('/fts/staff/merchant/')
				msg = 'INVALID ENTRY'



		else:

			form =fieldofficerfform()

			return render(request,'Ia/credit_activate_get.html',{
					'company':mybranch,
					'user':varuser,
					'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def services_update(request):

	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)


		if staff.ceo==0:
			return render(request,'partner/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST' :
			branch_code= request.POST['branch']
			email= request.POST['email']
			branch = tblBRANCH.objects.get(id=branch_code)
			staff= tblSTAFF.objects.get(email=email)

			######*****************#daily contribution*****************8

			sub = []

			ff =0


			if 'esu' in request.POST:
				esu=1
				ff=ff+ 1
				sub.append('Esusu')
			else:
				esu = 0


			if 'esuloan' in request.POST:
				esuloan=1
				ff=ff+ 1
				sub.append('Ajo Loan')
			else:
				esuloan = 0


			if 'sav' in request.POST:
				sav=1
				ff=ff+ 1
				sub.append('Savings')
			else:
				sav = 0




			if 'lc' in request.POST:
				lc=1
				ff=ff+ 1
				sub.append('Cash Loans')
			else:
				lc=0

			if 'li' in request.POST:
				li=1
				ff=ff+ 1
				sub.append('Items Loan')
			else:
				li=0


			if 'target' in request.POST:
				target=1
				ff=ff+ 1
				sub.append('Target Savings')
			else:
				target=0



			if 'fxd' in request.POST:
				fxd=1
				ff=ff+ 1
				sub.append('fixed Deposit')
			else:
				fxd=0

			if ff > 0:
				thrift1a=1
			else:
				thrift1a=0




			Userprofile.objects.filter(branch=branch,email=email).update(
				thrift1a=thrift1a,
				thrift_officer=1,

				esusu1a=esu,
				esusu1aloan=esuloan,


				savings1a=sav,
				loans1aitems=li,
				loans1acash=lc,

				fixeddepo1a=fxd,
				targetsave1a=target)



			hs=tblIaMERCHANT.objects.filter(branch=branch,staff =staff)
			hs_count = hs.count()

			if hs_count == 1:
				h = hs.get()

				h.esusu1a= esu
				h.esusu1aloan= esuloan


				h.savings1a= sav
				h.loans1acash= lc
				h.loans1aitems= li

				h.fixeddepo1a=fxd
				h.targetsave1a=  target
				h.save()

			elif hs_count ==0:

				tblIaMERCHANT(status=1,
					staff=staff,
					branch=branch,
					thrift1a=thrift1a,

					esusu1a= esu,
					esusu1aloan= esuloan,


					savings1a= sav,
					loans1acash= lc,
					loans1aitems= li,

					fixeddepo1a=fxd,
					targetsave1a=  target,

					code=generate_trans_pin()).save()


			try:
				register_field_officerIa(email)
			except:
				pass

			return render(request,'Ia/credit_activate_post2.html',{
				'company':branch,
				'msg':sub,
				'user':varuser})

		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')



def manageco(request):
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

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		meer = tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,status=1 )
		bp=[]



		for k in meer:
			mp = tblIalocations.objects.filter(merchant=k,branch=mybranch)
			h=[]
			myy=[]
			sdic={}

			if mp.count() > 0:
				for l in mp:
					j = str(l.location)
					g = {j:j}
					sdic.update(g)

				klist = sdic.values()
				for p in klist:
					h.append(p)
			else:
				p='N/A'
				h.append(p)


			if k.esusu1a is True:
				myy.append('Esusu')

			if k.savings1a is True:
				myy.append('Savings')


			if k.loans1acash is True:
				myy.append('Cash Loans')


			if k.loans1aitems is True:
				myy.append('Asset Loans')


			if k.fixeddepo1a is True:
				myy.append('Fixed Deposit')


			if k.targetsave1a is True:
				myy.append('Target Savings')


			h=f"{h[0]}"

			b={'location':h,'merchant':k,'product':myy}
			bp.append(b)



		return render(request,'Ia/credit_manage_get.html',
			{'company':mybranch, 'user':varuser,'merchant':bp})


	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def manpop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			fo,user=acccode.split(':')


			mn=tblIaMERCHANT.objects.get(id=fo)


			if mn.direc_credit ==1:
				dc=1
			else:
				dc=0

			if mn.direct_withdraw ==1:
				dw=1
			else:
				dw=0

			if mn.esusu1a == 1:
				esu =1
			else:
				esu = 0

			if  mn.esusu1aloan == 1:
				esloan =1
			else:
				esloan=0

			if mn.savings1a == 1:
				sav =1
			else:
				sav=0

			if mn.loans1acash == 1:
				loancash =1
			else:
				loancash=0

			if mn.loans1aitems ==1 :
				lotem =1
			else:
				lotem=0

			if mn.fixeddepo1a == 1:
				fxd =1
			else:
				fxd=0


			if mn.targetsave1a == 1 :
				tgs=1
			else:
				tgs=0




			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			mybranch=tblBRANCH.objects.get(id=staff.branch.id)
			k = tblbusinesslocations.objects.filter(branch=mybranch)

			mp = tblIalocations.objects.filter(merchant=mn)

			h=[]

			if mp:
				for l in mp:
					g=str(l.location)


			else:
				g=0

			h.append(g)


			return render(request,'Ia/credit_manage_name_pop.html',{
				'merchant':mn,'loc':h,
				'k':k})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')


def savepop(request): #customer - admin transaction
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

		if staff.admin==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			merc =request.POST['merchant']
			location =request.POST['location']


			if 'dc' in request.POST:
				dc=1
			else:
				dc=0

			if 'dw' in request.POST:
				dw=1
			else:
				dw=0


			merchant= tblIaMERCHANT.objects.get(id=merc)

			ceo = merchant.staff.ceo


			if ceo ==0:

				fo= tblIaMERCHANT.objects.filter(branch=mybranch,status=1)
				fo_count = int(fo.count())

				# sub = tblsubscription.objects.filter(branch=mybranch,app='DC')

				# if sub.count() == 1:
				# 	sub = sub.get()
				# else:
				# 	sub = sub.filter()[1]


				# standard_pack = int(sub.package.staff_count)


				if location != '-----':

					try:
						tblIalocations.objects.get(branch=mybranch,location=location,merchant=merchant)
					except:
						tblIalocations(branch=mybranch,location=location,merchant=merchant).save()

				tblIaMERCHANT.objects.filter(id=merc).update(direc_credit=dc,direct_withdraw=dw)

			return HttpResponseRedirect('/fts/staff/merchant/manage/')


		else:
			return HttpResponseRedirect('/fts/staff/merchant/manage/')
	else:
		return HttpResponseRedirect('/login/user/')

@csrf_exempt
def locpop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			fo,user=acccode.split(':')


			mn=tblIaMERCHANT.objects.get(id=fo)



			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			mybranch=tblBRANCH.objects.get(id=staff.branch.id)
			k = tblbusinesslocations.objects.filter(branch=mybranch)

			mp = tblIalocations.objects.filter(merchant=mn)


			return render(request,'Ia/credit_manage_loc_pop.html',{'merchant':mn,'loc':mp})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




def locdel(request,vid):


	if 'userid' in request.session:
		user=request.session['userid']

		staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		if staff.ceo ==1:
			k = tblIalocations.objects.get(branch=mybranch,id=vid)
			k.delete()

			return HttpResponseRedirect('/fts/staff/merchant/manage/')
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



def mycos(request):
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

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.admin==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		msg = ''

		meer = tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,status=1).order_by('status')

		if staff.admin == 1:
			return render(request,'Ia/credit_myco.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})


		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')




# ##********************customers****************************
def cus_list(request):
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
		gg=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1)
		memmerchant = gg.count()



		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant= gg.get()


		if staff.admin:
			cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch)
		else:
			cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch)
			# cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch,merchant=memmerchant)

		form = locationform()
		if staff.ceo==1:
			return render(request,'Ia/custlist.html',{'company':mybranch,'form':form, 'user':varuser,'client_list':cutlist})
		else:
			return render(request,'Ia/custlist_to.html',{'company':mybranch,'form':form, 'user':varuser,'client_list':cutlist})
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def ajaxcus_list(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				post = request.POST.copy()
				user = post['userid']
				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)
				staffdet=staff.staffrec.id
				branch=staff.branch.id
				mycompany=staff.branch.company
				comp_code=mycompany.id

				ourcompany=tblCOMPANY.objects.get(id=comp_code)
				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				data = tblbusinesslocations.objects.filter(branch=mybranch)

				new_list = []
				jk=[]

				for j in data:
					mk= j.location
					jk.append(mk)



				[new_list.append(item) for item in jk if item not in new_list] #remove repeatition from list

				if data.count() > 0:
					new_list.append('All')
				else:
					new_list.append('-----')

				return HttpResponse(json.dumps(new_list), content_type='application/json')

			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def adminlistajax(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			location,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)



			if location=='-----':
				g=0
				return render(request,'Ia/noloc.html',{'user':user,'location':location})

			else:
				if location=='All':

					data = tblCUSTOMER.objects.filter(branch=mybranch,status=True).order_by("surname","firstname","othername")
				else:
					data = tblCUSTOMER.objects.filter(branch=mybranch,location=location,status=True).order_by("surname","firstname","othername")

				gg=[]

				for hp in data:
					try:
						cutlistp = tblIaCUSTOMER.objects.get(customer=hp,status=True)
						gg.append(cutlistp)
					except:
						pass

				return render(request,'Ia/listcajax.html',{'dat':gg,'user':user,'location':location})


	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def ajaxcus_list2(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		  if request.method == 'POST':
			  varuser = request.session['userid']
			  post = request.POST.copy()
			  user = post['userid']
			  staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)
			  staffdet=staff.staffrec.id
			  branch=staff.branch.id
			  mycompany=staff.branch.company
			  comp_code=mycompany.id
			  ourcompany=tblCOMPANY.objects.get(id=comp_code)
			  mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			  mystaff=tblSTAFF.objects.get(branch=mybranch,email=user)

			  m2=tblIaMERCHANT.objects.get(branch=mybranch,staff=mystaff)

			  data = tblIalocations.objects.filter(branch=mybranch,merchant=m2)


			  jk=[]
			  jk.append('-----')

			  for j in data:
				  mk= j.location
				  jk.append(mk)


			  return HttpResponse(json.dumps(jk), content_type='application/json')

		  else:
			  gdata = ""
			  return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')

@csrf_exempt
def mylistajax(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			location,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company

			company=mycompany.name
			comp_code=mycompany.id

			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


			mystaff=tblSTAFF.objects.get(branch=mybranch,email=user)
			m2=tblIaMERCHANT.objects.get(branch=mybranch,staff=mystaff)
			data = tblIalocations.objects.filter(branch=mybranch,merchant=m2)

			if data.count() == 0:

				msg = ' Your list is empty because no location assigned to you yet. Contact admin'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if location=='-----':
				msg = 'Select Area'

				return render(request,'Ia/selectloan.html',{'msg':msg})

			elif location=='All':

				data = tblCUSTOMER.objects.filter(branch=mybranch)
			else:
				data = tblCUSTOMER.objects.filter(branch=mybranch,location=location)

			data=data.order_by('surname')
			gg=[]

			for hp in data:
				try:
					cutlistp = tblIaCUSTOMER.objects.get(customer=hp)
					gg.append(cutlistp)
				except:
					pass

			return render(request,'Ia/listcajax.html',{'dat':gg,'user':user,'location':location})


	else:
		return HttpResponseRedirect('/login/user/')






# #***********************GENERAL Thrift********************


def thriftrep(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.thrift_officer==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()


		try:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			monthname=request.POST['month'] #month in figures
			yyr=request.POST['myyear']



			thriftrec=tblIathrift.objects.filter(
				branch=mybranch,
				year=yyr,
				month=monthname).order_by('customer')
			g=[]

			for k in thriftrec:
				 customer = k.customer.id
				 g.append(customer)

			all_cus=[]
			cust=[]

			[all_cus.append(item) for item in g if item not in all_cus]

			for h in all_cus:
				df =tblIaCUSTOMER.objects.get(id=h)
				sales=thriftrec.filter(customer=h)

				ncr = sales.aggregate(Sum('service_charge'))
				add = int(ncr['service_charge__sum'])

				f = {'customer':df,'sales':add}
				cust.append(f)

			total = sum([d['sales'] for d in cust])


			return render(request,'Ia/thriftslog_post.html',{'company':mybranch,
				'user':varuser,
				'total':total,
				'thriftrec':cust,
				'year':yyr,
				'month':monthname})


		else:

			return render(request,'Ia/thriftslog_get.html',{'company':mybranch,'user':varuser,'year':yy})

	else:
		return HttpResponseRedirect('/login/user/')





# #***********************RECONCILOATION********************
def approval(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch_code=staff.branch.code
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		realdet = tblapp.objects.get(branch=mybranch)

		myy = []



		gb = tblproductsname.objects.filter(branch=mybranch)

		if realdet.esusu1a is True:
			hh= tblmyproducts.objects.get(product='Esusu')
			gb2=gb.get(product=hh)
			myy.append(gb2.your_product_name)




		if realdet.esusu1aloan is True:
			myy.append('Esusu Loan Repayent')



		if realdet.savings1a is True:
			hh= tblmyproducts.objects.get(product='Savings')
			gb2=gb.get(product=hh)
			myy.append(gb2.your_product_name)


		if realdet.loans1acash is True:
		   myy.append('Cash Loan Repayent')

		if realdet.loans1aitems is True:
			myy.append('Asset Loan Repayent')

		if realdet.fixeddepo1a is True:
			myy.append('Fixed Deposit')

		if realdet.targetsave1a is True:
			myy.append('Target Savings')




		if request.method == 'POST':
			form = reconciliationsform(request.POST)

			product=request.POST['myproducts']

			if form.is_valid():
				mydate=form.cleaned_data['date']


				dday,mday,yday=mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)


				transdate=date(yday,mday,dday)
				dow = calendar.month_name[mday]
				dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]

				bb = tblproductsname.objects.get(branch=mybranch,your_product_name=product)




				if bb.product.product == 'Esusu':

					remit2 = tblIafieldagent.objects.filter(branch=mybranch,
						recdate = transdate,
						is_declined=0,
						wallet_type='Main')#,
						# status='Unapproved')

					unapproved = remit2.filter(status='Unapproved')

					if unapproved.count() == 0:
						remit = remit2.filter(status='Approved')
					else:
						remit = remit2.filter(status='Unapproved')


					sdic= {}
					kk=[]


					for j in remit:
						j = j.merchant.id  #uses ID from tblSTAFF
						s = {j:j}
						sdic.update(s)
					klist = sdic.values()
					for p in klist:
						kk.append(p)



					count=remit.count()

					if count>0:
						kpp=[]
						for k in kk:
							merchant= tblIaMERCHANT.objects.get(id=k)

							merch = remit.filter(merchant=merchant)

							m1=merch.aggregate(Sum('amount'))
							m2 = m1['amount__sum']
							add3 = int(m2)

							s={'merchant':merchant,'sales':add3,'id':k}
							kpp.append(s)


						add=remit.aggregate(Sum('amount'))
						add = add['amount__sum']
						add = int(add)


						if unapproved.count() == 0:

							return render(request,'Ia/reconciliaton_esusu_approved.html',{'company':mybranch,
								'user':varuser,
								'thriftrec':kpp,
								'product':product,
								'dow':dpp,
								'dates':transdate,
								'cdate':mydate,
								'total':add})

						else:
							return render(request,'Ia/reconciliaton_esusu.html',{'company':mybranch,
								'user':varuser,
								'thriftrec':kpp,
								'product':product,
								'dow':dpp,
								'dates':transdate,
								'cdate':mydate,
								'total':add})


					else:
						msg ="NO RECORDS FOUND"
						return render(request,'Ia/reconerror.html',{'company':mybranch,
							'user':varuser,'msg':msg})

				elif bb.product.product== 'Savings':

					remit = tblIbbfieldagent.objects.filter(branch=mybranch,
						recdate = transdate,
						is_declined=0,
						wallet_type='Main',
						status='Unapproved')


					sdic= {}
					kk=[]

					for j in remit:
						j = j.merchant.id  #uses ID from tblSTAFF
						s = {j:j}
						sdic.update(s)
					klist = sdic.values()
					for p in klist:
						kk.append(p)

					count=remit.count()

					if count>0:
						kpp=[]
						for k in kk:
							merchant= tblIaMERCHANT.objects.get(id=k)

							merch = remit.filter(merchant=merchant)

							m1=merch.aggregate(Sum('amount'))
							m2 = m1['amount__sum']
							add3 = int(m2)

							s={'merchant':merchant,'sales':add3,'id':k}
							kpp.append(s)


						add=remit.aggregate(Sum('amount'))
						add = add['amount__sum']
						add = int(add)

						return render(request,'Ia/reconciliaton_savings.html',{'company':mybranch,
							'user':varuser,
							'thriftrec':kpp,
							'product':product,
							'dow':dpp,
							'dates':transdate,
							'cdate':mydate,
							'total':add})


					else:
						msg ="NO RECORDS FOUND"
						return render(request,'Ia/selectloan.html',{'msg':msg})

				elif f==0:#esusu loan
					f=0
				elif f==9:#loans from general savings
					f=0
				elif f==7:#target savings
					f=0
				elif f==87: #fixed deposit
					f=0
			else:
				msg= 'Fill all boxes'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:


			history= checksub(mybranch,'Esusu')


			if history['status'] =='Running':


				form=reconciliationsform()
				return render(request,'Ia/reconciliaton_get.html',{'company':mybranch,'prod':myy, 'user':varuser,'form':form,'msg':msg})

			else:


				msg = 'kindly Check your Subscription Status'
				return render(request,'Ia/selectloan.html',{'msg':msg})


	else:
		return HttpResponseRedirect('/login/user/')




def homereset(request):


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

		if staff.ceo==1:
			return render(request,'Ia/reset.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')








def reset(request):

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



		branch = tblBRANCH.objects.get(id=branch)
		k=Userprofile.objects.filter(branch=branch).exclude(ceo=1).delete()

		# ps = tbldefaultpass.objects.filter(branch=branch).delete()
		# cd = tblcarding.objects.filter(branch=branch).delete()
		# lc =tblbusinesslocations.objects.filter(branch=branch).delete()
		# stf = tblSTAFF.objects.filter(branch=branch).exclude(ceo=1).delete()
		tf = tblIathrift.objects.filter(branch=branch).delete()
		sv =tblIasavings_trans.objects.filter(branch=branch).delete()
		mc = tblIamerchantBank.objects.filter(branch=branch).delete()
		# mt = tblIaMERCHANT.objects.filter(branch=branch).exclude(staff=staffdet).delete()
		# ll = tblIalocations.objects.filter(branch=branch).delete()
		fa = tblIafieldagent.objects.filter(branch=branch).delete()


		cc = tblIaCUSTOMER.objects.filter(branch=branch)
		for k in cc:
			k.esusu1a= 0
			k.esusu1aloan= 0
			k.savings1a= 0
			k. loans1acash= 0
			k.loans1aitems=0
			k.fixeddepo1a=0
			k.targetsave1a=0
			k.active_loan=0
			k.save()
		cds = tblIacards.objects.filter(branch=branch).delete()
		d = tblIbbfieldagent.objects.filter(branch=branch).delete()
		cd = tblIbbsavings_trans.objects.filter(branch=branch).delete()


		return render(request,'Ia/reset_success.html',{'company':mybranch, 'user':varuser})





### dashboard***************************

def admindash5(request):

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


		if staff.thrift_officer==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		else :
			return render(request,'Ia/dashboardIa.html',{'company':mybranch, 'user':varuser,'pincode':staff})


	else:
		return HttpResponseRedirect('/login/user/')



def thrift_packages(request):

	y = tblthriftpackages.objects.filter()

	for j in y:
		if j.appendage=='Green':
			j.customer_count=250
			j.staff_count=1
			j.cost=10458.44
			j.save()

		elif j.appendage=='Peach':
			j.customer_count=1000000
			j.staff_count=1
			j.cost=12815.58
			j.save()

		elif j.appendage=='Bronze':
			j.customer_count=500
			j.staff_count=3
			j.cost=22520.84
			j.save()

		elif j.appendage=='Silver':
			j.customer_count=1000000
			j.staff_count=3
			j.cost=25935.93
			j.save()


		elif j.package=='Jumbo':
			j.customer_count=1000000
			j.staff_count=1000000
			j.cost=33753.85
			j.appendage='Gold'
			j.save()


		elif j.package=='Onboarding':
			j.appendage='Trial'
			j.save()






def flushout(request):


	gt = [14,13,12,11,10,9,8,7,6,4,2]

	for k in gt:

		# try:
		ccc =tblCOMPANY.objects.filter(id=k)

		brr=tblBRANCH.objects.filter(company=ccc)
		appp =tblapp.objects.filter(branch=brr)
		uuusa =Userprofile.objects.filter(branch=brr)
		subb =tblsubscription.objects.filter(branch=brr)


		iam = tblIaMERCHANT.objects.filter(branch=brr)
		cuu = tblIaCUSTOMER.objects.filter(branch=brr)
		ttt = tblIathrift.objects.filter(branch=brr)
		fa = tblIafieldagent.objects.filter(branch=brr)
		cas = tblIaCashier.objects.filter(branch=brr)
		mem =tblIamerchantBank.objects.filter(branch=brr)
		sfs=tblIasavings_trans.objects.filter(branch=brr)
		sdfd= tblIapayoutrequest.objects.filter(branch=brr)
		khu = tblIapayoutrecord.objects.filter(branch=brr)
		sss = tblSTAFF.objects.filter(branch=brr)

		ccc.delete()
		brr.delete()
		appp.delete()
		uuusa.delete()
		subb.delete()

		iam.delete()
		cuu.delete()
		ttt.delete()
		fa.delete()
		cas.delete()
		mem.delete()
		sfs.delete()
		sdfd.delete()
		khu.delete()
		sss.delete()

	return render(request,'/dashboard/')






# def welcome(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']
# 		try:
# 	    staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
# except:
#     return render(request,'Ia/404.html')
# 		except:
# 			msg = ' your account is not active for this service, kindly contact your boss'

# 			return render(request,'Ia/selectloan.html',{'msg':msg})


# 		staffdet=staff.staffrec.id

# 		branch=staff.branch.id
# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id

# 		ourcompany=tblCOMPANY.objects.get(id=comp_code)

# 		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

# 		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

# 		if staff.thrift_officer==0:
# 			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

# 		return render(request,'Ia/welcome.html',{'company':mybranch, 'user':varuser})

# 	else:
# 		return HttpResponseRedirect('/login/user/')













def cusreturn(request,dl):
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

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1).count()


		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)

		t= tblbusinesslocations.objects.filter(branch=mybranch)

		if staff.ceo:
			cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch)

		else:
			cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch)
			ty= tblIalocations.objects.filter(branch=mybranch,merchant=memmerchant)



		df = t.get(code=dl).location

		if staff.ceo==1:
			return render(request,'Ia/custreturn.html',{'company':mybranch,
				'location':t,
				'dl':df,
				'user':varuser,
				'client_list':cutlist})

		else:

			return render(request,'Ia/custreturn_fo.html',{'company':mybranch,
				'location':ty,
				'dl':df,
				'user':varuser,
				'client_list':cutlist})


	else:
		return HttpResponseRedirect('/login/user/')





@csrf_exempt
def getclass(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']
				state = acccode
				kk = []
				sdic = {}

				data = subjectteacher.objects.filter(email = varuser,status = 'ACTIVE',session = state).order_by('klass')
				for j in data:
					j = j.klass
					s = {j:j}
					sdic.update(s)

				# data1= groupteacher.objects.filter(email = varuser,status = 'ACTIVE',session = state).order_by('klass')
				# for j in data1:
				#     j = j.klass
				#     s = {j:j}
				#     sdic.update(s)

				klist = sdic.values()
				for p in klist:
					kk.append(p)

				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')





@csrf_exempt
def ajaxxccount_dep(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']

			yeart=0
			acccode,wallet,month,user=acccode.split(':')

			if month== '-' :
				msg = 'Select a month'
				return render(request,'Ia/selectloan.html',{'msg':msg})


			if acccode== '-----' :
				msg = 'cycle Cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else:
				staff = Userprofile.objects.get(email=user,status=1)
				staffid = staff.staffrec.id

				branch=staff.branch.id
				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)
				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff= staffid ,status=1)


				details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

				if staff.admin == 1:
					dcty= tblIaCUSTOMER.objects.get(customer=details)
				else:
					dcty= tblIaCUSTOMER.objects.get(customer=details)

				www=int(month)



				month = calendar.month_name[www]


				thriftty=tblIathrift.objects.filter(
					account_type = acccode,
					month=month,
					cycle=cycle,
					withdraw_status=0,
					complete_status=0,
					branch=mybranch,
					customer=dcty)

				gh=[]

				if thriftty.count() > 1:
					for km in thriftty:
						gm=[gh.append(int(km.year))]

					gh.sort()
					thriftrec=thriftty.get(year=gh[-1])



				elif thriftty.count()==1:
					thriftrec= thriftty.get()

				elif thriftty.count()==0:
					msg = ' No thrift record found'
					return render(request,'Ia/selectloan.html',{'msg':msg})



				thrift = thriftrec.thrift
				year=thriftrec.year
				yeart=year
				code = thriftrec.code




				CR= tblIasavings_trans.objects.filter(
					branch=mybranch,
					customer=dcty,
					code=code,
					status='CR',
					account_type = acccode)#.exclude(status='Account Maintenance')


				DR= tblIasavings_trans.objects.filter(
					branch=mybranch,
					customer=dcty,
					code=code,
					status='DR',
					account_type = acccode)


				if CR.count() > 0 :
					ncr=CR.aggregate(Sum('number'))
					ncr = ncr['number__sum']
				else:
					ncr =0

				if DR.count() > 0 :
					ndr=DR.aggregate(Sum('number'))
					ndr = ndr['number__sum']
				else:
					ndr = 0

				add = ncr

				if ncr == 31:

					msg = 'You reached the limit for this month'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				else:

					return render(request,'Ia/popdep.html',{
							'month':month,
							'wallet':wallet,
							'thrift':thrift,
							'year':year,
							'code':code,
							'cccode':acccode,
							'user':user,
							'add':add})


		else:
			return HttpResponseRedirect('/fts/thrift/payrequest/')
	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')

@csrf_exempt
def depsource(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			acccode,wallet,code,thrift,month,account,user=acccode.split(':')

			if acccode== '-----':
				msg = 'Select funding source'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			elif acccode=='Cash':
				myform = thriftamountform()

				staff = Userprofile.objects.get(email=user,status=1)

				if staff.admin == 1:
						return render(request,'Ia/popadmin.html',{'form':myform,
						'wallet':wallet,
						'thrift':thrift,
						'code':code,
						'month':month,
						'account_type':account})
				else:
					return render(request,'Ia/popto.html',{'form':myform,
						'wallet':wallet,
						'thrift':thrift,
						'code':code,
						'month':month,
						'account_type':account})


			elif acccode=='Transfer':
				msg = 'This option is coming soon !!!'
				return render(request,'Ia/selectloan.html',{'msg':msg})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')







###SELECT PRODUCTS###******************
@csrf_exempt
def products(request):
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


			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


			g = tblapp.objects.get(branch=mybranch)


			apps = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)

			gv = tblproductsname.objects.filter(branch=mybranch)
			ff = tblmyproducts.objects.filter()
			if gv.count() ==0:
				msg = 'You havent set names for your products'
				return render(request,'Ia/selectloan.html',{'msg':msg})
			else:

				return render(request,'Ia/myprod.html',
					{
					'merchant':memmerchant,
					'client':apps,
					'user':varuser,
					'customer':details,
					'wallet':wallet,
					'naam':gv,
					'year':yy,
					'sub':g,
					'sta':ff,
					'prod':gv,
					'company':mybranch,
					'id':mybranch.id,
					'user':staff})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')





def save_client_products(request):

	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)


		if request.method=='POST' :

			branch= request.POST['branch']
			wallet= request.POST['wallet']

			mybranch = tblBRANCH.objects.get(id=branch)

			oldd = tblapp.objects.get(branch=mybranch)

			ceo=tblSTAFF.objects.get(branch=mybranch,ceo=1)


			######*****************#daily contribution*****************8
			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,status=1)

			nb = tblIaCUSTOMER.objects.get(customer = details)



			sub = []
			ff=0


			if nb.esusu1a== 0:
				if 'esu' in request.POST:
					esu= 1
					sub.append('Esusu')
				else:
					esu =0
			else:
				esu =1



			if nb.esusu1aloan== 0:
				if 'esuloan' in request.POST:
					esuloan= 1
					sub.append('Ajo Loan')
				else:
					esuloan =0
			else:
				esuloan =1




			if nb.savings1a == 0:
				if 'sav' in request.POST:
					sav= 1
					sub.append('Savings')
				else:
					sav =0
			else:
				sav = 1


			if nb.loans1acash == 0:
				if 'loc' in request.POST:
					loc= 1
					sub.append('Cash Loans')
				else:
					loc =0
			else:
				loc = 1


			if nb.loans1aitems == 0:
				if 'li' in request.POST:
					li= 1
					sub.append('Asset Loan')
				else:
					li =0
			else:
				li = 1


			if nb.targetsave1a == 0:
				if 'tgg' in request.POST:
					tgg= 1
					sub.append('Target Savings')
				else:
					tgg =0
			else:
				tgg = 1


			if nb.fixeddepo1a == 0:
				if 'fxd' in request.POST:
					fxd= 1
					sub.append('Fixed Deposit')
				else:
					fxd =0
			else:
				fxd = 1


			nb.esusu1a=esu
			nb.esusu1aloan=esuloan

			nb.savings1a=sav
			nb.loans1acash=loc
			nb.loans1aitems=li

			nb.fixeddepo1a=fxd
			nb.targetsave1a=tgg
			nb.save()


			msg= 'Products activated successfully'

			return render(request,'Ia/prodsucc.html',{'company':mybranch,'customer':nb,'msg':msg,'wallet':wallet,'user':varuser})




		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')






@csrf_exempt
def safecard(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			wallet=acccode

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)

			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]




			return render(request,'Ia/cards.html',{'user':varuser,
				'customer':details,
				'wallet':wallet,
				'year':yy})




		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def safecardajax(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			if request.method == 'POST':
			    varuser = request.session['userid']
			    varerr =""
			    post = request.POST.copy()
			    acccode = post['userid']

			    business_year,wallet=acccode.split(':')

			    staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			    mybranch=tblBRANCH.objects.get(code=staff.branch.code)

			    customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
			    customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)

			    card = tblIacards.objects.filter(branch=mybranch,customer=customer,year= business_year)

			    if card.count() == 0:
			        return render(request,'Ia/cards2.html')
			    else:

			        return render(request,'Ia/cards1.html',{'card':card,'wallet':wallet})

	else:
		return HttpResponseRedirect('/login/')


def safecardsave(request):
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

			fresh=request.POST['fresh']
			year=request.POST['myyear']
			wallet=request.POST['wallet']  #returns month number as directed in form
			# number=request.POST['wallet']
			customer=tblCUSTOMER.objects.get(wallet=wallet)
			cus2=tblIaCUSTOMER.objects.get(customer=customer)


			cc = tblIacards.objects.filter(branch=mybranch,purpose=fresh,customer=cus2,card_status=1,year=year)
			if cc.count() == 0:
				tblIacards(branch=mybranch,purpose=fresh,customer=cus2,card_status=1,year=year).save()


			msg= 'Card saved successfully'

			return render(request,'Ia/cardsuc.html',{'company':mybranch,'customer':cus2,'msg':msg,'wallet':wallet,'user':varuser})


		else:
			return HttpResponseRedirect('/dashboard/')



	else:
		return HttpResponseRedirect('/login/user/')



# 	### ****************************ADD THRIFT AFFAIRS*************************


def addthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render(request,'Ia/selectloan.html',{'msg':msg})



		staffdet=staff.staffrec.id

		branch_code=staff.branch.code
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,status=1, thrift1a=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)


		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		monthname = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)


			if form.is_valid():
				mywallet=form.cleaned_data['wallet']

				try:
					details=tblCUSTOMER.objects.get(branch=mybranch,
						wallet=mywallet,
						status=1)

					if staff.admin==1: #anyone can add thrift to any client
						try:
							realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)
							myform = thriftform()
							return render(request,'Ia/myadd.html',{'company':mybranch,	'user':varuser,'form':myform,'customer':details,'wallet':mywallet})

						except:
							msg = 'This customer hasnt subscribed yet for this  service'


					elif staff.thrift_officer == 1: #anyone can add thrift to any client
						try:
							realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)
							myform = thriftform()
							return render(request,'Ia/myadd_to.html',{'company':mybranch,	'user':varuser,'form':myform,'customer':details,'wallet':mywallet})

						except:
							msg = 'This customer hasnt subscribed yet for this  service'

				except:
					msg='INVALID WALLET ADDRESS'

			else:
				msg='Enter a valid Wallet Address'


			return render(request,'Ia/selectloan.html',{'msg':msg})

		else:



			history = checksub(mybranch,'Esusu')

			# pack_customer_max = history.package.customer_count

			gh = tblIaCUSTOMER.objects.filter(branch=mybranch).count()

			ddt = date.today()

			sta= history['stop']

			if history['status'] == 'Running':
				if ddt > history['stop']:

					msg = 'you cannot proceed beyond this point, until you do something about your subscription'
					return render(request,'Ia/selectloan5.html',{'company':mybranch,'msg':msg})

				else:

					form=viewwalletform()
					msg = ''
					if staff.admin==1:
						return render(request,'Ia/addthrift.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})




					elif staff.thrift_officer==1:
						return render(request,'Ia/addthrift_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})


			else:
				msg = 'you cannot proceed beyond this point, until you do something about your subscription'
				return render(request,'Ia/selectloan5.html',{'company':mybranch,'msg':msg})



	else:
		return HttpResponseRedirect('/login/user/')

@csrf_exempt
def account_type(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			acccode,wallet,month,user=acccode.split(':')

			if month== '-' :
				msg = 'Select a month'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if acccode== '-----' :
				msg = 'cycle Cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else :

				staff = Userprofile.objects.get(email=user,status=1)
				staffid = staff.staffrec.id
				mybranch=staff.branch.id
				mybranch=tblBRANCH.objects.get(id=mybranch,status=1)

				www=int(month)

				monthname = calendar.month_name[www]

				try:
					k =appropriate_thrift(month,user,wallet,acccode)
					return render(request,'Ia/aaa.html',{'currency':mybranch.currency_code, 'month':monthname,'wallet':wallet,
							'thriftrec':k,'acccode':acccode})

				except :

					myform = thriftform()
					return render(request,'Ia/main_account.html',{'form':myform,
						'wallet':wallet,'account_type':acccode,'month':month})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




#######***THRIFTS FROM CUSTOMERS PAGE*###

@csrf_exempt
def dithrift(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			wallet = post['userid']

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code


			mybranch=tblBRANCH.objects.get(code=branch)
			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)

			# return render(request,'Ia/selectloan.html',{'msg':wallet})

			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet, status=1)


			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


			return render(request,'Ia/thrifts.html',{'customer':details,'wallet':wallet,'year':yy})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def findcardthrift(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			year,wallet=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code



			mybranch=tblBRANCH.objects.get(code=branch)

			# memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			# mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			# memmerchant=mem.count()


			# if staff.thrift_officer==0  or memmerchant<1:

			# 	return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			# else:
			# 	memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)

			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet, status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)


			month =date.today().month

			monthname = calendar.month_name[month]

			card = tblIacards.objects.filter(branch=mybranch,customer=realdet,card_status=1,year=year)

			if card.count() == 1:

				return render(request,'Ia/thrifts1.html',{'month':monthname,
					'card':card,'customer':details,'wallet':wallet,'user':varuser,
					'year':year})

			else:
				msg = 'No card found for the year  ' + year
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def findthrift(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			cycler = post['userid']
			cycle,wallet,month,user,card,year=cycler.split(':')


			if card== 'null' :
				msg = "Specify customer's Card"
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if month== '' :
				msg = 'Select a Month'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if cycle== '' :
				msg = 'Select prefered Cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else :


				staff = Userprofile.objects.get(email=user,status=1)
				branch_code=staff.branch.code
				mybranch=tblBRANCH.objects.get(code=branch_code,status=1)


				history= checksub(mybranch,'Esusu')



				if history['status'] =='Running':


					k =appropriate_thrift(mybranch,year,month,wallet,cycle,card)

					if k == 0:
						myform = thriftform()
						return render(request,'Ia/thrifts2.html',{'form':myform,'year':year,
							'wallet':wallet,'cycle':cycle,'month':month,'card':card})


					else:

						if k ==5:
							msg = f"DOUBLE THRIFTS FOUND FOR {month}  {year}"
							return render(request,'Ia/selectloan.html',{'msg':msg})

						else:

							return render(request,'Ia/thrifts3.html',{'currency':mybranch.currency_code, 'month':month,'wallet':wallet,
									'thriftrec':k,'acccode':cycle})


				else:
					msg = 'kindly Check your Subscription Status'
					return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')

def popputthrift(request):
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


		# memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		# memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,   staff=memstaff,status=1, thrift1a=1).count()

		# if staff.thrift_officer==0  or memmerchant<1:
		# 	return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		# else:
		# 	memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)


		if request.method == 'POST':
			mythrift=request.POST['thrift']
			wallet=request.POST['wallet']
			card=request.POST['card']
			cycle=request.POST['cycle']
			year=request.POST['year']
			month=request.POST['month']
			service=request.POST['service charge']

			customer=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet, status=1)

			dc_customer=tblIaCUSTOMER.objects.filter(branch=mybranch,customer=customer,
				status=1)
			dc_count= dc_customer.count()


			if dc_count== 1:
				dc_customer= dc_customer.get()

				# dc_customer tblIaCUSTOMER.objects.get(branch=mybranch,status=1,customer=customer)


			countt= tblIathrift.objects.filter(branch=mybranch,
				purpose=card,
				year = year,
				month=month,
				cycle=cycle,
				customer=dc_customer).count()

			if countt<1:
				month_index = datetime.strptime(month,"%B") #converts month_name to month_index
				tblIathrift(branch=mybranch,
					purpose=card,
					year = year,
					month=month,
					monthindex=month_index.month,
					cycle=cycle,
					interest_on_loan=0,
					service_charge = service,
					customer=dc_customer,
					thrift=mythrift,
					overdraft=0,
					actual_loan=0,
					code=generate_trans_pin()).save()


			msg= 'Thrift saved successfully'

			return render(request,'Ia/thriftsuc.html',{'customer':dc_customer,'msg':msg,'wallet':wallet,'user':varuser})


		else:
			return HttpResponseRedirect('/fts/thrift/addthrift/')

	else:
		return HttpResponseRedirect('/login/user/')

#######***END OF THRIFTS FROM CUSTOMERS PAGE*###



#******Deposit **********#############
@csrf_exempt
def didep(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			wallet = post['userid']

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)
			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			# return render(request,'Ia/selectloan.html',{'msg':wallet})
			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)


			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()[0:1]


			return render(request,'Ia/popdeposit.html',{'customer':details,'wallet':wallet,'year':yy})


		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def findcarddeposit(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			year,wallet=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)


			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet, status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)



			card = tblIacards.objects.filter(branch=mybranch,customer=realdet,card_status=1,year=year)

			if card.count() == 1:


				myy = []
				gb = tblproductsname.objects.filter(branch=mybranch)


				if staff.esusu1a is True:
					if realdet.esusu1a is True:
						hh= tblmyproducts.objects.get(product='Esusu')
						gb2=gb.get(product=hh)
						myy.append(gb2.your_product_name)

				if staff.savings1a is True:
					if realdet.savings1a is True:
						hh= tblmyproducts.objects.get(product='Savings')
						gb2=gb.get(product=hh)
						myy.append(gb2.your_product_name)

				if len(myy) ==1: #listcount
					return render(request,'Ia/popdeposit1.html',{'card':card,
						'prod':myy,
						'customer':details,
						'wallet':wallet})
				else:

					return render(request,'Ia/popdeposit6.html',{'card':card,
						'prod':myy,
						'customer':details,
						'wallet':wallet})


			else:
				msg = 'No card found for the year  ' + year
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def fillmonthdep(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,product=acccode.split(':')

				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				if card == '-----':
					msg = 'Select the appropriate card'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				if product == '-----':
					msg = 'Select the appropriate product'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				staffdet=staff.staffrec.id
				branch_code=staff.branch.code

				mybranch=tblBRANCH.objects.get(code=branch_code)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)

				bb = tblproductsname.objects.get(branch=mybranch,your_product_name=product)

				if bb.product.product == 'Esusu':
					history= checksub(mybranch,'Esusu')


					if history['status'] =='Running':

						kk=[]
						sdic={}

						data =  tblIathrift.objects.filter(branch=mybranch,
							year=business_year,
							purpose=card,
							complete_status=False,
							customer=customer).order_by('monthindex').reverse()


						if data.count() == 0:
							msg='No active THRIFT found'
							return render(request,'Ia/selectloan.html',{'msg':msg})

						for j in data:
							kk.append(j.month)


						new_list =[]

						[new_list.append(item) for item in kk if item not in new_list]  #### REMOVES REPEATITION#*****


						return render(request,'Ia/popdeposit2.html',{'data':new_list,'wallet':wallet,'user':varuser})


					else:

						msg = f"kindly Check your Subscription Status for {bb.your_product_name} product"
						return render(request,'Ia/selectloan.html',{'msg':msg})


				elif bb.product.product == 'Savings':


					history= checksub(mybranch,'General Savings')


					if history['status'] =='Running':
						fgh=[]

						tv = tblIbbfieldagent.objects.filter(branch=mybranch,
								customer=customer,
								status='Unapproved',
								wallet_type='Main',
								is_declined=0)



						if tv.count() > 0:
							for k in tv:
								pl=k.recdate
								fgh.append(pl)

							msg=list(dict.fromkeys(fgh))[0] # remove duplicates from list

						else:
							msg = date.today()


						if date.today() == msg: #if same day

							if tv.count() == 0:
								return render(request,'Ia/all.html',{'wallet':wallet})

							elif tv.count() > 0:

								all_data=[]

								unrem = tv.aggregate(Sum('amount'))
								unrem = int(unrem['amount__sum'])

								for k in tv:
									pl=k.recdate
									mm=k.merchant.id
									mm2= tblIaMERCHANT.objects.get(id=mm)
									ff= {'merchant':mm2,'recdate':pl}
									all_data.append(pl)

								ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


								y=ddd.year
								m=ddd.month
								d=ddd.day

								dow = calendar.day_name[calendar.weekday(y,m,d)]


								return render(request,'Ia/all_rem2.html',{
									'wallet':wallet,
									'currency':mybranch.currency_code,
									'year':business_year,
									'user':varuser,
									'unrem':unrem,
									'dow':dow,
									'ddt':ddd,
									'merchants':tv})

						else:
							all_data=[]

							unrem = tv.aggregate(Sum('amount'))
							unrem = int(unrem['amount__sum'])

							for k in tv:
								pl=k.recdate
								mm=k.merchant.id
								mm2= tblIaMERCHANT.objects.get(id=mm)
								ff= {'merchant':mm2,'recdate':pl}
								all_data.append(pl)

							ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


							y=ddd.year
							m=ddd.month
							d=ddd.day

							dow = calendar.day_name[calendar.weekday(y,m,d)]


							return render(request,'Ia/all_rem.html',{
								'wallet':wallet,
								'currency':mybranch.currency_code,
								'year':business_year,
								'user':user,
								'unrem':unrem,
								'dow':dow,
								'ddt':ddd,
								'merchants':tv})


					else:

						msg = f"kindly Check your Subscription Status for {bb.your_product_name} product"
						return render(request,'Ia/selectloan.html',{'msg':msg})




			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def fillcycledep(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,month=acccode.split(':')

				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.code


				mybranch=tblBRANCH.objects.get(code=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					year=business_year,
					purpose=card,
					customer=customer,
					complete_status=False,
					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def account_dep2(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			business_year, wallet, month,card,cycle=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1)

			staffid = staff.staffrec.id

			branch_code=staff.branch.code
			mybranch=tblBRANCH.objects.get(code =branch_code)

			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff= staffid ,status=1)

			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			dcty= tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)


			tt = tblIathrift.objects.filter(branch=mybranch,
				year=business_year,
				purpose=card,
				customer=dcty,
				month=month,
				cycle=cycle)


			if tt.count() == 0:
				msg = 'No Thrift Records Found'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			elif tt.count() == 1:
				thrift = tt[0]
				code = thrift.code
				status=thrift.is_closed
				service_charge=thrift.service_charge
				# month_index = list(calendar.month_name).index(month)

				if thrift.is_overdraft == False:

					sv = tblIasavings_trans.objects.filter(branch=mybranch,
						customer=dcty,
						code=code,
				# 		recdate__month=month_index,
						purpose=card,
						status='CR',
						product='Savings',
						year=business_year)


					if sv.count() == 0 :
						add = 0

					else:

						ncr = sv.aggregate(Sum('number'))
						add = int(ncr['number__sum'])



					if thrift.complete_status == False :
						if thrift.is_closed== False:

							fgh=[]

							tv = tblIafieldagent.objects.filter(branch=mybranch,
									status='Unapproved',
									wallet_type='Main',
									customer=dcty,
									code=code)

							if tv.count() > 0:
								for k in tv:
									pl=k.recdate
									fgh.append(pl)

								msg=list(dict.fromkeys(fgh))[0] # remove duplicates from list

							else:
								msg = date.today()

							if date.today() == msg:


								if tv.count() == 0:

									return render(request,'Ia/popdeposit3.html',{
										'wallet':wallet,
										'thrift':thrift,
										'service_charge':service_charge,
										'currency':mybranch.currency_code,
										'year':business_year,
										'user':varuser,
										'add':add})

								elif tv.count() > 0:

									all_data=[]

									unrem = tv.aggregate(Sum('amount'))
									unrem = int(unrem['amount__sum'])

									for k in tv:
										pl=k.recdate
										mm=k.merchant.id
										mm2= tblIaMERCHANT.objects.get(id=mm)
										ff= {'merchant':mm2,'recdate':pl}
										all_data.append(pl)

									ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


									y=ddd.year
									m=ddd.month
									d=ddd.day

									dow = calendar.day_name[calendar.weekday(y,m,d)]
									return render(request,'Ia/popdeposit4.html',{
										'wallet':wallet,
										'thrift':thrift,
										'service_charge':service_charge,
										'currency':mybranch.currency_code,
										'year':business_year,
										'user':varuser,
										'unrem':unrem,
										'dow':dow,
										'ddt':ddd,
										'add':add,
										'merchants':tv})

							else:
								all_data=[]

								unrem = tv.aggregate(Sum('amount'))
								unrem = int(unrem['amount__sum'])

								for k in tv:
									pl=k.recdate
									mm=k.merchant.id
									mm2= tblIaMERCHANT.objects.get(id=mm)
									ff= {'merchant':mm2,'recdate':pl}
									all_data.append(pl)

								ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


								y=ddd.year
								m=ddd.month
								d=ddd.day

								dow = calendar.day_name[calendar.weekday(y,m,d)]
								return render(request,'Ia/popdeposit5.html',{
									'wallet':wallet,
									'thrift':thrift,
									'service_charge':service_charge,
									'currency':mybranch.currency_code,
									'year':business_year,
									'user':varuser,
									'unrem':unrem,
									'dow':dow,
									'ddt':ddd,
									'add':add,
									'merchants':tv})

						else:
							msg= 'This cycle is closed, because you closed it'
							return render(request,'Ia/selectloan.html',{'msg':msg})


					else:
						return render(request,'Ia/depful.html',{
							'wallet':wallet,
							'thrift':thrift,
							'service_charge':service_charge,
							'currency':mybranch.currency_code,
							'year':business_year,
							'user':varuser,
							'add':add})

				else:
					if thrift.is_done == False:

						msg = 'Your loan is not fully repaid. Use the repay loan menu instead'
						return render(request,'Ia/selectloan.html',{'msg':msg})
					else:

						msg = 'Your loan of  ' + thrift.actual_loan +  '  is completely repaid'
						return render(request,'Ia/selectloan.html',{'msg':msg})

			else:# tt.count() == 0:
				msg=f"DOUBLE THRIFTS FOUND FOR {month}"
				return render(request,'Ia/selectloan.html',{'msg':msg})


		else:
			return HttpResponseRedirect('/fts/thrift/payrequest/')
	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')



@csrf_exempt
def source(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			funding,wallet,card,user,code=acccode.split(':')
			if funding== '-----':
				msg = 'How you would like to fund this transaction'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			elif funding=='Cash':
				myform = thriftamountform()

				return render(request,'Ia/admin.html',{
					'form':myform,
					'code':code,
					'wallet':wallet})


			elif funding=='Transfer':
				msg = 'This option is coming soon !!!'
				return render(request,'Ia/selectloan.html',{'msg':msg})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



def depdisplay(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')


		if request.method == 'POST':
			wallet=request.POST['wallet']
			year =request.POST['myyear']
			card =request.POST['card']
			producr =request.POST['myproducts']
			code =request.POST['code']
			amount =request.POST['amount']

			month =request.POST['month']
			cycle =request.POST['cycle']



			staffdet=staff.staffrec.id

			branch=staff.branch.code


			mybranch=tblBRANCH.objects.get(code=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)


			cus_thrift=tblIathrift.objects.get(branch=mybranch,
				customer=customer,month=month,cycle=cycle,
				code=code)

			wors = num2words(int(amount))


			return render(request,'Ia/cashindisplay.html',{'company':mybranch,
				'customer':customer,'user':varuser,'code':code,
				'thrift':cus_thrift,
				'wallet':wallet,
				'amount':amount,
				'words':wors })


def admin_cashin(request): #customer - admin transaction
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id

		ceo = staff.ceo
		branch_code=staff.branch.code

		mybranch=tblBRANCH.objects.get(code=branch_code)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if request.method == 'POST':
			wallet =request.POST['wallet']
			amount = request.POST['amount']
			thrift_code = request.POST['code']
			month = request.POST['month']
			cycle = request.POST['cycle']


			h = tblIathrift.objects.get(branch=mybranch,code=thrift_code,month=month,cycle=cycle)

			customer=tblCUSTOMER.objects.get(branch = mybranch, wallet=wallet,status=1)

			lll=tblbusinesslocations.objects.get(branch = mybranch, location=customer.location)
			location_code=lll.code

			email3=customer.email
			customer1=tblIaCUSTOMER.objects.get(customer=customer,status=1)

			thrift=int(h.thrift)
			amount=int(amount)


			service_charge= int(h.service_charge)

			card = h.purpose
			cycle=h.cycle


			hang = tblIafieldagent.objects.filter(branch=mybranch,
						status='Unapproved',
						wallet_type='Main',
						customer=customer1,
						code=thrift_code,
						is_declined=0)




			if hang.count() == 0:
				hang = 0

			else:
				hang_count = hang.aggregate(Sum('number'))
				hang = int(hang_count['number__sum'])






			mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,
				customer=customer1,
				code = thrift_code,
				status='CR',
				purpose = card,
				product='Savings',
				wallet_type='Main')

			mont_contribution_count= mont_contribution.count()


			if mont_contribution_count == 0:
				add_count = 0

			else:
				add_count = mont_contribution.aggregate(Sum('number'))
				add_count = int(add_count['number__sum'])


			if hang == 0:

				if add_count == 0:
					p="X + Nj"
					amount2 = amount - int(h.service_charge)

				else:
					p = "Nj"
					amount2=amount

			else:
				p="Nj"
				amount2=amount

			ddt=[]


			number,l=divmod(amount2,thrift)

			if p == "X + Nj":
				number+=1 #why



			if l == 0 : #if amount is divisible by thrift
				if  add_count + number + hang <= 31 :
					product='Savings'

					ty = overall_deposit(varuser,mybranch,ceo,customer1,amount,h,memstaff,add_count,number,product,p)

					try:
						Direct_creditingIa(email3,surname,thrift,amount,month)
					except:
						h=0

					if staff.ceo == 1:
						return render(request,'Ia/apsuccess.html',{
							'company':mybranch,
							'user':varuser,
							'p':p,
							'location_code':location_code,
							'customer':customer1,
							'amount':ty})

					elif staff.thrift_officer == 1:
						return render(request,'Ia/cashinthriftsuccess.html',{'account_type':account_type,
							'company':mybranch,
							'user':varuser,
							'location_code':location_code,
							'customer':customer1,
							'amount':ty})

				else:
					msg =add_count,  number,'amount not applicable'
					return render(request,'Ia/selectloan.html',{'msg':msg})


			else:
				msg = 'Adjust amount'
				return render(request,'Ia/selectloan.html',{'msg':msg})


		else:
			# return HttpResponseRedirect('/fts/mycustomers/dashboard/'+ wallet +"/")
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')


##****End of esusu deposit*******##




@csrf_exempt
def closeacc(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			wallet=acccode

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)
			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)

			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)

			card = tblIacards.objects.filter(branch=mybranch,customer=realdet)

			yy= get_business_yr(mybranch).year

			return render(request,'Ia/closeacc.html',{'company':mybranch,
				'user':varuser,
				'year':yy,
				'card':card,
				'customer':details,
				'wallet':wallet})


		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def closeaccmonth(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet=acccode.split(':')

				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.code

				mybranch=tblBRANCH.objects.get(code=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					purpose=card,
					year=business_year,
					customer=customer)

				for j in data:
					j = j.month
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def closecycle(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,month=acccode.split(':')

				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					year=business_year,
					purpose=card,
					customer=customer,
					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def delete_details(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			business_year, wallet, month, user, card,cycle=acccode.split(':')

			if card== '' :
				msg = 'Select the appropriate card'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else :

				staff = Userprofile.objects.get(email=user,status=1)

				staffid = staff.staffrec.id

				branch_code=staff.branch.code
				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)
				mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

				memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff= staffid ,status=1)

				details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

				dcty= tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)



				history= checksub(mybranch,'Esusu')


				if history['status'] =='Running':




					tt = tblIathrift.objects.filter(branch=mybranch,
						year=business_year,
						purpose=card,
						customer=dcty,
						month=month,
						cycle=cycle)


					if tt.count() == 0:
						msg = 'No Thrift RECORD Found'
						return render(request,'Ia/selectloan.html',{'msg':msg})

					elif tt.count() == 1:
						thrift = tt[0]

						if thrift.is_overdraft ==0:

							code = thrift.code
							is_closed=thrift.is_closed
							if is_closed==1:
								status='Closed'
							elif is_closed==0:
								status='Open'

							sv = tblIamerchantBank.objects.filter(branch=mybranch,
								customer=dcty,
								code=code,
								purpose=card,
								status='CR',
								year=business_year)

							if sv.count() == 0 :
								add = 0

							else:

								ncr = sv.aggregate(Sum('number'))
								add = int(ncr['number__sum'])

							if add == 31:
								return render(request,'Ia/clo2.html',{
									'wallet':wallet,
									'thrift':thrift,
									'code':code,
									'status':status,
									'currency':mybranch.currency_code,
									'year':business_year,
									'user':user,
									'add':add})


							else:

								return render(request,'Ia/clo.html',{
									'wallet':wallet,
									'thrift':thrift,
									'code':code,
									'status':status,
									'currency':mybranch.currency_code,
									'year':business_year,
									'user':user,
									'add':add})
						else:
							msg =' You cant close this cycle right now'
							return render(request,'Ia/selectloan.html',{'msg':msg})

				else:

					msg = 'kindly Check your Subscription Status'
					return render(request,'Ia/selectloan.html',{'msg':msg})



		else:
			return HttpResponseRedirect('/fts/thrift/payrequest/')
	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')



def savechange(request,code):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')
		if request.method == 'POST':

			status =request.POST['account_type']
			wallet =request.POST['wallet']


			staffid = staff.staffrec.id

			branch_code=staff.branch.code
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

			history= checksub(mybranch,'Esusu')


			if history['status'] =='Running':

				tt = tblIathrift.objects.filter(code = code)

				if status== 'Open':
					status=0
					clue='Opened'
				elif status =='Closed':
					status=1
					clue='Closed'
				tt.update(is_closed=status)
				customer=tt.get()
				cus = customer.customer.id
				cus2=tblIaCUSTOMER.objects.get(id=cus)


				msg= f' status {clue} successful'

				# return render(request,'Ia/succcc.html',{'msg':msg,'wallet':wallet,'user':varuser})
				return render(request,'Ia/succcc.html',{'msg':msg,'wallet':wallet,'user':varuser,'customer':cus2,})


			else:

				msg = 'kindly Check your Subscription Status'
				return render(request,'Ia/selectloan.html',{'msg':msg})


		else:

			msg= 'Operation successful'

			return render(request,'Ia/succcc.html',{'msg':msg,'wallet':wallet,'user':varuser})


	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')




###*************MANAGE POSTING*******#################
def viewllposts(request,vid):

	if 'userid' in request.session:
		varuser = request.session['userid']
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

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1).count()

		details = tblCUSTOMER.objects.get(wallet= vid)

		realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)

		card = tblIacards.objects.filter(branch=mybranch,customer=realdet)


		card = tblIacards.objects.filter(branch=mybranch,customer=realdet)
		yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()

		myy = []

		gb = tblproductsname.objects.filter(branch=mybranch)

		if realdet.esusu1a is True:
			hh= tblmyproducts.objects.get(product='Esusu')
			gb2=gb.get(product=hh)
			myy.append(gb2.your_product_name)


		if realdet.savings1a is True:
			hh= tblmyproducts.objects.get(product='Savings')
			gb2=gb.get(product=hh)
			myy.append(gb2.your_product_name)

		return render(request,'Ia/trandet.html',{'company':mybranch,
			'user':varuser,
			'year':yy,
			'card':card,
			'prod':myy,
			'customer':details,
			'wallet':vid})




@csrf_exempt
def manmonth(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,product=acccode.split(':')

				if card == '-----':
					msg = 'Select Card type'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				elif product == '-----':

					msg = 'Select the appropriate product'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				currency=mybranch.currency_code

				customer2=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer2)

				lll=tblbusinesslocations.objects.get(branch = mybranch, location=customer2.location)
				location_code=lll.code

				bb = tblproductsname.objects.get(branch=mybranch,your_product_name=product)

				if bb.product.product == 'Esusu':

					kk=[]
					sdic={}


					data =  tblIathrift.objects.filter(branch=mybranch,
						purpose=card,
						year=business_year,
						customer=customer)

						#### REMOVES REPEATITION#*****
					for j in data:
						j = j.month
						s = {j:j}
						sdic.update(s)


					klist = sdic.values()
					for p in klist:
						kk.append(p)
					return render(request,'Ia/manmonth.html',{'data':kk})


				elif bb.product.product == 'Savings':
					msg = tblIbbsavings_trans.objects.filter(year=business_year,customer=customer).exclude(description='Service Charge')
					return render(request,'Ia/account_balance.html',{'company': mybranch,'location_code':location_code, 'msg':msg})

			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def mancycle(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,month=acccode.split(':')

				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					year=business_year,
					purpose=card,
					customer=customer,
					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def mpost_account(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			business_year, wallet, month, user, card,cycle=acccode.split(':')


			staff = Userprofile.objects.get(email=user,status=1)

			staffid = staff.staffrec.id

			branch_code=staff.branch.code
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff= staffid ,status=1)

			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			dcty= tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)



			history= checksub(mybranch,'Esusu')


			if history['status'] =='Running':

				tt = tblIathrift.objects.filter(branch=mybranch,
					year=business_year,
					purpose=card,
					customer=dcty,
					month=month,
					cycle=cycle)


				if tt.count() == 0:
					msg = 'No Thrift RECORD Found'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				elif tt.count() == 1:
					thrift = tt[0]
					code = thrift.code

					sv = tblIamerchantBank.objects.filter(branch=mybranch,
						customer=dcty,
						code=code,
						purpose=card,
						year=business_year)#.exclude(status='DR')
					sv = sv.exclude(description='Interest on Loan')

					# sv = tblIasavings_trans.objects.filter(branch=mybranch,
					#     customer=dcty,
					#     code=code,
					#     purpose=card,
					#     year=business_year)#.exclude(status='DR')

					if sv.count() == 0 :
						add = 0

					else:

						ncr = sv.filter(status='CR').aggregate(Sum('number'))
						add = int(ncr['number__sum'])

					# if add == 0:
					# add+=1

					dice=[]
					for k in  sv:
						trans =tblIasavings_trans.objects.filter(transac_id = k.transac_id)

						if trans.count() > 0:
							dd = trans.aggregate(Sum('number'))
							dd = int(dd['number__sum'])
						else:
							dd = 0
						g=int(k.number),dd
						r={'recdate': k.transdate,'description':k.description,'amount':k.amount,
						'number':g, 'transac_id':k.transac_id}
						dice.append(r)

					return render(request,'Ia/mpost.html',{
						'wallet':wallet,
						'thrift':thrift,
						'code':code,
						'history':dice,
						'currency':mybranch.currency_code,
						'year':business_year,
						'user':user,
						'add':add})

			else:

				msg = 'kindly Check your Subscription Status'
				return render(request,'Ia/selectloan.html',{'msg':msg})



		else:
			return HttpResponseRedirect('/fts/thrift/payrequest/')
	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')


@csrf_exempt
def mpost_refresh(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			vidd = post['userid']
			vidd,staff = vidd.split(":")

			refresh(vidd,staff)

			return 'ok'


	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def mpost_view(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			vidd = post['userid']

			customer=tblIamerchantBank.objects.get(transac_id = vidd)


			return render(request,'Ia/postdet.html',{'trans_id':vidd,
				'hhh':customer})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')


####***Delete wallet*****###
@csrf_exempt
def delpodel(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')


			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)

			branch=staff.branch.id

			mybranch=tblBRANCH.objects.get(id=branch)


			c1 = tblCUSTOMER.objects.get(branch =mybranch, wallet=wallet,status=1)

			c2 = tblIaCUSTOMER.objects.get(customer=c1)

			mycom = tblIathrift.objects.filter(customer=c2)


			if mycom.count() == 0:  # no savings (trift)
				j =0

			else:
				j=1


			if mycom.count() == 0: #no savings(savings)
				j=0
			else:
				j=1


			if mycom.count() == 0: #no loans
				j=0
			else :
				j=1

			if mycom.count() == 0: #no investments
				j=0

			else:
				j=1


			name = "{} {} {}".format(c1.surname, c1.firstname, c1.othername)
			wallet=c1.wallet
			cusss= {'name':name,'wallet':wallet}

			if j == 0:
				return render(request,'Ia/delwal.html',{'msg':cusss})

			else:
				return render(request,'Ia/delwal2.html',{'msg':cusss})


		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')




def vidsts(request,vid):
	if 'userid' in request.session:
		user=request.session['userid']

		staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


		branch=staff.branch.id

		mybranch=tblBRANCH.objects.get(id=branch)

		k = tblCUSTOMER.objects.get(branch=mybranch,wallet=vid)
		# k.delete()

		return HttpResponseRedirect('/fts/mycustomers/dashboard/+ wallet /')

	else:
		return HttpResponseRedirect('/login/user/')


def delete_recycle(request,code):

	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')
		if request.method == 'POST':

			wallet =request.POST['wallet']


			staffid = staff.staffrec.id

			branch_code=staff.branch.code
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

			history= checksub(mybranch,'Esusu')


			if history['status'] =='Running':

				tt = tblIathrift.objects.filter(code = code)
				if tt.count() == 0:
					msg = 'No Thrift RECORD Found'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				elif tt.count() == 1:
					sv = tblIamerchantBank.objects.filter(code=code).delete()

					tblIasavings_trans.objects.filter(code=code).delete()
					tblIathrift.objects.filter(code=code).delete()

					msg= 'record deleted successfully'

					return render(request,'Ia/succcc.html',{'msg':msg,'wallet':wallet,'user':varuser})





			else:

				msg = 'kindly Check your Subscription Status'
				return render(request,'Ia/selectloan.html',{'msg':msg})


		else:


			msg= 'Click continue'

			return render(request,'Ia/succcc.html',{'msg':msg,'wallet':wallet,'user':varuser})


	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')



@csrf_exempt
def recycle(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)

			card = tblIacards.objects.filter(branch=mybranch,customer=realdet)

			yy= get_business_yr(mybranch).yedar

			return render(request,'Ia/poprecycle.html',{'company':mybranch,
				'user':user,
				'year':yy,
				'card':card,
				'customer':details,
				'wallet':wallet})


		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def rmonth(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user=acccode.split(':')

				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					purpose=card,
					year=business_year,
					customer=customer)

				for j in data:
					j = j.month
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def rcycle(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,month=acccode.split(':')

				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					year=business_year,
					purpose=card,
					customer=customer,
					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def recycle_account(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			business_year, wallet, month, user, card,cycle=acccode.split(':')

			if card== '' :
				msg = 'Select the appropriate card'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else :

				staff = Userprofile.objects.get(email=user,status=1)

				staffid = staff.staffrec.id

				branch_code=staff.branch.code
				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)
				mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

				memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff= staffid ,status=1)

				details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

				dcty= tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)



				history= checksub(mybranch,'Esusu')


				if history['status'] =='Running':




					tt = tblIathrift.objects.filter(branch=mybranch,
						year=business_year,
						purpose=card,
						customer=dcty,
						month=month,
						cycle=cycle)


					if tt.count() == 0:
						msg = 'No Thrift RECORD Found'
						return render(request,'Ia/selectloan.html',{'msg':msg})

					elif tt.count() == 1:
						thrift = tt[0]  # or thrift = thrift.get()
						code = thrift.code


						if thrift.is_overdraft == 0:


							sv = tblIamerchantBank.objects.filter(branch=mybranch,
								customer=dcty,
								code=code,
								purpose=card,
								status='CR',
								year=business_year)

							if sv.count() == 0 :
								add = 0

							else:

								ncr = sv.aggregate(Sum('number'))
								add = int(ncr['number__sum'])


							return render(request,'Ia/rec.html',{
								'wallet':wallet,
								'thrift':thrift,
								'code':code,
								'currency':mybranch.currency_code,
								'year':business_year,
								'user':user,
								'add':add})
						else:
							msg = 'You cant recycle right now'
							return render(request,'Ia/selectloan.html',{'msg':msg})

				else:

					msg = 'kindly Check your Subscription Status'
					return render(request,'Ia/selectloan.html',{'msg':msg})



		else:
			return HttpResponseRedirect('/fts/thrift/payrequest/')
	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')


def paygensave(request):
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


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			amount=request.POST['amount']
			fig = num2words(int(amount))


			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,status=1)
			detailIb=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details)
			fig = num2words(int(amount))

			# fig = num2words(int(amount), lang='eng', to='currency', separator=' and', cents=False, currency='USD')

			# fig = num2words(int(amount), lang='eng', to='currency') #--to [cardinal|ordinal|ordinal_num|year|ISO 4217]., lang =en,fr,fr-BE,fr-CH,uk


			bal = int(account_balance_gen_saving(detailIb.id))


			return render(request,'Ia/deposit.html',{'company':mybranch,'user':varuser,
					'customer':detailIb,'branch':branch,'bal':bal, 'wallet':mywallet,'wrd':fig,'amount':amount})
		else:

			return HttpResponseRedirect('/dashboard/')




	else:
		return HttpResponseRedirect('/login/user/')



def gen_savings_admin_cashin(request):
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



		if request.method == 'POST':
			wallet=request.POST['wallet']
			customer=request.POST['customer']
			branch=request.POST['branch']
			amount=request.POST['amount']



			customer=tblIaCUSTOMER.objects.get(branch=mybranch,id =customer)
			fdate= datetime.today()
			ddate = fdate.date()
			ttime= fdate.time()



			lll=tblbusinesslocations.objects.get(location=customer.customer.location)
			location_code=lll.code


			memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,thrift1a=1, status=1)

			code =generate_trans_pin()

			if staff.ceo==1 : ##instant crediting if you are the ceo
				tblIbbsavings_trans(
				branch=mybranch,
				description='Credit',
				transdate=ddate,
				status='CR',
				wallet_type='Main',
				amount=amount,
				avalability='Available',
				customer=customer,
				transac_id=code,
				recdate=ddate,
				ttime=ttime,
				year=ddate.year,
				merchant=memmerchant).save()


				try:
					direct_depositIb(customer.customer.email)
				except:
					pass


				return render(request,'Ia/cashin_success.html',{'company':mybranch,
						'user':varuser,
						'customer':customer,
						'agent':memstaff,
						'location_code':location_code,
						'ttime':ttime,
						'ddate':ddate,
						'bal':int(account_balance_gen_saving(customer.id)),
						'amount':amount})

			else:
				rd = tblIbbfieldagent(branch=mybranch,
						amount=amount,
						merchant=memmerchant,
						recdate=ddate,
						customer=customer,
						ttime=ttime,
						status='Unapproved',
						wallet_type='Main',
						transac_id=code,
						year= ddate.year,
						is_declined=0).save()

				return render(request,'Ia/addthrift_cash.html',
					{'company':mybranch,
						'user':varuser,
						'customer':customer,
						'location_code':location_code,
						'wallet':wallet,
						'amount':amount})


	else:
		return HttpResponseRedirect('/login/user/')






####### WITHDRAWAL *******#############
@csrf_exempt
def popwithdraw(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()

			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)
			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)



			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)


			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()




			if staff.ceo == 1:
				return render(request,'Ia/reqcashpop.html',{'customer':details,'wallet':wallet,'year':yy})


			else:
				msg= 'Make sure you have the priviledge to take this action'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			msg='Incorrect entry'
			return render(request,'Ia/selectloan.html',{'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def findcardwithdraw(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			year,wallet=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)


			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet, status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)



			card = tblIacards.objects.filter(branch=mybranch,customer=realdet,card_status=1,year=year)

			if card.count() == 1:


				myy = []
				gb = tblproductsname.objects.filter(branch=mybranch)


				if staff.esusu1a is True:
					if realdet.esusu1a is True:
						hh= tblmyproducts.objects.get(product='Esusu')
						gb2=gb.get(product=hh)
						myy.append(gb2.your_product_name)

				if staff.savings1a is True:
					if realdet.savings1a is True:
						hh= tblmyproducts.objects.get(product='Savings')
						gb2=gb.get(product=hh)
						myy.append(gb2.your_product_name)

				if len(myy) == 1:


					return render(request,'Ia/reqcashpop1.html',{'year':year,
						'card':card,
						'prod':myy,
						'customer':details,
						'wallet':wallet})
				else:

					return render(request,'Ia/reqcashpop7.html',{'year':year,
						'card':card,
						'prod':myy,
						'customer':details,
						'wallet':wallet})



			else:
				msg = 'No card found for the year  ' + year
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def fillmonthwithdr(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,product=acccode.split(':')

				if card == '-----':
					msg = 'Select Card type'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				elif product == '-----':

					msg = 'Select the appropriate product'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch_code=staff.branch.code

				mybranch=tblBRANCH.objects.get(code=branch_code)

				currency=mybranch.currency_code

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)

				bb = tblproductsname.objects.get(branch=mybranch,your_product_name=product)

				if bb.product.product == 'Esusu':
					history= checksub(mybranch,'Esusu')


					if history['status'] =='Running':

						kk=[]
						sdic={}


						data =  tblIathrift.objects.filter(branch=mybranch,
							purpose=card,
							year=business_year,
							is_contributed=True,
							customer=customer)

							#### REMOVES REPEATITION#*****
						for j in data:
							j = j.month
							s = {j:j}
							sdic.update(s)


						klist = sdic.values()
						for p in klist:
							kk.append(p)

						# p= len(kk)
						if len(kk) == 0 :
							msg= 'No Funds in this Account'
							return render(request,'Ia/selectloan.html',{'msg':msg})


						return render(request,'Ia/reqcashpop2.html',{'data':kk})
					else:

						msg = 'kindly Check your Subscription Status for '+ bb.your_product_name
						return render(request,'Ia/selectloan.html',{'msg':msg})

				elif bb.product.product == 'Savings':
					history= checksub(mybranch,'General Savings')


					if history['status'] =='Running':

						bal = int(account_balance_gen_saving(customer.id))
						if bal > 0:
							return render(request,'Ia/reqcashpop3.html',{'company':mybranch, 'wallet':wallet,'bal':bal})
						else:
							msg = 'Make some deposits to continue'
							return render(request,'Ia/selectloan.html',{'msg':msg})

					else:

						msg = 'kindly Check your Subscription Status for '+ bb.your_product_name
						return render(request,'Ia/selectloan.html',{'msg':msg})

				else:
					return HttpResponseRedirect('/login/')

			else:
				return HttpResponseRedirect('/login/')
		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')






@csrf_exempt
def fillcyclewit(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,month=acccode.split(':')

				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.code

				mybranch=tblBRANCH.objects.get(code=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					purpose=card,
					year=business_year,
					customer=customer,
					is_contributed=True,
					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def account_withdraw_pop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']

			businessyear, wallet,month,card,cycle=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1)
			staffdet=staff.staffrec.id
			branch_code=staff.branch.code
			mybranch=tblBRANCH.objects.get(code=branch_code)


			currency=mybranch.currency_code


			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,
				staff= staffdet ,status=1)

			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)

			cus_thrift=tblIathrift.objects.filter(branch=mybranch,
				purpose=card,
				year=businessyear,
				customer=customer,
				month=month,
				cycle=cycle)

			if cus_thrift.count() ==0:
				msg = 'No records found'
				return render(request,'Ia/selectloan.html',{'msg':msg})


			# cus_thrift=cus_thrift.get()
			cus_thrift=cus_thrift[0] #indexing

			if cus_thrift.is_overdraft == 0:
				if cus_thrift.withdraw_status== 0:

					if cus_thrift.is_contributed== 0:
						msg = 'make some deposits to continue'
						return render(request,'Ia/selectloan.html',{'msg':msg})
					else:

						mythrift=cus_thrift.thrift
						code = cus_thrift.code

						dll = []
						ALLTOT= tblIasavings_trans.objects.filter(
							branch=mybranch,
							purpose=card,
							year=businessyear,
							customer=customer,
							wallet_type='Main',
							code=code)

						CR=ALLTOT.filter(status='CR').exclude(description='Account Maintenance')

						DR=ALLTOT.filter(status='DR')

						if CR.count() > 0 :
							cr=CR.aggregate(Sum('amount'))
							cr = cr['amount__sum']

							nc=CR.aggregate(Sum('number'))
							nc = nc['number__sum']

						else:
							cr =0
							nc=0

						if DR.count() > 0 :
							dr=DR.aggregate(Sum('amount'))
							dr = dr['amount__sum']

							nd=DR.aggregate(Sum('number'))
							nd= nd['number__sum']


						else:
							dr = 0
							nd=0

						add = int(cr - dr)
						number =int(nc - nd)


						jdjd= {'amount':add,'num':number,'thrift':mythrift}

						dll.append(jdjd)


						if staff.ceo==0:
							msg = 'you are not allowed to do this'
							return render(request,'Ia/selectloan.html',{'msg':msg})
						else:
							return render(request,'Ia/reqcashpop4.html',{'thriftrec':dll,
								'wallet':wallet,
								'count':number,
								'code':code,
								'year':businessyear,
								'card':card,
								'currency':currency,
								'monthname':month,
								'cycle':cycle,
								'thrift':mythrift})


				else:
					msg ='you have withdrawn your funds for the month'
					return render(request,'Ia/selectloan.html',{'msg':msg})

			else:
				if cus_thrift.is_done == 1:
					msg = 'Your loan is completely repaid'
				else:
					msg = 'Keep repaying your Loan. Thank you'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/dalogin/')

	else:
		return HttpResponseRedirect('/dalogin/')



def displaycashout(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			year =request.POST['year'] #month_index
			card =request.POST['card'] #account_type
			withdrrr =request.POST['withdrr'] #account_type
			code =request.POST['code'] #account_type

			month =request.POST['month']
			cycle =request.POST['cycle']



			withdrrr=int(withdrrr)


			staffdet=staff.staffrec.id

			branch=staff.branch.code




			mybranch=tblBRANCH.objects.get(code=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)



			cus_thrift=tblIathrift.objects.get(branch=mybranch,
				customer=customer,month=month,cycle=cycle,
				code=code)

			cycle=cus_thrift.cycle

			bal =int(account_balance(mybranch, customer,card,year))

			withdrawable= withdrrr * int(cus_thrift.thrift)

			if withdrawable > bal:
				return render(request,'Ia/reqcashpop5.html',{'company':mybranch,
					'customer':customer,'user':varuser,'code':code,
					'thrift':cus_thrift,
					'wallet':wallet,
					'withdrr':withdrrr,
					 'withdrawable':withdrawable})
			else:
				return render(request,'Ia/reqcashpop6.html',{'company':mybranch,
					'customer':customer,'user':varuser,'code':code,
					'thrift':cus_thrift,
					'wallet':wallet,
					'withdrr':withdrrr,
					 'withdrawable':withdrawable})

		else:
			return HttpResponseRedirect('/dashboard/')

def cashoutrequest(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		staffdet=staff.staffrec.id
		branch=staff.branch.code

		mybranch=tblBRANCH.objects.get(code=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		currency=mybranch.currency_code

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			year =request.POST['year'] #month_index
			card =request.POST['card'] #account_type
			withdrrr =request.POST['withdrr'] #account_type
			code =request.POST['code'] #account_type

			month =request.POST['month']
			cycle =request.POST['cycle']



			withdrrr=int(withdrrr)

			# monthname = calendar.month_name[int(month)]
			ttf =datetime.now()
			myydate=ttf.date()
			myytime=ttf.time()


			customer=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,status=1)

			lll=tblbusinesslocations.objects.get(branch = mybranch, location=customer.location)
			location_code=lll.code

			email=customer.email
			customer=tblIaCUSTOMER.objects.get(branch=mybranch, customer=customer,status=1)
			customer_code=customer.code

			thriftt= tblIathrift.objects.get(branch=mybranch,
				purpose=card,
				year=year,
				month=month,
				cycle=cycle,
				customer=customer,
				is_contributed=1,
				is_empty=0,
				withdraw_status=0,
				is_overdraft=0,
				code=code)

# 			return render(request,'Ia/selectloan.html',{'msg':thriftt})

			thrift_code=thriftt.code
			thrift=thriftt.thrift
			cycle=thriftt.cycle
			month=thriftt.month


			TOTAL= tblIasavings_trans.objects.filter(
				branch=mybranch,
				customer=customer,
				code=thrift_code,
				purpose=card)

			CR = TOTAL.filter(status='CR').exclude(description='Account Maintenance')

			DR = TOTAL.filter(status='DR')


			if CR.count() > 0 :

				cr=CR.aggregate(Sum('number'))
				cr = cr['number__sum']

			else:
				cr =0

			if DR.count() > 0 :
				dr=DR.aggregate(Sum('number'))
				dr = dr['number__sum']

			else:
				dr = 0

			number = cr - dr


			if number - withdrrr >= 0:
				ggg = int(thrift) * withdrrr
				trans_id =generate_trans_pin()
				tblIamerchantBank(branch=mybranch,
					merchant=memmerchant,
					customer=customer,
					purpose=card,
					recdate=myydate,
					transac_id=trans_id,
					status='DR',
					description='Debit',
					amount=ggg,
					year=year,
					cycle=cycle,
					ttime=myytime,
					code=thrift_code,
					number=withdrrr,
					approved_by=varuser,
					transdate=myydate,
					wallet_type='Main').save()

				tblIasavings_trans(branch=mybranch,
					description='Debit',
					transdate=myydate,
					purpose=card,
					status='DR',
					customer=customer,
					number=withdrrr,
					wallet_type = 'Main',
					ttime=myytime,
					amount=ggg,
					year=year,
					cycle=cycle,
					avalability='Not Available',
					merchant=memmerchant,
					transac_id=trans_id,
					recdate=myydate,
					code =thrift_code).save()

				try:
					withdraw_email(email)
				except:
					iu=0



				total_savings= int(account_balance(mybranch, customer,card,year))

				total_withdrawn = withdrrr + dr


				hh = after_withdrawal(customer_code, thrift_code,varuser,total_withdrawn,cr,month,cycle)



				return render(request,'Ia/payoutsuccess.html',{
					'company':mybranch,
					'customer':customer,
					'tot':ggg,
					'date':myydate,
					'user':varuser,
					'time':myytime,
					'thriftt':thriftt,
					'card_type':card,
					'location_code':location_code,
					'currency':currency,
					'total':total_savings,
					'agent':memstaff,
					'month':month,
					'year':year})

			else:
				msg = 'Number too large'
				return render(request,'Ia/selectloan.html',{'msg':msg})
		else:
			return HttpResponseRedirect('/fts/thrift/cashout/')
	else:
		return HttpResponseRedirect('/login/user/')




def cashoutdispl(request): #step 1 walk in customers
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

		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,status=1,thrift1a=1)

		if request.method == 'POST':
			mywallet=request.POST['wallet']
			withdrw=request.POST['amount']
			charge=request.POST['charge']

			details=tblCUSTOMER.objects.get(branch=mybranch,wallet=mywallet,
				status=1)
			detailIa=tblIaCUSTOMER.objects.get(customer=details)
			fig = num2words(int(withdrw))
			chg = num2words(int(charge))

			www=detailIa.id
			bal= account_balance_gen_saving(www)

			leftover = int(bal) - int(withdrw) - int(charge)



			if leftover >= 0 :

				if detailIa.active_loan == 0:

					return render(request,'Ia/reqcash.html',{'company':mybranch,
						'user':varuser,
					'customer':detailIa,
					'amount':withdrw,
					'charge':charge,
					'wrd':fig,
					'chg':chg,
					'bal':bal,
					'left':leftover,
					'wallet':mywallet})

				else:
					return render(request,'Ib/reqc_with.html',{'company':mybranch,
							'user':varuser,
						'customer':detailIa,
						'amount':withdrw,
						'charge':charge,
						'wrd':fig,
						'chg':chg,
						'bal':bal,
						'left':leftover,
						'wallet':mywallet})

			else:
				return render(request,'Ia/no_withdraw.html',{'company':mybranch,
						'user':varuser,
					'customer':detailIa,
					'amount':withdrw,
					'charge':charge,
					'wrd':fig,
					'chg':chg,
					'bal':bal,
					'left':leftover,
					'wallet':mywallet})


		else:

			msg= 'Click continue'

			return render(request,'Ia/succcc.html',{'msg':msg,'wallet':wallet,'user':varuser})






	else:
		return HttpResponseRedirect('/login/user/')





def witcashout(request):
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

		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,status=1,thrift1a=1)

		if request.method == 'POST':
			wallet=request.POST['wallet']
			amount =request.POST['amount']
			charge =request.POST['charge']


			fdate= datetime.today()
			ddate = fdate.date()
			ttime= fdate.time()

			customer=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,status=1)

			lll=tblbusinesslocations.objects.get(branch = mybranch, location=customer.location)
			location_code=lll.code



			code=generate_trans_pin()

			Ib = tblIaCUSTOMER.objects.get(customer=customer,status=1)


			if staff.ceo==1:

				savings = tblIbbsavings_trans.objects.filter(branch=mybranch,
					merchant=memmerchant,
					customer=Ib,
					recdate=ddate,
					amount=amount,
					wallet_type='Main',
					status='DR')

				if savings.count()== 0:
					tblIbbsavings_trans(branch=mybranch,
						merchant=memmerchant,
						customer=Ib,
						recdate=ddate,
						transdate=ddate,
						transac_id=code,
						amount=amount,
						wallet_type='Main',
						year=ddate.year,
						ttime=ttime,
						status='DR',
						description='Debit',
						avalability='Not Available').save()


				t3= tblIbbsavings_trans.objects.filter(branch=mybranch,
					merchant=memmerchant,
					customer=Ib,
					recdate=ddate,
					transdate=ddate,
					amount=charge,
					wallet_type='Main',
					status='DR',
					description='Service Charge',
					avalability='Not Available')

				if t3.count()==0:

					tblIbbsavings_trans(branch=mybranch,
						merchant=memmerchant,
						customer=Ib,
						recdate=ddate,
						transdate=ddate,
						amount=charge,
						transac_id=code,
						year=ddate.year,
						ttime=ttime,
						wallet_type='Main',
						status='DR',
						description='Service Charge',
						avalability='Not Available').save()

				return render(request,'Ia/payoutsuccess1.html',{'company':mybranch,
				 'user':varuser,
				 'tot':amount,
				 'location_code':location_code,
				 'customer':Ib})#'tot':total})

		return HttpResponseRedirect('/fts/mycustomers/dashboard/')
		# return HttpResponseRedirect('/fts/mycustomers/dashboard/'+ wallet +"/")


	else:
		return HttpResponseRedirect('/login/user/')



#######RECEIPTS (CUSTOMERS)********#############
def cusreceipt(request,vid):
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


		msg = 'This menu is undergoing improvement'
		return render(request,'Ia/customer_receipts.html',{'company':mybranch,
			'user':varuser,'msg':msg})
	else:
		return HttpResponseRedirect('/login/user/')






########ACCOUNT BALANCES***#########

@csrf_exempt
def historypop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,wallet=wallet,status=1)

			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()




			return render(request,'Ia/acoount_balances.html',{'user':varuser,
				'customer':details,
				'wallet':wallet,
				'year':yy})


	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def findcardbalance(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			year,wallet=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)


			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet, status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)

			card = tblIacards.objects.filter(branch=mybranch,customer=realdet,card_status=1,year=year)

			if card.count() == 1:


				myy = []
				gb = tblproductsname.objects.filter(branch=mybranch)


				if staff.esusu1a is True:
					if realdet.esusu1a is True:
						hh= tblmyproducts.objects.get(product='Esusu')
						gb2=gb.get(product=hh)
						myy.append(gb2.your_product_name)

				if staff.savings1a is True:
					if realdet.savings1a is True:
						hh= tblmyproducts.objects.get(product='Savings')
						gb2=gb.get(product=hh)
						myy.append(gb2.your_product_name)




				if len(myy) == 1:

					return render(request,'Ia/acoount_balances1.html',{'year':year,
						'card':card,
						'prod':myy,
						'customer':details,
						'wallet':wallet})

				else:

					return render(request,'Ia/acoount_balances11.html',{'year':year,
						'card':card,
						'prod':myy,
						'customer':details,
						'wallet':wallet})

			else:
				msg = 'No card found for the year  ' + year
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def fillmonthbal(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,product=acccode.split(':')

				if card == '-----':
					msg = 'Select Card type'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				elif product == '-----':

					msg = 'Select the appropriate product'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.code

				mybranch=tblBRANCH.objects.get(code=branch)

				currency=mybranch.currency_code

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				bb = tblproductsname.objects.filter(branch=mybranch,your_product_name=product)
				if bb.count() == 1:
					bb=bb.get()

					if bb.product.product == 'Esusu':
						return render(request,'Ia/acoount_balancess1.html',{'wallet':wallet})

					elif bb.product.product == 'Savings':


						msg = int(account_balance_gen_saving(customer.id))

						tv = tblIbbfieldagent.objects.filter(branch=mybranch,
								status='Unapproved',
								wallet_type='Main',
								customer=customer)

						if tv.count() == 0:

							return render(request,'Ia/account_balance_to.html',{'msg':msg,
								'company':mybranch})

						else:
							all_data=[]

							unrem = tv.aggregate(Sum('amount'))
							unrem = int(unrem['amount__sum'])

							for k in tv:
								pl=k.recdate
								all_data.append(pl)

							ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


							y=ddd.year
							m=ddd.month
							d=ddd.day


							dow = calendar.day_name[calendar.weekday(y,m,d)]

							mmm =tv[0]

							return render(request,'Ia/account_balance_to_rem.html',{
								'wallet':wallet,
								'card':card,
								'currency':currency,
								'bal':msg,
								'dow':dow,
								'unrem':unrem,
								'merchants':mmm,
								'datte':ddd})

				else:

					msg = 'You are not activated for this product'
					return render(request,'Ia/selectloan.html',{'msg':msg})




			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def fillmonthbalooooo(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,baltype,product=acccode.split(':')

				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.code

				mybranch=tblBRANCH.objects.get(code=branch)

				currency=mybranch.currency_code

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk=[]
				sdic={}

				if baltype == '-----':
					msg = 'Select balance type'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				elif baltype == 'cycleb':
					data =  tblIathrift.objects.filter(branch=mybranch,
						purpose=card,
						year=business_year,
						customer=customer)


					if data.count() == 0:
						msg='No thrift found'
						return render(request,'Ia/selectloan.html',{'msg':msg})

						#### REMOVES REPEATITION#*****
					for j in data:
						j = j.month
						s = {j:j}
						sdic.update(s)


					klist = sdic.values()
					for p in klist:
						kk.append(p)


					return render(request,'Ia/acoount_balances2.html',{'data':kk,'wallet':wallet})

				elif baltype == 'cardb':
					msg = int(account_balance(mybranch, customer,card,business_year))
					return render(request,'Ia/acoount_balances4.html',{'msg':msg,'currency':currency})

		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')

@csrf_exempt
def fillbalcycle(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,month=acccode.split(':')

				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					purpose=card,
					year=business_year,
					customer=customer,
					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def account_history_pop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']


			businessyear, wallet,month,user,card,cycle=acccode.split(':')


			staff = Userprofile.objects.get(email=varuser,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


			currency=mybranch.currency_code



			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,
				staff= staffdet ,status=1)

			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)


			cus_thrift=tblIathrift.objects.filter(branch=mybranch,
				purpose=card,
				year=businessyear,
				customer=customer,
				month=month,
				cycle=cycle)

			if cus_thrift.count() ==0:
				msg = 'No records found'
				return render(request,'Ia/selectloan.html',{'msg':msg})



			cus_thrift=cus_thrift.get()


			mythrift=cus_thrift.thrift
			code = cus_thrift.code

			dll = []
			ALLTOT= tblIasavings_trans.objects.filter(
				branch=mybranch,
				purpose=card,
				year=businessyear,
				customer=customer,
				wallet_type='Main',
				code=code).exclude(description='Account Maintenance')

			CR=ALLTOT.filter(status='CR').exclude(description='Interest on Loan')

			DR=ALLTOT.filter(status='DR')

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


			add = int(cr - dr)



			if staff.thrift_officer==0:
				msg = 'you are not allowed to do this'
				return render(request,'Ia/selectloan.html',{'msg':msg})
			else:

				tv = tblIafieldagent.objects.filter(branch=mybranch,
						status='Unapproved',
						wallet_type='Main',
						customer=customer,
						code=code)

				if tv.count() == 0:
					return render(request,'Ia/acoount_balances3.html',{'thriftrec':dll,
						'wallet':wallet,
						'code':code,
						'cycle':cycle,
						'year':businessyear,
						'card':card,
						'currency':currency,
						'monthname':month,
						'cycle':cycle,
						'bal':add})


				else:
					all_data=[]

					unrem = tv.aggregate(Sum('amount'))
					unrem = int(unrem['amount__sum'])

					for k in tv:
						pl=k.recdate
						all_data.append(pl)

					ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


					y=ddd.year
					m=ddd.month
					d=ddd.day


					dow = calendar.day_name[calendar.weekday(y,m,d)]

					mmm =tv[0]

					return render(request,'Ia/balpop_rem.html',{'thriftrec':dll,
						'wallet':wallet,
						'code':code,
						'cycle':cycle,
						'year':businessyear,
						'card':card,
						'currency':currency,
						'monthname':month,
						'cycle':cycle,
						'bal':add,
						'dow':dow,
						'unrem':unrem,
						'merchants':mmm,
						'datte':ddd})



		else:
			return HttpResponseRedirect('/dalogin/')



	else:
		return HttpResponseRedirect('/login/user/')

########END OF ACCOUNT BALANCES***#########


########STATEMENT***#########



@csrf_exempt
def ecardpop_ori(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)



			tdate= date.today()
			mday=tdate.month
			yday=tdate.year
			month = calendar.month_name[mday] #converts to name of month



			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)


			card = tblIacards.objects.filter(branch=mybranch,customer=realdet)
			yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()



			myy = []

			gb = tblproductsname.objects.filter(branch=mybranch)


			if staff.esusu1a is True:
				if realdet.esusu1a is True:
					hh= tblmyproducts.objects.get(product='Esusu')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)

			if staff.savings1a is True:
				if realdet.savings1a is True:
					hh= tblmyproducts.objects.get(product='Savings')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)



			return render(request,'Ia/ecardpop.html',{'customer':realdet,
				'card':card,
				'year':yy,
				'prod':myy,
				'wallet':wallet,'user':user})


	else:
		return HttpResponseRedirect('/login/user/')





@csrf_exempt
def ecardpop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()

			wallet = post['userid']


			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code


			mybranch=tblBRANCH.objects.get(code=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,wallet=wallet,status=1)

			yy=tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()




			return render(request,'Ia/ecardpop.html',{'user':varuser,
				'customer':details,
				'wallet':wallet,
				'year':yy})


	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def findcardstatement(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			year,wallet=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

			staffdet=staff.staffrec.id
			branch=staff.branch.code

			mybranch=tblBRANCH.objects.get(code=branch)


			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet, status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)



			card = tblIacards.objects.filter(branch=mybranch,customer=realdet,card_status=1,year=year)

			if card.count() == 1:


				myy = []
				gb = tblproductsname.objects.filter(branch=mybranch)


				if staff.esusu1a is True:
					if realdet.esusu1a is True:
						hh= tblmyproducts.objects.get(product='Esusu')
						gb2=gb.get(product=hh)
						myy.append(gb2.your_product_name)

				if staff.savings1a is True:
					if realdet.savings1a is True:
						hh= tblmyproducts.objects.get(product='Savings')
						gb2=gb.get(product=hh)
						myy.append(gb2.your_product_name)




				if len(myy) == 1:

					return render(request,'Ia/ecardpop1.html',{'year':year,
						'card':card,
						'prod':myy,
						'customer':details,
						'wallet':wallet})
				else:


					return render(request,'Ia/ecardpop11.html',{'year':year,
						'card':card,
						'prod':myy,
						'customer':details,
						'wallet':wallet})



			else:
				msg = 'No card found for the year  ' + year
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def ecardmonth(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,product=acccode.split(':')

				if card == '-----':
					msg = 'Select Card type'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				elif product == '-----':

					msg = 'Select the appropriate product'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.code


				mybranch=tblBRANCH.objects.get(code=branch)


				currency=mybranch.currency_code

				customer2=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer2)

				bb = tblproductsname.objects.get(branch=mybranch,your_product_name=product)


				lll=tblbusinesslocations.objects.get(branch = mybranch, location=customer2.location)
				location_code=lll.code

				if bb.product.product == 'Esusu':

					kk=[]
					sdic={}


					data =  tblIathrift.objects.filter(branch=mybranch,
						purpose=card,
						year=business_year,
						customer=customer)

					if data.count() == 0:

						msg='No thrift found'
						return render(request,'Ia/selectloan.html',{'msg':msg})


						#### REMOVES REPEATITION#*****
					for j in data:
						j = j.month
						s = {j:j}
						sdic.update(s)


					klist = sdic.values()
					for p in klist:
						kk.append(p)


					return render(request,'Ia/ecardpop2.html',{'data':kk,'wallet':wallet})


				elif bb.product.product == 'Savings':

					msg = tblIbbsavings_trans.objects.filter(year=business_year, customer=customer).exclude(status='Service Charge')
					bal = int(account_balance_gen_saving(customer.id))

					tv = tblIbbfieldagent.objects.filter(branch=mybranch,
							status='Unapproved',
							wallet_type='Main',
							customer=customer)

					if tv.count() == 0:

						return render(request,'Ia/account_statement.html',{'msg':msg,
							'location_code':location_code,
							'company':mybranch,'bal':bal,'customer':customer})

					else:
						all_data=[]

						unrem = tv.aggregate(Sum('amount'))
						unrem = int(unrem['amount__sum'])

						for k in tv:
							pl=k.recdate
							all_data.append(pl)

						ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


						y=ddd.year
						m=ddd.month
						d=ddd.day


						dow = calendar.day_name[calendar.weekday(y,m,d)]

						mmm =tv[0]

						return render(request,'Ia/account_statement_rem.html',{
							'wallet':wallet,
							'card':card,
							'currency':currency,
							'bal':bal,
							'msg':msg,
							'dow':dow,
							'location_code':location_code,
							'unrem':unrem,
							'merchants':mmm,
							'customer':customer,
							'datte':ddd})


			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def fillecardcycle(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,month=acccode.split(':')

				staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.code

				mybranch=tblBRANCH.objects.get(code=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					purpose=card,
					year=business_year,
					customer=customer,
					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def account_statement_history(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			businessyear, wallet,monthname,user,card,cycle=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1)
			staffdet=staff.staffrec.id

			branch=staff.branch.code
			mybranch=tblBRANCH.objects.get(code=branch)

			currency=mybranch.currency_code



			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff= staffdet ,status=1)

			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
			details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details,status=1)

			# details=tblCUSTOMER.tblIaCUSTOMER_set.all()# customer_set.all()#objects.get(branch=mybranch, wallet=wallet,status=1)



			thrift=tblIathrift.objects.filter(branch=mybranch,
				purpose=card,
				year=businessyear,
				customer=details,
				month=monthname,
				cycle=cycle)


			if thrift.count() ==0:
				msg = 'No THRIFT records found'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			thrift= thrift.get()


			code=thrift.code
			g='Account Maintenance','Interest on Loan'

			thr= tblIasavings_trans.objects.filter(
				branch=mybranch,
				customer=details,
				code=code).order_by('recdate')

			amt = 0

			dd=[]


			for k in thr:
				if k.description== 'Credit':
					amt = amt + int(k.amount)
				elif k.description == 'Debit':
					amt= amt - int(k.amount)

				else:
					amt= amt + 0

				tt = {'trans':k,'bal':amt}
				dd.append(tt)



			CR = thr.filter(description='Credit').exclude(description='Interest on Loan')

			DR = thr.filter(description ='Debit')


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
			comm =''
			uu=''

			tv = tblIafieldagent.objects.filter(branch=mybranch,
					status='Unapproved',
					wallet_type='Main',
					customer=details,
					code=code)

			if tv.count() == 0:

				return render(request,'Ia/sta.html',{
					'branch':mybranch,
					'wallet':wallet,
					'comm':comm,
					'thriftrec':dd,
					'cycle':cycle,
					'currency':currency,
					'uu':uu,
					'bal':int(add)})
			else:


				all_data=[]

				unrem = tv.aggregate(Sum('amount'))
				unrem = int(unrem['amount__sum'])


				for k in tv:
					pl=k.recdate
					all_data.append(pl)

				ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


				y=ddd.year
				m=ddd.month
				d=ddd.day

				dow = calendar.day_name[calendar.weekday(y,m,d)]
				mmm =tv[0]

				return render(request,'Ia/sta_rem.html',{
					'branch':mybranch,
					'wallet':wallet,
					'comm':comm,
					'thriftrec':dd,
					'cycle':cycle,
					'currency':currency,
					'uu':uu,
					'bal':int(add),
					'dow':dow,
					'unrem':unrem,
					'merchants':mmm,
					'datte':ddd})



		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def account_statement_historyd(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			varuser = request.session['userid']
			post = request.POST.copy()
			acccode = post['userid']
			businessyear, wallet,monthname,user,card,cycle=acccode.split(':')

			staff = Userprofile.objects.get(email=varuser,status=1)
			staffdet=staff.staffrec.id

			branch=staff.branch.code
			mybranch=tblBRANCH.objects.get(code=branch)

			currency=mybranch.currency_code



			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff= staffdet ,status=1)

			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
			details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details,status=1)

			# details=tblCUSTOMER.tblIaCUSTOMER_set.all()# customer_set.all()#objects.get(branch=mybranch, wallet=wallet,status=1)



			thrift=tblIathrift.objects.filter(branch=mybranch,
				purpose=card,
				year=businessyear,
				customer=details,
				month=monthname,
				cycle=cycle)


			if thrift.count() ==0:
				msg = 'No THRIFT records found'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			thrift= thrift.get()


			code=thrift.code




			tvp = tblIafieldagent.objects.filter(branch=mybranch,
					status='Approved',
					wallet_type='Main',
					customer=details,
					code=code)




			thr= tblIasavings_trans.objects.filter(
				branch=mybranch,
				customer=details,
				code=code).order_by('recdate')

			bbb= tblIamerchantBank.objects.filter(
				branch=mybranch,
				customer=details,
				merchant=memmerchant,
				code=code).order_by('recdate')



			amt = 0

			dd=[]

			for pk in tvp:
				transac_id= pk.transac_id
				de = thr.filter(transac_id=transac_id)

				if de.count() == 0:
					status= 'Processing'
				elif de.count() ==1 :
					status='Successful'
					k=de.get()

					if k.description== 'Credit':
						amt = amt + int(k.amount)
					elif k.description == 'Debit':
						amt= amt - int(k.amount)

					else:
						amt= amt + 0

					tt = {'trans':k,'bal':amt,'status':status}
					dd.append(tt)

				else :
					status='Successful'
					for k in de:


						if k.description== 'Credit':
							amt = amt + int(k.amount)
						elif k.description == 'Debit':
							amt= amt - int(k.amount)

						else:
							amt= amt + 0

						tt = {'trans':k,'bal':amt,'status':status}
						dd.append(tt)



			CR = thr.filter(description='Credit').exclude(description='Interest on Loan')

			DR = thr.filter(description ='Debit')


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
			comm =''
			uu=''

			tv = tblIafieldagent.objects.filter(branch=mybranch,
					status='Unapproved',
					wallet_type='Main',
					customer=details,
					code=code)

			if tv.count() == 0:

				return render(request,'Ia/sta.html',{
					'branch':mybranch,
					'wallet':wallet,
					'comm':comm,
					'thriftrec':dd,
					'cycle':cycle,
					'currency':currency,
					'uu':uu,
					'bal':int(add)})
			else:


				all_data=[]

				unrem = tv.aggregate(Sum('amount'))
				unrem = int(unrem['amount__sum'])


				for k in tv:
					pl=k.recdate
					all_data.append(pl)

				ddd=list(dict.fromkeys(all_data))[0] # remove duplicates from list


				y=ddd.year
				m=ddd.month
				d=ddd.day

				dow = calendar.day_name[calendar.weekday(y,m,d)]
				mmm =tv[0]

				return render(request,'Ia/sta_rem.html',{
					'branch':mybranch,
					'wallet':wallet,
					'comm':comm,
					'thriftrec':dd,
					'cycle':cycle,
					'currency':currency,
					'uu':uu,
					'bal':int(add),
					'dow':dow,
					'unrem':unrem,
					'merchants':mmm,
					'datte':ddd})



		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



########END OF  STATEMENT***#########

@csrf_exempt
def popoverdrafts(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()

			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)

			details=tblCUSTOMER.objects.get(branch=mybranch,wallet=wallet,status=1)

			realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)
			card = tblIacards.objects.filter(branch=mybranch,customer= realdet)
			yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()

			myy = []

			loanss= []
			gb = tblproductsname.objects.filter(branch=mybranch)


			if staff.esusu1a is True:
				if realdet.esusu1a is True:
					hh= tblmyproducts.objects.get(product='Esusu')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)


			if staff.savings1a is True:
				if realdet.savings1a is True:
					hh= tblmyproducts.objects.get(product='Savings')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)


			if staff.ceo == 1:
				details=tblIaCUSTOMER.objects.get(customer=details,status=1)
				return render(request,'Ia/overdrafts.html',{'company':mybranch,
					'user':user,
					'card':card,
					'year':yy,
					'prod':myy,
					'customer':details,
					'wallet':wallet})

			else:
				msg= 'Make sure you are RESPONSIBLE for this customer'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			msg='Incorrect entry'
			return render(request,'Ia/selectloan.html',{'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def draftmonth(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,product=acccode.split(':')

				if card == '-----':
					msg = 'Select Card type'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				elif product == '-----':

					msg = 'Select the appropriate product'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)

				staffdet=staff.staffrec.id
				branch_code=staff.branch.code

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

				currency=mybranch.currency_code

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				bb = tblproductsname.objects.filter(branch=mybranch, your_product_name=product)



				history= checksub(mybranch,'Esusu')


				if history['status'] =='Running':
					if bb.count() == 1:
						bb = bb.get()

						if bb.product.product == 'Esusu':
							kk=[]
							sdic={}

							data =  tblIathrift.objects.filter(branch=mybranch,
								purpose=card,
								year=business_year,
								customer=customer)

								#### REMOVES REPEATITION#*****
							for j in data:
								j = j.month
								s = {j:j}
								sdic.update(s)


							klist = sdic.values()
							for p in klist:
								kk.append(p)
							return render(request,'Ia/overdrafts2.html',{'data':kk})


						elif bb.product.product == 'Savings':
							loanss=[]

							if staff.loans1acash is True:
								if customer.loans1acash is True:
									loanss.append('Cash Loan')

							if staff.loans1aitems is True:
								if customer.loans1aitems is True:
									loanss.append('Asset Loan')


							return render(request,'Ia/loanpro.html',{'typp':loanss,'wallet':wallet})

					else:
						msg = 'There was an error'
						return render(request,'Ia/selectloan.html',{'msg':msg})


				else:

					msg = 'kindly Check your Subscription Status'
					return render(request,'Ia/selectloan.html',{'msg':msg})


			else:
				return HttpResponseRedirect('/login/')
		else:
			return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect('/login/')




@csrf_exempt
def ploan(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				ttype,pack,user,wallet=acccode.split(':')
				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)

				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)



				if pack == '':

					msg = 'Select Cash / Asset'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				if ttype == '':

					msg = 'Select Standard / Custom'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				elif ttype == 'Standard':
					ln = tblIastandardloan.objects.filter(branch=mybranch,status=1)
					if ln.count() < 1:
						msg = 'No loan Package set up'
						return render(request,'Ia/selectloan.html',{'msg':msg})
					else:
						return render(request,'Ia/stanloan.html',{'data':ln,'wallet':wallet})

				elif ttype== 'Custom':
					msg = 'Procesing'
					return render(request,'Ia/selectloan.html',{'msg':msg})
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def loanbreak(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				pack,amount,repay,user,wallet=acccode.split(':')

				if pack == '-----':
					msg = 'Select a Package'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				elif amount == '':

					msg = 'Enter amount'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				elif repay == '':

					msg = 'Select a repayment plan'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)

				branch=staff.branch.id


				mybranch=tblBRANCH.objects.get(id=branch)

				ty = tblIastandardloan.objects.get(branch=mybranch,description=pack)
				rate = int(ty.rate)
				output = (100+rate)
				due=output  * int(amount) / 100
				duration=int(ty.duration)

				if repay == 'daily':
					loan_duration=duration * 5
				elif repay == 'weekly':
					loan_duration= duration
				elif repay == 'monthly':
					loan_duration= duration / 4


				repayment = due / loan_duration

				currency = mybranch.currency_code

				return render(request,'Ia/loans.html',{'msg':due,
					'duration':duration,'currency':currency,
					'repay':repay,'wallet':wallet,'rate':rate,
					'repayment':repayment})


		else:
			return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect('/login/')




def displaycontinuousoverdraft(request):
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

		currency=mybranch.currency_code


		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']

			card =request.POST['card']
			year =request.POST['business_year']
			package =request.POST['loanpack']
			amount =request.POST['amount']
			duration =request.POST['duration']
			repayment =request.POST['repayment']
			due=request.POST['due']
			freq=request.POST['repay']


			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)

			return render(request,'Ia/overdraftcontinuosdisplay.html',{'company':mybranch,
				'customer':customer,
				'user':varuser,
				'year':year,
				'card':card, 'package':package,
				'currency':currency,
				'duration':duration,
				'repayment':repayment,
				'wallet':wallet,
				'due':due,
				'freq':freq,
				'amount':amount

				})

		else:
			return HttpResponseRedirect('/dashboard/')



def generalsaveapproveloan(request):
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

		if request.method=='POST':
			status= "Running"
			wallet = request.POST['wallet']


			card =request.POST['card']
			year =request.POST['year']
			package =request.POST['package']
			amount =request.POST['amount']
			thrift =request.POST['repayment']
			due =request.POST['due']
			freq =request.POST['freq']

			do =tblIastandardloan.objects.filter(branch=mybranch,
					description= package,
					status=1)

			if do.count() ==1:
				do=do.get()

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				ttf =datetime.now()
				start_date=ttf.date()

				d1 = int(do.duration * 7 ) + 2

				d1 = d1 / 31

				ennd= int(start_date.month) +d1

				end_date= date(start_date.year,4,7)



				tblloandetails(branch=mybranch,
					customer=customer,
					start_date=start_date,
					end_date=end_date,
					staffrec=memstaff,
					package=do,
					card=card,
					code=generate_trans_pin(),
					status=status,
					volume=amount,
					thrift=thrift,
					frequency=freq,
					repayment=due).save()


				msg= 'Loan approved Successfully'

				return render(request,'Ia/succcc.html',{'msg':msg,'wallet':wallet,'user':varuser})


			else:

				return HttpResponseRedirect('/login/user/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def fillcycledraft(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,month=acccode.split(':')

				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					purpose=card,
					year=business_year,
					customer=customer,

					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def ovedraftbum(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']


			businessyear, wallet,month,user,card,cycle=acccode.split(':')


			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


			currency=mybranch.currency_code



			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,
				staff= staffdet ,status=1)

			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)


			cus_thrift=tblIathrift.objects.filter(branch=mybranch,
				purpose=card,
				year=businessyear,
				customer=customer,
				month=month,
				cycle=cycle)

			if cus_thrift.count() ==0:
				msg = 'No records found'
				return render(request,'Ia/selectloan.html',{'msg':msg})



			cus_thrift=cus_thrift.get()

			if cus_thrift.is_overdraft==0:
				mythrift=cus_thrift.thrift
				code = cus_thrift.code
				my_thrift = cus_thrift.thrift
				wallet= cus_thrift.customer.customer.wallet

				ty = Loan_repaid_count(wallet,staff,code)

				contribution = (ty['savings_cr'] - ty['savings_dr']) * int(mythrift)


				withdrawable = (31 - ty['savings_dr'])  * int(mythrift)


				overdraft = withdrawable  - (ty['savings_cr'] - ty['savings_dr'] ) * int(mythrift)


				if staff.ceo==0:
					msg = 'you are not allowed to do this'
					return render(request,'Ia/selectloan.html',{'msg':msg})
				else:
					return render(request,'Ia/overdraftsbum.html',{
						'wallet':wallet,
						'code':code,
						'year':businessyear,
						'withdrawable':withdrawable,
						'card':card,
						'thrift':mythrift,
						'overdraft':overdraft,
						'contribution':contribution,
						'currency':currency,
						'monthname':month,
						'cycle':cycle})
			else:
				msg ='Youl already got payment advance for this cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/dalogin/')

	else:
		return HttpResponseRedirect('/dalogin/')

def displayoverdraft(request):
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

		currency=mybranch.currency_code


		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']

			credit =request.POST['deposited']
			code =request.POST['code']
			withdrawable =request.POST['withdrawable']
			overdraft =request.POST['overdraft']
			service_charge =request.POST['servicecharge']

			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)



			cus_thrift=tblIathrift.objects.get(branch=mybranch,
				customer=customer,
				code=code)


			fff = int(withdrawable) - int(service_charge) #these two variables are unicode



			return render(request,'Ia/overdraftdisplay.html',{'company':mybranch,
				'customer':customer,'user':varuser,'code':code,
				'charge':service_charge, 'charges':credit,
				'payout':fff,'thrift':cus_thrift,'overdraft':overdraft,
				'wallet':wallet, 'withdrawable':withdrawable})

		else:
			return HttpResponseRedirect('/dashboard/')




def approvemyloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		currency=mybranch.currency_code

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			servicecharge =request.POST['service_charge']
			code =request.POST['code']
			overdraft =request.POST['overdraft']

			ttf =datetime.now()
			myydate=ttf.date()
			myytime=ttf.time()



			customer=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,status=1)

			lll=tblbusinesslocations.objects.get(branch = mybranch, location=customer.location)
			location_code=lll.code

			email=customer.email
			customer=tblIaCUSTOMER.objects.get(branch=mybranch, customer=customer,status=1)



			thrift= tblIathrift.objects.filter(branch=mybranch,code=code)


			if thrift.count() == 1:
				thriftt= thrift.get()

				thrift_code=thriftt.code
				cycle=thriftt.cycle
				month=thriftt.month


				if thriftt.is_overdraft == 0:

					ty = Loan_repaid_count(wallet,staff,code)


					withdrawable = (31 - ty['savings_dr'])  * int(thriftt.thrift)

					number  = 31 - ty['savings_dr']

					# number= int(withdrawable) / int(thriftt.thrift)

					payable = withdrawable - int(servicecharge)

					trans_id =generate_trans_pin()


					chch = tblIamerchantBank.objects.filter(branch=mybranch,
								merchant=memmerchant,
								customer=customer,
								purpose=thriftt.purpose,
								status='DR',
								description='Loan',
								product='Loan',
								amount=withdrawable,
								code=code,
								number=number,
								wallet_type='Main')


					if chch.count() == 0 :
						tblIamerchantBank(branch=mybranch,

							merchant=memmerchant,
							customer=customer,
							purpose=thriftt.purpose,
							status='DR',
							description='Loan',
							product='Loan',
							amount=withdrawable,
							code=code,
							number= number,
							wallet_type='Main',

							recdate=myydate,
							transac_id=trans_id,
							year=thriftt.year,
							cycle=thriftt.cycle,
							ttime=myytime,
							approved_by=varuser,
							transdate=myydate).save()



					chch2 = tblIamerchantBank.objects.filter(branch=mybranch,
								merchant=memmerchant,
								customer=customer,
								purpose=thriftt.purpose,
								status='CR',
								description='Interest on Loan',
								amount=servicecharge,
								product='Loan',
								code=code,
								number=0,
								wallet_type='Main')


					if chch2.count() == 0 :
						tblIamerchantBank(branch=mybranch,

							merchant=memmerchant,
							customer=customer,
							purpose=thriftt.purpose,
							status='CR',
							description='Interest on Loan',
							amount=servicecharge,
							product='Loan',
							code=code,
							number=0,
							wallet_type='Main',

							recdate=myydate,
							transac_id=trans_id,
							year=thriftt.year,
							cycle=thriftt.cycle,
							ttime=myytime,
							approved_by=varuser,
							transdate=myydate).save()

					svc = tblIasavings_trans.objects.filter(branch=mybranch,

							merchant=memmerchant,
							customer=customer,
							purpose=thriftt.purpose,
							status='DR',
							description='Loan',
							amount=withdrawable,
							code=code,
							number=number,
							wallet_type='Main',
							product='Loan')


					if svc.count() == 0:
						tblIasavings_trans(branch=mybranch,

							merchant=memmerchant,
							customer=customer,
							purpose=thriftt.purpose,
							status='DR',
							description='Loan',
							amount=withdrawable,
							code=code,
							number=number,
							wallet_type='Main',
							product='Loan',

							transdate=myydate,
							ttime=myytime,
							year=thriftt.year,
							cycle=thriftt.cycle,
							avalability='Not Available',
							transac_id=trans_id,
							recdate=myydate).save()




					svc2 = tblIasavings_trans.objects.filter(branch=mybranch,

							merchant=memmerchant,
							customer=customer,
							purpose=thriftt.purpose,
							status='CR',
							description='Interest on Loan',
							amount=servicecharge,
							code=code,
							number=0,
							wallet_type='Main',
							product='Loan')


					if svc2.count() == 0:
						tblIasavings_trans(branch=mybranch,

							merchant=memmerchant,
							customer=customer,
							purpose=thriftt.purpose,
							status='CR',
							description='Interest on Loan',
							amount=servicecharge,
							code=code,
							number=0,
							wallet_type='Main',
							product='Loan',

							transdate=myydate,
							ttime=myytime,
							year=thriftt.year,
							cycle=thriftt.cycle,
							avalability='Not Available',
							transac_id=trans_id,
							recdate=myydate).save()



					try:
						withdraw_email(email)
					except:
						iu=0



					thrift.update(overdraft_date_start=myydate,
						interest_on_loan=servicecharge,
						actual_loan=withdrawable,
						overdraft=overdraft,
						is_empty=1,
						is_contributed=0,
						withdraw_status=1,
						is_overdraft=1)

					return render(request,'Ia/overdsuc.html',{
						'company':mybranch,
						'customer':customer,
						'overdraft':payable,
						'date':myydate,
						'user':varuser,
						'location_code':location_code,
						'currency':currency,
						'agent':memstaff,
						'month':month,
						'year':thriftt.year})


				else:
					return HttpResponseRedirect('/dashboard/')


			else:
				msg ='rrrrrrtu'
				return render(request,'Ia/selectloan.html',{'msg':msg})
		else:
			return HttpResponseRedirect('/fts/customeria/list/')
	else:
		return HttpResponseRedirect('/login/user/')



##########REPAY   LOAN******##########################



def reploanview(request,vid):

	if 'userid' in request.session:
		varuser = request.session['userid']
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


		mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
		memmerchant=mem.count()


		if staff.thrift_officer==0  or memmerchant<1:

			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)



		details=tblCUSTOMER.objects.get(branch=mybranch, wallet=vid,status=1)
		realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)


		card = tblIacards.objects.filter(branch=mybranch,customer=realdet)
		yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()

		myy = []
		# loanss= []

		gb = tblproductsname.objects.filter(branch=mybranch)


		if staff.esusu1a is True:
			if realdet.esusu1a is True:
				hh= tblmyproducts.objects.get(product='Esusu')
				gb2=gb.get(product=hh)
				myy.append(gb2.your_product_name)


		if staff.savings1a is True:
			if realdet.savings1a is True:
				hh= tblmyproducts.objects.get(product='Savings')
				gb2=gb.get(product=hh)
				myy.append(gb2.your_product_name)


		return render(request,'Ia/poprepay.html',{'company':mybranch,
			'user':varuser,
			'year':yy,
			'card':card,
			'prod':myy,
			'customer':details,
			'wallet':vid})



	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def fillmonthloanrep(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,product=acccode.split(':')

				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				if card == '-----':
					msg = 'Select the appropriate card'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				if product == '-----':
					msg = 'Select the appropriate product'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				staffdet=staff.staffrec.id
				branch_code=staff.branch.code

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)

				history= checksub(mybranch,'Esusu')


				if history['status'] =='Running':

					bb = tblproductsname.objects.filter(branch=mybranch, your_product_name=product)
					if bb.count() == 1:
						bb = bb.get()

					if bb.product.product == 'Esusu':

						kk=[]
						sdic={}

						data =  tblIathrift.objects.filter(branch=mybranch,
							year=business_year,
							purpose=card,
							customer=customer).order_by('monthindex').reverse()

							#### REMOVES REPEATITION#*****
						for j in data:
							j = j.month
							s = {j:j}
							sdic.update(s)


						klist = sdic.values()
						for p in klist:
							kk.append(p)


						return render(request,'Ia/mmont.html',{'data':kk})



					elif bb.product.product == 'Savings':
						loanss=[]

						if staff.loans1acash is True:
							if customer.loans1acash is True:
								loanss.append('Cash Loan')

						if staff.loans1aitems is True:
							if customer.loans1aitems is True:
								loanss.append('Asset Loan')


						return render(request,'Ia/loanrep.html',{'typp':loanss})


				else:
					msg = 'kindly Check your Subscription Status'
					return render(request,'Ia/selectloan.html',{'msg':msg})

			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



@csrf_exempt
def fillcyclerep(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,month=acccode.split(':')

				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)


				kk = []
				sdic = {}


				data =  tblIathrift.objects.filter(branch=mybranch,
					year=business_year,
					purpose=card,
					customer=customer,
					month=month)


				for j in data:
					j = j.cycle
					s = {j:j}
					sdic.update(s)


				klist = sdic.values()
				for p in klist:
					kk.append(p)
				return HttpResponse(json.dumps(kk), content_type='application/json')
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def loan_account_repay(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			business_year, wallet, month, user, card,cycle=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)

			staffid = staff.staffrec.id

			branch_code=staff.branch.code
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff= staffid ,status=1)

			details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			dcty= tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)

			wallet=details.wallet



			history= checksub(mybranch,'Esusu')


			if history['status'] =='Running':


				tt = tblIathrift.objects.filter(branch=mybranch,
					year=business_year,
					purpose=card,
					customer=dcty,
					month=month,
					cycle=cycle)


				if tt.count() == 0:
					msg = 'No Thrift Records Found'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				elif tt.count() == 1:
					thrift = tt[0]
					code = thrift.code
					status=thrift.is_closed
					mythrift = thrift.thrift

					if thrift.is_overdraft == True:
						if thrift.is_done == False:

							ty = Loan_repaid_count(wallet,staff,code)

							contributed= ty['savings_cr'] * int(mythrift)

							repaid = ty['loan_repaid'] * int(mythrift)


							bal = (ty['loan_repaid'] + ty['savings_cr'] - 31 ) * int(mythrift)


							if thrift.is_closed== False:
								if ty['savings_cr'] > 0:
									return render(request,'Ia/loansource2.html',{
											'wallet':wallet,
											'thrift':thrift,
											'currency':mybranch.currency_code,
											'year':business_year,
											'user':user,
											'paid':repaid,
											'contributed':contributed,
											'bal':bal,
											'total':thrift.actual_loan})

								else:

									return render(request,'Ia/loansource.html',{
										'wallet':wallet,
										'thrift':thrift,
										'currency':mybranch.currency_code,
										'year':business_year,
										'user':user,
										'paid':repaid,
										'bal':bal,
										'total':thrift.actual_loan})

						else:
							msg = 'Your loan is fully repaid '
							return render(request,'Ia/repall.html',{
								'wallet':wallet,
								'thrift':thrift,
								'currency':mybranch.currency_code,
								'year':business_year,
								'user':user,
								'add':thrift.actual_loan})

					else:
						msg = "You haven't applied for loan"
						return render(request,'Ia/selectloan.html',{'msg':msg})

			else:

				msg = 'kindly Check your Subscription Status'
				return render(request,'Ia/selectloan.html',{'msg':msg})



		else:
			return HttpResponseRedirect('/fts/thrift/payrequest/')
	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')



@csrf_exempt
def loansource(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			funding,wallet,card,user,code=acccode.split(':')
			if funding== '-----':
				msg = 'How you would like to fund this transaction'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			elif funding=='Cash':
				myform = thriftamountform()
				staff = Userprofile.objects.get(email=user,status=1)

				if staff.ceo==1:
					return render(request,'Ia/repay.html',{
						'form':myform,
						'code':code,
						'wallet':wallet})

				elif staff.thrift_officer==1 :
					return render(request,'Ia/repay_to.html',{
						'form':myform,
						'code':code,
						'wallet':wallet})
				else:
					return HttpResponseRedirect('/login/user/')


			elif funding=='Transfer':
				msg = 'This option is coming soon !!!'
				return render(request,'Ia/selectloan.html',{'msg':msg})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




def repayadmin(request): #customer - admin transaction
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

		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			wallet =request.POST['wallet']
			amount = request.POST['amount']
			code = request.POST['code']


			customer=tblCUSTOMER.objects.get(branch = mybranch, wallet=wallet,status=1)

			lll=tblbusinesslocations.objects.get(branch = mybranch, location=customer.location)
			location_code=lll.code

			email3=customer.email
			customer1=tblIaCUSTOMER.objects.get(customer=customer,status=1)

			customer_code=customer1.code


			h = tblIathrift.objects.get(branch=mybranch,code=code)
			thrift=int(h.thrift)
			amount=int(amount)

			card = h.purpose
			cycle=h.cycle


			mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,
				customer=customer1,
				code = code,
				status='CR',
				# description='Credit',
				purpose = card,
				product='Savings',
				wallet_type='Main')

			mont_contribution_count= mont_contribution.count()

			# return render(request,'Ia/selectloan.html',{'msg':mont_contribution_count})

			if mont_contribution_count == 0:
				add_count = 0
				m2 = 0
			else:
				add_count = mont_contribution.aggregate(Sum('number'))
				add_count = int(add_count['number__sum'])

				m2 = mont_contribution.get(description='Account Maintenance')





			if add_count == 0:
				if m2 == 0 :
					p="X + Nj"
					amount2 = amount - int(h.service_charge)

				else:

					p = "Nj"
					amount2=amount

			else:
				p = "Nj"
				amount2=amount


			# msg=amount2
			# return render(request,'Ia/selectloan.html',{'msg':msg})

			ddt=[]
			number = 0
			l=0
			lump,rem=divmod(amount2,thrift)

			if rem == 0 : #if amount is divisible by thrift
				hhp=generate_trans_pin()

				total_loan_repaid = Loan_repaid_count(wallet,staff,code)

				contributed = int(total_loan_repaid['loan_repaid']) + int(total_loan_repaid['savings_cr'])

				if  contributed + lump <= 31 :
					product='Loan'
					ty = repay_loan(branch,wallet,amount,code,varuser, contributed, lump,product )

					try:
						Direct_creditingIa(email3,surname,thrift,amount,month)
					except:
						h=0

					if ty == 1:
						msg='you cant post same amount twice same day'
						return render(request,'Ia/selectloan.html',{'msg':msg})

					else:

						return render(request,'Ia/repay_loan_success.html',{
							'company':mybranch,
							'customer':customer1,
							'user':varuser,
							'amount':ty,
							'p':p,
							'location_code':location_code
							})




				else:
					msg ='amount not applicable'
					return render(request,'Ia/selectloan.html',{'msg':msg})


			else:
				msg = 'I am not divisible'
				return render(request,'Ia/selectloan.html',{'msg':msg})
		else:
			return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login/user/')


#####*********************MY LOANS**********************************########



def myloansview(request,vid):

	if 'userid' in request.session:
		varuser = request.session['userid']
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

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1).count()

		details = tblCUSTOMER.objects.get(wallet= vid)



		details=tblCUSTOMER.objects.get(branch=mybranch, wallet=vid,status=1)
		realdet = tblIaCUSTOMER.objects.get(branch=mybranch, status=1, customer=details)


		card = tblIacards.objects.filter(branch=mybranch,customer=realdet)
		yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()

		myy = []
		# loanss= []

		gb = tblproductsname.objects.filter(branch=mybranch)


		if staff.esusu1a is True:
			if realdet.esusu1a is True:
				hh= tblmyproducts.objects.get(product='Esusu')
				gb2=gb.get(product=hh)
				myy.append(gb2.your_product_name)


		if staff.savings1a is True:
			if realdet.savings1a is True:
				hh= tblmyproducts.objects.get(product='Savings')
				gb2=gb.get(product=hh)
				myy.append(gb2.your_product_name)


		return render(request,'Ia/popmyloan.html',{'company':mybranch,
			'user':varuser,
			'year':yy,
			'card':card,
			'prod':myy,
			'customer':details,
			'wallet':vid})
	else:
		return HttpResponseRedirect('/login/user/')





@csrf_exempt
def loantype(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				business_year,card,wallet,user,product,loantype=acccode.split(':')

				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


				if card == '-----':
					msg = 'Select the appropriate card'
					return render(request,'Ia/selectloan.html',{'msg':msg})


				if product == '-----':
					msg = 'Select the appropriate product'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				if loantype == '-----':
					msg = 'Select the appropriate status'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				staffdet=staff.staffrec.id
				branch_code=staff.branch.code

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

				customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				customer=tblIaCUSTOMER.objects.get(branch=mybranch,customer=customer)

				history= checksub(mybranch,'Esusu')


				if history['status'] =='Running':

					bb = tblproductsname.objects.filter(branch=mybranch, your_product_name=product)
					if bb.count() == 1:
						bb = bb.get()

					if bb.product.product == 'Esusu':

						kk=[]
						sdic={}

						data =  tblIathrift.objects.filter(branch=mybranch,
							year=business_year,
							purpose=card,
							customer=customer).order_by('monthindex').reverse()

							#### REMOVES REPEATITION#*****
						for j in data:
							j = j.month
							s = {j:j}
							sdic.update(s)


						klist = sdic.values()
						for p in klist:
							kk.append(p)


						return render(request,'Ia/mmont.html',{'data':kk})


					elif bb.product.product == 'Savings':

						loanss=[]
						g =tblloandetails.objects.filter(customer=customer,status=loantype)

						return render(request,'Ia/popmyloanrep.html',{'branch':mybranch,'myloans':g,'status':loantype,'wallet':wallet})


				else:
					msg = 'kindly Check your Subscription Status'
					return render(request,'Ia/selectloan.html',{'msg':msg})

			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:

			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def genploan(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				card,pack,product,user,wallet=acccode.split(':')
				staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)

				staffdet=staff.staffrec.id
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)



				if pack == '':

					msg = 'Select Cash / Asset'
					return render(request,'Ia/selectloan.html',{'msg':msg})



				elif pack == 'Cash Loan':
					customer=tblCUSTOMER.objects.get(wallet=wallet)
					cus2=tblIaCUSTOMER.objects.get(customer=customer)
					status='UnPaid'

					ln = tblloandetails.objects.filter(branch=mybranch,customer=customer).exclude(status='Repaid')
					dd=[]
					for kk in ln:
						code = kk.code
						dy = whatsloanbal(code)
						dd.append(dy)



					return render(request,'Ia/repayloan.html',{'branch':mybranch,
						'myloans':dd,'status':status,'user':user,
						'wallet':wallet,'card':card,'product':product})

				elif pack== 'Asset Loan':
					msg = 'Procesing'
					return render(request,'Ia/selectloan.html',{'msg':msg})
			else:
				return HttpResponseRedirect('/login/')

		else:
			return HttpResponseRedirect('/login/')
	else:
		return HttpResponseRedirect('/login/')


@csrf_exempt
def ru(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()

			acccode = post['userid']
			loancode,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)



			ln = tblloandetails.objects.filter(branch=mybranch,code=loancode)

			if ln.count() ==1:
				ln=ln.get()
				dy=whatsloanbal(loancode)
				wallet=ln.customer.customer.wallet


				if staff.ceo == 1:
					return render(request,'Ia/repayl.html',{'branch':mybranch,
						'user':user,
						'rec':dy['details'],
						'loan':dy['loan'],
						'wallet':wallet,
						'code':loancode,
						'repaid':dy['repaid'],
						'bal':dy['bal']})

				else:
					msg= 'Make sure you are RESPONSIBLE for this customer'
					return render(request,'Ia/selectloan.html',{'msg':msg})

			else:
				msg= 'Make sure you refresh the page and try again'
				return render(request,'Ia/selectloan.html',{'msg':msg})


		else:
			msg='Incorrect entry'
			return render(request,'Ia/selectloan.html',{'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def loanepay(request): #customer - admin transaction
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

		memmerchant=tblIaMERCHANT.objects.filter(staff=memstaff,thrift1a=1, status=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,thrift1a=1, status=1)

		if request.method == 'POST':
			wallet =request.POST['wallet']
			amount = request.POST['amount']
			code = request.POST['code']

			merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)
			merchant=tblIaMERCHANT.objects.get(staff=merchant,thrift1a=1)


			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
			customer=tblIaCUSTOMER.objects.get(branch=mybranch, customer=customer)


			amount=int(amount)

			dy=whatsloanbal(code)

			if amount > 0:
				sf,rr= divmod(dy['bal'],amount)


				dddy = datetime.today()
				tdate = dddy.date()
				ttime = dddy.time()

				f= tblloanrepay.objects.filter(branch=mybranch,loan=dy['loan'],
					repaid=amount,customer=customer,
					pd_date =tdate)

				if f.count() == 0:

					transac_id=generate_trans_pin()

					if sf == 0: #this means you are overpaying
						sav = amount - dy['bal']

						fg =tblIbbsavings_trans.objects.filter(branch=mybranch,
								description='Excess from loan repay',
								transdate=tdate,
								status='CR',
								wallet_type='Main',
								amount=sav,
								avalability='Available',
								customer=customer,
								recdate=tdate,
								year=tdate.year,
								merchant=memmerchant)


						if fg.count() == 0:
							tblIbbsavings_trans(branch=mybranch,
								description='Excess from loan repay',
								transdate=tdate,
								status='CR',
								wallet_type='Main',
								amount=sav,
								avalability='Available',
								customer=customer,
								transac_id=transac_id,
								recdate=tdate,
								ttime=ttime,
								year=tdate.year,
								merchant=memmerchant).save()


						kl =tblloanrepay.objects.filter(branch=mybranch,customer=customer, loan=dy['loan'],
								repaid=dy['bal'],pd_date =tdate)
						if kl.count() == 0:
							tblloanrepay(branch=mybranch, customer=customer, transac_id = transac_id,loan=dy['loan'],
								repaid=dy['bal'],pd_date =tdate).save()

						currency=mybranch.currency_code
						currency2=mybranch.currency_code
						msg= dy['bal']
						msg3='repaid succesfully as loan'
						msg4= sav
						msg5='deposited in your savings account'
						msg2=''
						lb = whatsloanbal(code)

						if lb['bal'] == 0:
							p=lb['loan']
							p.status = 'Repaid'
							p.save()
							msg2 ='Loan fully repaid'

					else:
						df = tblloanrepay.objects.filter(branch=mybranch,
							customer=customer, loan=dy['loan'],
							repaid=amount, pd_date =tdate)

						if df.count() == 0:

							tblloanrepay(branch=mybranch,transac_id=transac_id, customer=customer, loan=dy['loan'],
								repaid=amount, pd_date =tdate).save()


						currency2=mybranch.currency_code
						msg= amount
						msg2=''
						msg3= ' repaid succesfully'
						msg4=''
						msg5=''
						currency=''

						lb = whatsloanbal(code)

						if lb['bal'] == 0:
							p=lb['loan']
							p.status = 'Repaid'
							p.save()
							msg2 ='Loan fully repaid'

				else:

					msg= 'double enryy not possble'
					currency=''
					currency2=''
					msg2=''
					msg3=''
					msg4=''
					msg5=''

				return render(request,'Ia/succcc.html',{'customer':customer,'currency':currency,
					'currency2':currency2,
					'msg':msg,'msg2':msg2,
					'msg3':msg3,'msg4':msg4,
					'msg5':msg5,'wallet':wallet,'user':varuser})


			else:
				f=0




		else:
			return HttpResponseRedirect('/dashboard/')


	else:
		return HttpResponseRedirect('/login/user/')





###########################*************#####################################################


######LOAN FOR GENERAL SAVINGS************************************##################

def loanwelcome(request):
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


		return render(request,'Ia/loan_setup_home.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/')




def loan_setup(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		loans = tblIastandardloan.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.ceo==0:
			return render(request,'404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			description=request.POST['package']
			rate= request.POST['rate']
			duration=request.POST['duration']

			pack_count=loans.count()

			if pack_count == 0 :
				tblIastandardloan(rate = 0 ,description='-----', staffrec=user,branch=mybranch,status=1,duration=0).save()
				tblIastandardloan(rate = rate ,description=description, staffrec=user,branch=mybranch,status=1,duration=duration).save()
			else:
				tblIastandardloan(rate = rate ,description=description, staffrec=user,branch=mybranch,status=1,duration=duration).save()
			msg = "package added successfully"
			return render(request,'Ia/loan_setup_packagespost.html',{'company':mybranch, 'user':varuser,'msg':msg})

		return render(request,'Ia/loan_setup_packages.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')



def setgrace(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		return render(request,'Ia/loan_setgrace.html',{'company':mybranch, 'user':varuser})
	else :
		return HttpResponseRedirect('/login/')



@csrf_exempt
def ajaxsetgrace(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				post = request.POST.copy()
				acccode = post['userid']

				email,plan = acccode.split(':')

				staff = Userprofile.objects.get(email=email,status=1)
				branch=staff.branch.id

				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompay=tblCOMPANY.objects.get(id=comp_code)

				mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


				if plan == '-----':
					msg='Select repayment plan'
					return render(request,'Ib/selectloan.html',{'msg':msg})

				# msg=plan
				# return render(request,'Ib/selectloan.html',{'msg':msg})

				if plan == 'day(s)':
					rplan = 'daily'

				elif plan == 'week(s)':
					rplan= 'weekly'


				grace = tblIagrace.objects.filter(branch=mybranch,plan = rplan)
				if grace.count() ==1:
					grace=grace.get()
					return render(request,'Ia/loan_setgrace_getgrace.html',{'msg':grace})
				elif grace.count() == 0:
					return render(request,'Ia/loan_setgrace_plan.html',{'user':email,'plan':plan})

	else:
		return HttpResponseRedirect('/login/')


def addgrace(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			plan = request.POST['plan']
			grace = request.POST['grace']


			if plan == 'day(s)':
				rplan = 'daily'

			elif plan == 'week(s)':
				rplan= 'weekly'



			gc = tblIagrace.objects.filter(branch=mybranch,plan=rplan,grace=grace)
			if gc.count() ==0:
				tblIagrace(branch=mybranch,plan=rplan,grace=grace,status=1).save()

			return render(request,'Ia/loan_setgrace_graceset_success.html',{'company':mybranch,
				'user':varuser,
				'rplan':rplan,
				'dur':grace,'plan':plan})



		return render(request,'Ia/loan_setgrace.html',{'company':mybranch, 'user':varuser})
	else :
		return HttpResponseRedirect('/login/')





def loan_packages(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)


		loans = tblIastandardloan.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		return render(request,'Ia/loan_setup_packages1.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else :
		return HttpResponseRedirect('/login/')





def repayment(request):
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


		if staff.ceo ==0:
				return render(request,'Ib/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			wallet=request.POST['wallet']
			p=[]

			try :
				memstaff = tblCUSTOMER.objects.get(branch=mybranch,wallet =wallet, status=1)
				memstaff = tblIbCUSTOMER.objects.get(branch=mybranch,customer=memstaff, status=1)

				lln=tblIbloanrequests.objects.get(customer=memstaff,branch=mybranch,
					status='Running')

				thrift=lln.thrift
				total = lln.output

				ltrans = tblIbloantransaction.objects.filter(transaction_source=lln, status='CR')

				summ = ltrans.aggregate(Sum('thrift'))
				repaid = summ['thrift__sum']

				if ltrans.count()< 1:
					balance= float(total)
					repaid=0.00
				else:
					balance= float(total) - repaid

				return render(request,'Ib/repay_hist.html',{'name':memstaff,
					'wallet':wallet,
					'company':mybranch,
					'user':varuser,
					'total':total,
					'repaid':repaid,
					'balance':balance,
					'thrift':thrift})

			except:

				msg='no records found'

				return render(request,'Ib/selectloan.html',{'msg':msg})

		else:
			msg = ''
			return render(request,'Ib/repay1.html',{'company':mybranch,'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')

####################********************************************########################
def putthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.companyu
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,	staff=memstaff,status=1, thrift1a=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff=memstaff,thrift1a=1, status=1)


		yday = date.today().year

		if request.method == 'POST':
			form = thriftform(request.POST)
			if form.is_valid():
				number=request.POST['month']  #returns month number as directed in form
				mythrift=form.cleaned_data['thrift']
				wallet=request.POST['wallet']
				account_type=request.POST['account_type']

				monthname=calendar.month_name[int(number)] #converts month index to month name

				customer=tblCUSTOMER.objects.get(branch=mybranch,
					wallet=wallet,
					status=1)


				dc_customer=tblIaCUSTOMER.objects.filter(branch=mybranch,customer=customer,
					status=1).count()

				if dc_customer== 1:
					dc_customer=tblIaCUSTOMER.objects.get(branch=mybranch,status=1,customer=customer)

				generate_trans_pin()

				countt= tblIathrift.objects.filter(purpose = card,
					month=monthname,
					branch=mybranch,
					cycle=cycle,
					is_closed=0,
					customer=dc_customer).count()

				if countt<1:
					tblIathrift(purpose = card,
						month=monthname,
						thrift=mythrift,
						branch=mybranch,
						customer=dc_customer,
						code=generate_trans_pin(),
						year=yday).save()

					if staff.admin==1:

						return render(request,'Ia/addthriftsuccess.html',{'company':mybranch,
							'user':varuser,'wallet':wallet,'account':account_type,'year':yday,
							'thrift':mythrift,'month':monthname})




					elif staff.thrift_officer==1:
						return render(request,'Ia/addthriftsuccess_to.html',{'company':mybranch,
						'user':varuser,'wallet':wallet,'account':account_type,'year':yday,
						'thrift':mythrift,'month':monthname})

				else:
					msg='ow8990343dgbf5465'
					return render(request,'Ia/selectloan.html',{'msg':msg})


			else:
				msg='kljhljhluj'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/fts/thrift/addthrift/')

	else:
		return HttpResponseRedirect('/login/user/')





# 	### ****************************VIEW THRIFT AFFAIRS*************************


def viewthrift(request):
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


		if staff.thrift_officer==0:
				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


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
					try:
						details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details)
						myform = thriftform()
						if staff.admin == 1:

							return render(request,'Ia/myview.html',{'company':mybranch,'user':varuser,'form':myform,
								'customer':details,'wallet':mywallet})
						elif staff.thrift_officer==1:
							df=8
							return render(request,'Ia/myview_to.html',{'company':mybranch,'user':varuser,'form':myform,
								'customer':details,'wallet':mywallet})

					except:
						msg= 'Not subscribed for this service'
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

			return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			form=viewwalletform()
			msg = ''

			if staff.admin==1:
				return render(request,'Ia/viewthrifthistory.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})


			elif staff.thrift_officer==1:
				return render(request,'Ia/viewthrifthistory_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def account_view(request): #anybody can view anybodys thrift
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			acccode,wallet,month,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)
			staffid = staff.staffrec.id
			mybranch=staff.branch.id
			mybranch=tblBRANCH.objects.get(id=mybranch,status=1)

			tdate= date.today()
			year=tdate.year

			if month== '-' :
				msg = 'Select a month'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if acccode== '-----' :
				msg = 'cycle Cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else :
				try :

						www=int(month)

						monthname = calendar.month_name[www]
						k= view_thrift(month,user,wallet,acccode)
						currency=mybranch.currency_code

						# return render(request,'Ia/aaa.html',{'month':monthname,'wallet':wallet,
							# 'thriftrec':k,'acccode':acccode})

						return render(request,'Ia/vvv.html',{'currency':currency, 'month':monthname,'wallet':wallet,
							'thriftrec':k,'acccode':acccode})

				except :
					msg = 'No entries found'
					myform = thriftform()
					return render(request,'Ia/selectloan.html',{'msg':msg,})


		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



# #***********************CHANGE Thrift views********************

def changethrift(request):
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


		if staff.thrift_officer==0:
				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to month_number to month_name

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet,status=1)
					try:
						details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details)
						myform = thriftform()
						if staff.admin==1:
							return render(request,'Ia/mychange.html',{'company':mybranch,'user':varuser,'form':myform,
								'customer':details,'wallet':mywallet})





						if staff.thrift_officer==1:
							return render(request,'Ia/mychange_to.html',{'company':mybranch,'user':varuser,'form':myform,
								'customer':details,'wallet':mywallet})

						return render(request,'Ia/mychange.html',{'company':mybranch,'user':varuser,'form':myform,
							'customer':details,'wallet':mywallet})
					except:
						msg= 'Not subscribed for this service'
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

			return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render(request,'Ia/changethrift.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

			elif staff.thrift_officer==1:
				return render(request,'Ia/changethrift_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def account_change(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			acccode,wallet,month,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


			tdate=date.today()
			year=tdate.year


			if month== '-' :
				msg = 'Select a month'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if acccode== '-----' :
				msg = 'cycle Cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else :

				try :
					www=int(month)

					monthname = calendar.month_name[www]

					staff = Userprofile.objects.get(email=user,status=1)

					staffid = staff.staffrec.id

					details=tblCUSTOMER.objects.get(branch=mybranch,
						wallet=wallet,
						status=1)
					details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details)

					try:

						www=int(month)

						monthname = calendar.month_name[www]
						thriftrec = appropriate_thrift(month,user,wallet,acccode)

					except:
						msg = 'No record found'
						return render(request,'Ia/selectloan.html',{'msg':msg})


					transactions=tblIasavings_trans.objects.filter(branch=mybranch,
						account_type=acccode,
						customer=details,
						transdate__month=www)

					if transactions.count() == 0 :
						transactions=0
						msg = 'Click the change link to begin'

					else:
						msg = ' you cannot change thrift value at this time'
						transactions=transactions.count()

					currency = mybranch.currency_code

					return render(request,'Ia/ccc.html',{'currency':currency, 'count':transactions,
						'month':monthname,'wallet':wallet,'user':user,'acccode':acccode,
						'msg':msg,'thriftrec':thriftrec})

				except :
					msg = 'No entries found'
					return render(request,'Ia/selectloan.html',{'msg':msg,})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def edit_thrift_popup(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,month,account_type,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
			customer=tblIaCUSTOMER.objects.get(branch=mybranch, customer=customer)


			mycom = tblIathrift.objects.get(
				customer=customer,
				month=month,
				is_closed=0,
				account_type=account_type)
			yer=mycom.year

			yer=mycom.year
			thrift=mycom.thrift
			return render(request,'Ia/thrif_edit.html',{'thrift':thrift,
				'income':mycom,'account_type':account_type,
				'month':month,
				'year':yer,
				'wallet':wallet})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




def safethriftedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.thrift_officer==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		# dattee= date.today().month


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			ttr=request.POST['thrift']
			month=request.POST['month'] #month in words
			newthrift = request.POST['new thrift']
			account_type = request.POST['account_type']
			ttr =int(ttr)

			customer=tblCUSTOMER.objects.get(wallet=mywallet,status=1)
			customer=tblIaCUSTOMER.objects.get(customer=customer)

			firstthrift = tblIathrift.objects.get(
				purpose = card,
				month=month,
				is_closed=0,
				customer=customer)
			yer = firstthrift.year

			if firstthrift.thrift==ttr:
				firstthrift.thrift=newthrift
				firstthrift.save()

				if staff.admin:
					return render(request,'Ia/savethriftsuccess.html',{'company':mybranch,
						'user':varuser,
						'month':month,'year':yer,
						'wallet':mywallet,'thrift':ttr,'newt':newthrift})

				elif staff.thrift_officer==1:

					return render(request,'Ia/savethriftsuccess_to.html',{'company':mybranch,
						'user':varuser,
						'month':month,'year':yer,
						'wallet':mywallet,'thrift':ttr,'newt':newthrift})



			else:
				msg='i no do again'
				return render(request,'Ia/selectloan.html',{'msg':msg})
		else:

				return HttpResponseRedirect('/fts/thrift/changethrift/')
	else:
		return HttpResponseRedirect('/login/user/')






# #***********************ROLLOVER Thrift********************



def rolloverthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.thrift_officer==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		mydatee=date.today().month #month in figures
		current_date =int(mydatee)
		yday = date.today().year
		ddt= calendar.month_name[int(mydatee)] #month in words

		if mydatee == 12:
			nextmonth = 1
			yday2=yday+1
		else:
			nextmonth=mydatee + 1
			yday2=yday

		nnm= calendar.month_name[int(nextmonth)]

		if request.method=='POST':
			details=tblCUSTOMER.objects.filter(branch=mybranch, status=1)

			# msg=details return render(request,'Ia/selectloan.html',{'msg':msg})

			for  k in details:
				kl = tblIaCUSTOMER.objects.filter(customer=k,status=1)
				dj = kl.count()

				if dj==1: #hes a member
					t1A = kl.get(customer=k,status=1)

					thriftrec=tblIathrift.objects.filter(branch=mybranch,
						customer= t1A,
						cycle=cycle,
						month=month,
						year = yday)

					for tt in thriftrec:
						td = tt.account_type
						thrift= t.thrift

						customer_thrift=tblIathrift.objects.filter(year=yday,
							month=nextmonth,
							customer=t1A,
							cycle=cycle,
							branch=mybranch,
							account_type=td).count()

						if customer_thrift==0:
							tblIathrift(year=yday,
								month=nextmonth,
								customer=t1A,
								thrift=thrift,
								code=generate_trans_pin(),
								branch=mybranch,
								account_type=td).save()

			if staff.admin==1:
				return render(request,'Ia/rollsuccess.html',{'company':mybranch,'user':varuser,'month':ddt,'nextmonth':nnm})
			elif staff.thrift_officer==1:
				return render(request,'Ia/rollsuccess_to.html',{'company':mybranch,'user':varuser,'month':ddt,'nextmonth':nnm})


		else:

			if staff.admin==1:

				return render(request,'Ia/rolloverthrift.html',{'company':mybranch,
					'year':yday,
					'year2':yday2,
					'user':varuser,
					'month':ddt,
					'nextmonth':nnm})
			elif staff.thrift_officer==1:

				return render(request,'Ia/rolloverthrift_to.html',{'company':mybranch,
						'year':yday,
						'year2':yday2,
						'user':varuser,
						'month':ddt,
						'nextmonth':nnm})


	else:
		return HttpResponseRedirect('/login/user/')









def addmythrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render(request,'Ia/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)

		tdate= date.today()
		mday=tdate.month
		month = calendar.month_name[mday]
		myform = kthriftform()


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			myform = kthriftform(request.POST)
			details=tblCUSTOMER.objects.get(
				# merchant=memmerchant,
				 wallet=mywallet,
				 status=1)
			return render(request,'Ia/comeadd.html',{'company':mybranch,'user':varuser,'form':myform,
			'wallet':mywallet,'month':month})
		else:
			return HttpResponseRedirect('/login/user/')


def putinthriftf(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			msg = ' your account is not active for this service, kindly contact your boss'

			return render(request,'Ia/selectloan.html',{'msg':msg})

		if staff.thrift_officer==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)

		if request.method == 'POST':
			form = kthriftform(request.POST)
			if form.is_valid():
				month=request.POST['month']  # month in words
				mythrift=form.cleaned_data['thrift']
				wallet=request.POST['wallet']

				today=date.today()
				yday=today.year

				month1 = datetime.strptime(month,"%B") #converts month_name to month_index
				month2=month1.month
				customer=tblCUSTOMER.objects.get(branch=mybranch,
					wallet=wallet,
					status=1)

				tblIathrift(account_type = 'Main account',withdraw_status=0,month=month,year=yday,thrift=mythrift,branch=mybranch,
					# merchant= memmerchant,
					customer=customer,
					code=8797,number=month2).save()

				return render(request,'Ia/addthriftsuccess.html',{'company':mybranch, 'user':varuser,'wallet':wallet,'thrift':mythrift,'month':month})
			else:
				msg = 'im me'
				return render(request,'Ia/comeadd.html',{'msg':month})

		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')











def log(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		form=logform()
		if staff.admin==1:
			return render(request,'Ia/activitlog.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		else:
			msg= 'error!!!'
		return render(request,'Ia/selectloan.html',{'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def fillmerchantb(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			status,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user)
			staffid = staff.staffrec.id
			mybranch=staff.branch.id
			mybranch=tblBRANCH.objects.get(id=mybranch,status=1)
			currency=mybranch.currency_code

			if status=='-----':
				msg= 'select status'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			mydate = date.today()

			if status == 'DR':
				transaction_source = tblIafieldagent.objects.filter(branch=mybranch,
					status='Received',wallet_type='Main',recdate=mydate)
				remm=[]
				all_data=[]

				for k in transaction_source:
					pl=k.merchant.id
					all_data.append(pl)

				msg=list(dict.fromkeys(all_data)) # remove duplicates from list

				for mm in msg:
					merchant = tblIaMERCHANT.objects.get(branch=mybranch,id=mm)
					transs = tblIafieldagent.objects.filter(branch=mybranch,
						status='Received',merchant=mm, wallet_type='Main',recdate=mydate)
					total =transs.aggregate(Sum('amount'))
					total=total['amount__sum']
					mit = {'merchant':merchant,'trans':transs,'total':total}
					remm.append(mit)

				return render(request,'Ia/activitlog_merchant.html',{'company':mybranch,
					'thriftrec':remm,'date':mydate,'currency':currency, 'status':status})

			if status == 'WR':
				msg = 'not Available'
				return render(request,'Ia/selectloan.html',{'msg':msg})


		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




def logapprove(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		form=viewtransform()
		if staff.admin==1:
			return render(request,'Ia/activitlog_approve.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		else:
			msg= 'error!!!'
		return render(request,'Ia/selectloan.html',{'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def showtrans(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			status,transdate,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)
			staffid = staff.staffrec.id
			mybranch=staff.branch.id
			mybranch=tblBRANCH.objects.get(id=mybranch,status=1)
			currency=mybranch.currency_code


			if status=='-----':
				msg= 'Select Status'
				return render(request,'Ia/selectloan.html',{'msg':msg})


			if transdate=='':
				msg= 'select date'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			dday,mday,yday = transdate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)


			mydate=date(yday,mday,dday)

			if status == 'DR':
				transaction_source = tblIafieldagent.objects.filter(branch=mybranch,
					status='Received',wallet_type='Main',recdate=mydate)
				remm=[]
				all_data=[]

			for k in transaction_source:
				pl=k.merchant.id
				all_data.append(pl)

			msg=list(dict.fromkeys(all_data)) # remove duplicates from list

			for mm in msg:
				merchant = tblIaMERCHANT.objects.get(branch=mybranch,id=mm)
				transs = tblIafieldagent.objects.filter(branch=mybranch,
					status='Received',merchant=mm, wallet_type='Main',recdate=mydate)
				total =transs.aggregate(Sum('amount'))
				total=total['amount__sum']
				mit = {'merchant':merchant,'trans':transs,'total':total}
				remm.append(mit)

			return render(request,'Ia/activitlog_merchant.html',{'company':mybranch,
				'thriftrec':remm,'date':mydate,'currency':currency, 'status':status})

			if status == 'WR':
				msg = 'not Available'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



# ###################################****************************************************
























# def thriftedit(request):
# 	if 'userid' in request.session:
# 		varuser=request.session['userid']

# 		try:
	staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)

# 		except:
# 			msg = ' your account is not active for this service, kindly contact your boss'

# 			return render(request,'Ia/selectloan.html',{'msg':msg})

# 		if staff.thrift_officer==0:
# 			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
# 		staffdet=staff.staffrec.id

# 		branch=staff.branch.id
# 		mycompany=staff.branch.company
# 		company=mycompany.name
# 		comp_code=mycompany.id

# 		ourcompany=tblCOMPANY.objects.get(id=comp_code)
# 		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

# 		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

# 		try:
# 			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
# 		except:
# 			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

# 		dattee= date.today().month


# 		if request.method == 'POST':
# 			mywallet=request.POST['wallet']
# 			ttr=request.POST['thrift']
# 			dd=request.POST['date'] #month in fnumber
# 			dd = calendar.month_name[int(dd)] #converts to month name

# 			return render(request,'Ia/prevchan.html',{'company':mybranch, 'user':varuser,'month':dd,'wallet':mywallet,'thrift':ttr})

# 	else:
# 		return HttpResponseRedirect('/login/user/')










# ####  CAsh iN prOcedures************************

def payrequests(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')
		staffdet=staff.staffrec.id
		branch_code=staff.branch.code

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
		memmerchant=mem.count()


		if staff.thrift_officer==0  or memmerchant<1:

			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']

				try:
					details=tblCUSTOMER.objects.get(branch=mybranch,
						wallet=mywallet,
						status=1)

					if staff.admin ==1 :
						dcty= tblIaCUSTOMER.objects.get(customer=details,status=1)

					else: #in the future, COs might get the right to deal any customer

						dcty= tblIaCUSTOMER.objects.get(customer=details,status=1)


					myform = thriftform()

					if staff.admin==1:
						return render(request,'Ia/deposit.html',{
							'company':mybranch,
							'user':varuser,
							'form':myform,
							'customer':details,
							'wallet23':mywallet
							})



					elif staff.thrift_officer==1:
						return render(request,'Ia/deposite_to.html',{'company':mybranch,'user':varuser,'form':myform,'customer':details,'wallet':mywallet})


				except:
					msg='EITHER YOU ARE NOT RESPONSIBLE TO THIS CUSTOMER OR THEIR WALLET ADDRESS IS INVALID'
					return render(request,'Ia/selectloan.html',{'msg':msg})
			else:
				return HttpResponseRedirect('/fts/thrift/payrequest/')


		else:

			history = checksub(mybranch,'Esusu')

			gh = tblIaCUSTOMER.objects.filter(branch=mybranch).count()

			ddt = date.today()



			if history['status'] == 'Running':
				if ddt > history['stop'] :

					msg = 'you cannot proceed beyond this point, until you do something about your subscription'
					return render(request,'Ia/selectloan6.html',{'company':mybranch,'msg':msg})

				else:

					form=viewwalletform()
					if staff.admin==1:
						return render(request,'Ia/all.html',{'company':mybranch, 'user':varuser,'form':form})



					elif staff.thrift_officer==1:
						return render(request,'Ia/all_to.html',{'company':mybranch, 'user':varuser,'form':form})



			else:
				msg = 'you cannot proceed beyond this point, until you do something about your subscription'
				return render(request,'Ia/selectloan6.html',{'company':mybranch,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')







@csrf_exempt
def account_dep(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			card,wallet,user=acccode.split(':')

			if card== '' :
				msg = 'Select the appropriate card'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else :

				yye=date.today().year



				staff = Userprofile.objects.get(email=user,status=1)

				staffid = staff.staffrec.id

				branch=staff.branch.id
				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)
				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, staff= staffid ,status=1)

				details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

				dcty= tblIaCUSTOMER.objects.get(customer=details,branch=mybranch)

				tt = tblIathrift.objects.filter(branch=mybranch,
					customer=dcty,
					year=yye,
					purpose=card,
					is_closed=0)






				if tt.count() == 0:
					msg = 'No Thrift RECORD Found'
					return render(request,'Ia/selectloan.html',{'msg':msg})

				elif tt.count() == 1:
					thrift = tt[0]
					code = thrift.code

					sv = tblIamerchantBank.objects.filter(branch=mybranch, customer=dcty,code=code,purpose=card,status='CR',year=yye)
					# sv = tblIamerchantBank.objects.filter(branch=mybranch, customer=dcty,code=code,purpose=card,status='CR',year=yye)

					if sv.count() == 0 :
						add = 0

					else:

						ncr = sv.aggregate(Sum('number'))
						add = ncr['number__sum']


					return render(request,'Ia/dep.html',{
						'wallet':wallet,
						'thrift':thrift,
						'currency':mybranch.currency_code,
						'year':yye,
						'user':user,
						'add':add})

				elif tt.count() > 1:
					thrift = tt[tt.count() - 1]
					month= thrift.month
					code = thrift.code

					t4 = tt.filter(month=month)#,branch=mybranch, customer=dcty,year=yye,purpose=card)

					# msg = t4.count() return render(request,'Ia/selectloan.html',{'msg':msg})


					if t4.count()==1:
						thrift = t4[0]
						code = thrift.code

						if thrift.is_closed==1:
							k=0
						else:

							sv = tblIamerchantBank.objects.filter(branch=mybranch, customer=dcty,code=code,purpose=card,status='CR',year=yye)

							if sv.count() == 0 :
								add = 0

							else:

								ncr = sv.aggregate(Sum('number'))
								add = ncr['number__sum']


							return render(request,'Ia/dep.html',{
								'wallet':wallet,
								'thrift':thrift,
								'currency':mybranch.currency_code,
								'year':yye,
								'user':user,
								'add':add})

					elif t4.count() > 1:

						kl=[]

						for k in t4:
							pp = k.cycle
							kl.append(pp)

						return render(request,'Ia/depco.html',{
							'thrift':thrift,
							'cycle':kl,
							'month':month,
							'year':yye,
							'currency':mybranch.currency_code,
							'year':yye,
							'user':user})





		else:
			return HttpResponseRedirect('/fts/thrift/payrequest/')
	else:
		return HttpResponseRedirect('/fts/thrift/payrequest/')











@csrf_exempt
def getcount(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			cycle,card,user,month,year=acccode.split(':')


			if cycle=="":
				msg = 'Select appropriate cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else:
				yye=date.today().year

				staff = Userprofile.objects.get(email=user,status=1)

				staffid = staff.staffrec.id

				branch=staff.branch.id
				mycompany=staff.branch.company
				company=mycompany.name
				comp_code=mycompany.id
				ourcompany=tblCOMPANY.objects.get(id=comp_code)
				mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

				tg = tblIathrift.objects.get(cycle=cycle, purpose =card, month=month,year=yye)
				code=tg.code

				sv = tblIamerchantBank.objects.filter(branch=mybranch,code=code,purpose=card,status='CR',year=yye)

				if sv.count() == 0 :
					add = 0

				else:

					ncr = sv.aggregate(Sum('number'))
					add = ncr['number__sum']

				return render(request,'Ia/dep32.html',{
					'branch':mybranch,
					'code':code,
					'thrift':tg,
					'wallet':tg.customer.customer.wallet,
					'add':add,
					'user':user})


		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')





def cashier_cashin(request):
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

		memmerchant=tblIaMERCHANT.objects.filter(staff=memstaff,thrift1a=1, status=1).count()

		if staff.thrift_officer==0  or memmerchant<1:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,thrift1a=1, status=1)


		if request.method == 'POST':
			form = thriftamountform(request.POST)
			if form.is_valid():
				amount=form.cleaned_data['amount']
				mythrift=request.POST['thrift']
				wallet=request.POST['wallet']
				account_type=request.POST['account_type']


				merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)
				merchant=tblIaMERCHANT.objects.get(staff=merchant,thrift1a=1)

				amount=int(amount)

				thrift=int(mythrift)

				fdate= date.today()
				transdate=fdate

				customer=tblCUSTOMER.objects.get(branch = mybranch, wallet=wallet)
				customer1=tblIaCUSTOMER.objects.get(customer=customer)
				monthname = calendar.month_name[fdate.month]

				th = tblIathrift.objects.get(branch=mybranch,
					account_type=account_type,
					customer=customer1,
					month=monthname,
					year =fdate.year)

				code = th.code

				ddt=[]
				lump,l=divmod(amount,thrift)

				p = (monthrange(transdate.year, transdate.month))[-1]
				number= int(amount / thrift)

				if l == 0 :	#how many have u saved so far?:

					mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,

						customer=customer1, #who owns the mo
						recdate__month=fdate.month, #tranaction date
						status='CR',
						purpose = card,
						wallet_type='Main')

					if mont_contribution.count() == 0:
						add_count = 0
					else:
						add_count = mont_contribution.aggregate(Sum('number'))
						add_count = add_count['number__sum']

					if  add_count + lump <= p :

						if tblIafieldagent.objects.filter(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=number,recdate=transdate,amount=amount,purpose = card,wallet_type='Main',status='Received').count() <1 :


							tblIafieldagent(branch=mybranch,merchant=merchant,code=code,customer=customer1,number=number,recdate=transdate,amount=amount,purpose = card,wallet_type='Main',status='Received').save()

							return render(request,'Ia/cashinthriftsuccess_cash.html',{'account_type':account_type,
								'company':mybranch,
								'user':varuser,
								'wallet':wallet,
								'thrift':mythrift,
								'amount':amount,
								'count':number})

						else:
							msg = "you cant post same money twice same day"
							return render(request,'Ia/selectloan.html',{'msg':msg})

					else:
						msg = 'amount too large'
						return render(request,'Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})

				else:
					msg = 'amount not applicable'
					return render(request,'Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})

			else:
				msg = 'Error!!!'
				return render(request,'Ia/selectloan.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')




def json_view(func):
	def wrap(req, *args, **kwargs):
		resp = func(req, *args, **kwargs)
		if isinstance(resp, HttpResponse):
			return resp
		return HttpResponse(json.dumps(resp), content_type="application/json")

	return wrap

@json_view
def autocomplete(request):
	term = request.GET.get('term')

	varuser=request.session['userid']
	try:
		staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
	except:
		return render(request,'Ia/404.html')

	suggestions = []
	qset = tblIathrift.objects.get(account_type = 'Main account',code =8797)#[:10]
	thrift  = 1000
	thrr = 2000
	suggestions.append(thrr)

	# for x in range(1,6):
	# 	thrr = x * thrift
	# 	suggestions.append({'label': '%s :%s :%s :%s ' % (x, thrr), 'number': x,'amount':thrr})
	# 	# suggestions.append({'amount':thrr})
	return suggestions

	# for i in qset:
	#     suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
	# return suggestions


def history(request):
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


		if staff.thrift_officer==0:
				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet, status=1)
					details= tblIaCUSTOMER.objects.get(customer=details,status=1)
					myform = thriftform()
					return render(request,'Ia/conthistory.html',{'company':mybranch,'user':varuser,'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render(request,'Ia/account_balance.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})




			elif staff.thrift_officer==1:
				return render(request,'Ia/account_balance_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def statementtt(request):
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


		if staff.thrift_officer==0:
				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=mywallet, status=1)
					details= tblIaCUSTOMER.objects.get(customer=details,status=1)
					myform = thriftform()
					return render(request,'Ia/contstatement.html',{'company':mybranch,'user':varuser,'form':myform,
					'customer':details,'wallet':mywallet})
				except:
					msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render(request,'Ia/account_statement.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})




			elif staff.thrift_officer==1:
				return render(request,'Ia/account_statement_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def account_history(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			acccode,wallet,month,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


			if month== '-' :
				msg = 'Select a month'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if acccode== '-----' :
				msg = 'cycle Cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			else :


				try :
					www=int(month)

					monthname = calendar.month_name[www] #converts month_index to month_name

					staff = Userprofile.objects.get(email=user,status=1)
					staffid = staff.staffrec.id

					memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff= staffid ,status=1)

					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
					details=tblIaCUSTOMER.objects.get(branch=mybranch, customer=details,status=1)

					thrift=tblIathrift.objects.get(account_type = acccode, month=monthname,customer=details)
					code=thrift.code


					CR= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=details,
						code=code,
						status='CR',
						account_type = acccode).exclude(description='Account Maintenance')


					DR= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=details,
						code=code,
						status='DR',
						account_type = acccode)



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


					# msg = cr - dr return render(request,'Ia/selectloan.html',{'msg':msg})


					add = cr - dr
					comm =''
					uu=''

					if cr - dr == 0:
						if dr  > 0 :

							comm= dr
							uu= ' Cash Withdrawn by you' #catenation needed

						elif dr== 0:

							request_count= tblIapayoutrequest.objects.filter(account_type = acccode,
								wallet_type='Main',
								merchant=memmerchant,
								status='Unpaid',
								customer=details,
								recdate__month = www)

							rqt = request_count.count()

							if rqt  > 0 :
								add=request_count.aggregate(Sum('amount'))
								add = add['amount__sum']
								add= add , 'Requested'

					return render(request,'Ia/bal.html',{
						# 'customer':details,
						'wallet':wallet,
						'comm':comm,
						'uu':uu,
						'bal':add})



				except :
					msg= 'No record found'
					msg=msg
					return render(request,'Ia/selectloan.html',{'msg':msg})


		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')






def viewwalletpop(request,vid):

	if 'userid' in request.session:
		varuser = request.session['userid']
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

		memmerchant=tblIaMERCHANT.objects.filter(branch=mybranch, staff=memstaff,thrift1a=1, status=1).count()

		details = tblCUSTOMER.objects.get(wallet= vid)

		return render(request,'Ia/cusdetail.html',{'company':mybranch, 'user':varuser,'details':details,'wallet':vid})







def unremmitted(request):   #######******** SALES BOOK*********************
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')
		if staff.thrift_officer==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.code

		mybranch=tblBRANCH.objects.get(code=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		myy = []
		gb = tblproductsname.objects.filter(branch=mybranch)


		if staff.esusu1a is True:
			# if realdet.esusu1a is True:
				hh= tblmyproducts.objects.get(product='Esusu')
				gb2=gb.get(product=hh)
				myy.append(gb2.your_product_name)

		if staff.savings1a is True:
			# if realdet.savings1a is True:
				hh= tblmyproducts.objects.get(product='Savings')
				gb2=gb.get(product=hh)
				myy.append(gb2.your_product_name)


		if request.method == 'POST':
			form = depreportform(request.POST)
			if form.is_valid():
				mystatus=form.cleaned_data['status']
				tdate=form.cleaned_data['date']

				product =request.POST['myproducts']

				g=gb.get(your_product_name=product)




				dday,mday,yday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				oydate=date(yday,mday,dday)
				oydate4= oydate.strftime('%A')

				thriftrec=[]


				if g.product.product=='Esusu':


			#########seperate this function into roles, admin, merchant, ccashier
					if mystatus=='Contribution':
						status='Deposit'

						cont_list=tblIamerchantBank.objects.filter(branch=mybranch,
							recdate=oydate,
							merchant=memmerchant,
							status='CR')


						trec =[]

						if cont_list.count() > 0:
							for kp in cont_list:
								mtv = tblIathrift.objects.get(code=kp.code)
								thrift_month = mtv.month
								amount=kp.amount
								customer=kp.customer.customer.surname + '   ' + kp.customer.customer.firstname+ '   ' + kp.customer.customer.othername
								fr={'month':thrift_month, 'trans': kp.transac_id, 'ttime':kp.ttime,'customer':customer,'amount':amount}
								trec.append(fr)

							s =cont_list.aggregate(Sum('amount'))
							s=int(s['amount__sum'])
						else:
							s=0

						return render(request,'Ia/salesbook5.html',{'company':mybranch,
							'date':oydate4,
							'date2':oydate,
							'user':varuser,
							's':s,
							'currency':currency,
							'thriftrec':trec,
							'status':status})



					elif mystatus=='Withdrawal':

						cont_list=tblIasavings_trans.objects.filter(branch=mybranch,
							recdate=oydate,
							merchant=memmerchant,
							status='DR')



						trec =[]

						if cont_list.count() > 0:
							for kp in cont_list:
								mtv = tblIathrift.objects.get(code=kp.code)
								thrift_month = mtv.month
								amount=kp.amount
								customer=kp.customer.customer.surname + '   ' + kp.customer.customer.firstname+ '   ' + kp.customer.customer.othername
								fr={'month':thrift_month, 'trans':kp.transac_id,'ttime':kp.ttime,'customer':customer,'amount':amount}
								trec.append(fr)
							w =cont_list.aggregate(Sum('amount'))
							w=int(w['amount__sum'])
						else:
							w=0


						return render(request,'Ia/salesbook4.html',{'company':mybranch,
							'date':oydate4,
							'date2':oydate,
							'user':varuser,
							'w':w,
							'currency':currency,
							'thriftrec':trec,
							'status':mystatus})


					elif mystatus == 'All':
						trec=[]

						withdrawals=tblIasavings_trans.objects.filter(branch=mybranch,
							recdate=oydate,
							merchant=memmerchant,
							status='DR')

						trec =[]

						if withdrawals.count() > 0:
							for kp in withdrawals:
								mtv = tblIathrift.objects.get(code=kp.code)
								thrift_month = mtv.month
								amount=kp.amount
								statusw=kp.status
								customer=kp.customer.customer.surname + '   ' + kp.customer.customer.firstname+ '   ' + kp.customer.customer.othername
								fr={'month':thrift_month,'customer':customer,'amount':amount,'status':statusw}
								trec.append(fr)



						sales=tblIamerchantBank.objects.filter(branch=mybranch,
							recdate=oydate,
							merchant=memmerchant,
							status='CR')


						if sales.count() > 0:
							for kp in sales:
								mtv = tblIathrift.objects.get(code=kp.code)
								thrift_month = mtv.month
								amount=kp.amount
								statusw=kp.status
								customer=kp.customer.customer.surname + '   ' + kp.customer.customer.firstname+ '   ' + kp.customer.customer.othername
								fr={'month':thrift_month,'customer':customer,'amount':amount,'status':statusw}
								trec.append(fr)




						w =withdrawals.aggregate(Sum('amount'))
						w=w['amount__sum']

						s =sales.aggregate(Sum('amount'))
						s=s['amount__sum']



					return render(request,'Ia/salesbook3.html',{'company':mybranch,
						'date':oydate4,
						'date2':oydate,
						'user':varuser,
						'w':w,
						's':s,
						'thriftrec':trec,
						'status':mystatus})
				else:
					return render(request,'Ia/selectloan.html',{'msg':g.product.product})


			else :
				msg = 'Fill up all boxes'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			return render(request,'Ia/selectloan.html',{'msg':msg})

		else:

			myy = []
			gb = tblproductsname.objects.filter(branch=mybranch)


			if staff.esusu1a is True:
				# if realdet.esusu1a is True:
					hh= tblmyproducts.objects.get(product='Esusu')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)

			if staff.savings1a is True:
				# if realdet.savings1a is True:
					hh= tblmyproducts.objects.get(product='Savings')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)


			##Add other products



			if  staff.ceo==1 :
				form=depreportform()

				if len(myy) == 1:
					return render(request,'Ia/salesbook21.html',{'company':mybranch, 'user':varuser,'form':form,'prod':myy})
				else:
					return render(request,'Ia/salesbook2.html',{'company':mybranch, 'user':varuser,'form':form,'prod':myy})


	else:
		return HttpResponseRedirect('/login/user/')



def fa_unremmitted(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')
		if staff.thrift_officer==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.code

		mybranch=tblBRANCH.objects.get(code=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form = viewtransform(request.POST)
			if form.is_valid():
				mystatus=form.cleaned_data['status']
				tdate=form.cleaned_data['date']


				dday,mday,yday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				oydate=date(yday,mday,dday)
				oydate4= oydate.strftime('%A')

				thriftrec=[]
				if mystatus=='DR':
					status='Sales'

					ss = tblIasavings_trans.objects.filter(branch=mybranch,
						merchant=memmerchant, product='Savings',status='CR',
						recdate=oydate)

					trec=tblIafieldagent.objects.filter(branch=mybranch,
						recdate=oydate,
						merchant=memmerchant).order_by('status')

					approved = trec.filter(status='Approved')
					unapproved = trec.filter(status='Unapproved')
					declined = trec.filter(status='Declined')


					failed=[]
					allfailed=[]


					if approved.count() > 0:
						approved =approved.aggregate(Sum('amount'))
						approved=int(approved['amount__sum'])
					else:
						approved=0


					if unapproved.count() > 0:
						unapproved =unapproved.aggregate(Sum('amount'))
						unapproved=int(unapproved['amount__sum'])
					else:
						unapproved=0

					if declined.count() > 0:
						declined =declined.aggregate(Sum('amount'))
						declined=int(declined['amount__sum'])
					else:
						declined=0


					for t in trec:
						if t.status=='Unapproved':
							status1='Not yet Deposited'

						elif t.status=='Declined':
							status1='Declined'

						elif t.status=='Approved':
							gg=ss.filter(transac_id=t.transac_id)
							status1='Approved'


							if t.programmm == "X + Nj":

								if int(t.number) > 1:

									if gg.count() < 2:
										status1='Failed to Deposit'
										d= gg.get()
										cc = int(d.amount)
										failed.append(int(t.amount) - cc )
										allfailed.append(int(t.amount) - cc )
									else:
										status1='Deposited'

								elif int(t.number)  ==1 :
									if gg.count()==0:
										status1='Failed to Deposit'
										failed.append(int(t.amount))
										allfailed.append(int(t.amount))

									else:
										status1='Deposited'

							elif t.programmm == "Nj":
								if gg.count()==0:
									status1='Failed to Deposit'
									failed.append(int(t.amount))
									allfailed.append(int(t.amount))
								else:

									status1='Deposited'





						if len(failed) > 0:
							failed = failed[0]
						else:
							failed=0



						kl={'customer':t.customer,'Failed':failed,'Amount':t.amount,'Approval':t.status,'Status':status1,'transaction_code':t.transac_id}
						thriftrec.append(kl)
						failed=[]


					allfailed= sum(allfailed)


					return render(request,'Ia/salesbook1.html',{'company':mybranch,
						'date':oydate4,
						'date2':oydate,
						'user':varuser,
						'currency':currency,
						'approved':approved,
						'unapproved':unapproved,
						'declined':declined,
						'Failed':allfailed,
						'ttt':thriftrec,
						'status':status})


				else:
					msg = 'fggf'
					return render(request,'Ia/selectloan.html',{'msg':msg})

		else:

			myy = []
			gb = tblproductsname.objects.filter(branch=mybranch)


			if staff.esusu1a is True:
				if memmerchant.esusu1a is True:
					hh= tblmyproducts.objects.get(product='Esusu')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)

			if staff.savings1a is True:
				if memmerchant.savings1a is True:
					hh= tblmyproducts.objects.get(product='Savings')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)


			##Add other products/ services


			if staff.thrift_officer==1:
				form =viewtransform()
				return render(request,'Ia/salesbook.html',{'company':mybranch, 'user':varuser,'form':form,'prod':myy})

	else:
		return HttpResponseRedirect('/login/user/')
#######******** END OF SALES BOOK*********************

##########    WRITHDRAWAL ************************

def cashout(request):
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


		if staff.thrift_officer==0:
				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']

				try:
					details=tblCUSTOMER.objects.get(branch=mybranch,wallet=mywallet,status=1)
					myform = thriftform()

					if staff.admin == 1:
						details=tblIaCUSTOMER.objects.get(customer=details,status=1)
						return render(request,'Ia/reqcash.html',{'company':mybranch,
							'user':varuser,
							'form':myform,
							'customer':details,
							'wallet':mywallet})


					if staff.thrift_officer == 1:
						try:

							details=tblIaCUSTOMER.objects.get(merchant=memmerchant, customer=details,status=1)
							return render(request,'Ia/reqcash_to.html',{'company':mybranch,
								'user':varuser,
								'form':myform,
								'customer':details,
								'wallet':mywallet})
						except:
							msg= 'Make sure you are RESPONSIBLE for this customer'
							return render(request,'Ia/selectloan.html',{'msg':msg})

				except:
					msg='INVALID WALLET ADDRESS'
					return render(request,'Ia/selectloan.html',{'msg':msg})
			else:
				msg='Incorrect entry'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			form=viewwalletform()
			msg = ''
			if staff.admin==1:
				return render(request,'Ia/cashout.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

			else:
				msg = 'direct all withdrawals through admin'
				return render(request,'Ia/selectloan.html',{'msg':msg})




			# elif staff.thrift_officer== 1:
			# 	return render(request,'Ia/cashout_to.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def account_withdrawh(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			acccode,wallet,month,user=acccode.split(':')
			staff = Userprofile.objects.get(email=user,status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)


			currency=mybranch.currency_code

			if month== '-':
				msg = 'Select a month'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if acccode== '-----' :
				msg = 'cycle Cycle'
				return render(request,'Ia/selectloan.html',{'msg':msg})


			www=int(month)
			yyr=date.today().year
			monthname = calendar.month_name[www]
			acccode=unicode(acccode)

			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,
				staff= staffdet ,status=1)

			customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			customer=tblIaCUSTOMER.objects.get(customer=customer,status=1)


			try:
				cus_thrift=tblIathrift.objects.get(
					account_type = acccode,
					branch=mybranch,
					customer=customer,
					year=yyr,
					month = monthname)

				if cus_thrift.withdraw_status==0:
					mythrift=cus_thrift.thrift
					code = cus_thrift.code

					dll = []
					ALLTOT= tblIasavings_trans.objects.filter(
						branch=mybranch,
						customer=customer,
						code=code,
						account_type = acccode)

					CR=ALLTOT.filter(status='CR').exclude(description='Account Maintenance')

					DR=ALLTOT.filter(status='DR')

					# msg =DR.count() #'you have withdrawn your funds for the month'
					# return render(request,'Ia/selectloan.html',{'msg':msg})

					if CR.count() > 0 :
						cr=CR.aggregate(Sum('amount'))
						cr = cr['amount__sum']

						nc=CR.aggregate(Sum('number'))
						nc = nc['number__sum']

					else:
						cr =0
						nc=0

					if DR.count() > 0 :
						dr=DR.aggregate(Sum('amount'))
						dr = dr['amount__sum']

						nd=DR.aggregate(Sum('number'))
						nd= nd['number__sum']


					else:
						dr = 0
						nd=0



					try:
						add = int(cr - dr)
					except:
						add = cr - dr


					try:
						number =int(nc - nd)
					except:
						number =nc - nd



					jdjd= {'amount':add,'num':number,'thrift':mythrift}

					dll.append(jdjd)


					if staff.thrift_officer==0:
						msg = 'you are not allowed to do this'
						return render(request,'Ia/selectloan.html',{'msg':msg})
					else:
						return render(request,'Ia/withdrr.html',{'thriftrec':dll,
							'wallet':wallet,
							'month':www,
							'count':number,
							'currency':currency,
							'monthname':monthname,
							'account_type':acccode,
							'thrift':mythrift})


				else:
					msg ='you have withdrawn your funds for the month'
					return render(request,'Ia/selectloan.html',{'msg':msg})

			except:
				msg = 'No thrift record found'
				return render(request,'Ia/selectloan.html',{'msg':msg})



		else:
			return HttpResponseRedirect('/dalogin/')

	else:
		return HttpResponseRedirect('/dalogin/')






def individual(request):
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

	if staff.admin==0:
		return render(request,'Ia/404.html',{'company':mybranch,'user':varuser})

	if request.method == 'POST':
		form = remittalform(request.POST)
		if form.is_valid():
			merchant =form.cleaned_data['merchant']
			mydate2=form.cleaned_data['date']  #JavaScript Date Object

			yday,mday,dday = mydate2.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #Python Date Object

			try:
				memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1,branch=mybranch)
			except:
				form=remittalform()
				msg = 'INVALID MERCHANT ID'
				return render(request,'Ia/remittals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

			ddt=[]
			thriftrec= tblIasavings_trans.objects.filter(
				branch=mybranch,
				merchant=merchant,
				recdate=mydate,
				wallet_type='Main',
				remitted='Unremmitted',
				approved='Not Approved')

			mycount= thriftrec.count()

			if mycount >0:
				add=thriftrec.aggregate(Sum('amount'))
				add = add['amount__sum']
				dl={'amount':add}
				ddt.append(dl)

				return render(request,'Ia/remhistory.html',{'company':mybranch,'dates':mydate2,
					'merchant':memmerchant,
					'user':varuser,'thriftrec':ddt,
					'date':mydate,'ttt':thriftrec})

			else:
				msg ='NO TRANSACTION FOUND'
		else:
			form=remittalform()
			msg=''
			return render(request,'Ia/remittals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def seedit(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,trandate=acccode.split(':')

			try:
				mycom = tblIafieldagent.objects.get(id=state, status='Received') #details of the trans on merchant tab

				return render(request,'Ia/app_trans.html',{'income':mycom,'date1':trandate})

			except :
				msg='error !!!'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')


def approveone(request):
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

		if staff.admin==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			merchant2=request.POST['merchant']
			transid = request.POST['trans']
			cash =request.POST['cash'] #posted
			amount =request.POST['mmm'] #carry come
			mydate2=request.POST['date1'] #Javascript date object

			amount=int(amount)
			cash=int(cash)


			dday,mday,yday = mydate2.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object

			fdate= date.today() #record date, the date you took record
			remterr=date(fdate.year,fdate.month,fdate.day)
			merchant=tblSTAFF.objects.get(branch=mybranch,email=varuser)

			merchant=tblIaMERCHANT.objects.get(staff=merchant,thrift1a=1) #admin

			merchant2=tblIaMERCHANT.objects.get(id=merchant2)

			ttt =tblIafieldagent.objects.get(id=transid,status='Received')
			code = ttt.code
			thrift = int(ttt.amount / ttt.number)
			transdate = ttt.recdate #date the original transaction happened
			customer = ttt.customer.customer.id
			number= ttt.number
			transaction_id=ttt.transac_id

			pl= number-1


			customer=tblCUSTOMER.objects.get(branch=mybranch, id=customer)
			customer=tblIaCUSTOMER.objects.get(customer=customer)
			wallet=customer.customer.wallet

			# monthname = calendar.month_name[fdate.month]
			th = tblIathrift.objects.get(branch=mybranch,account_type=account_type,customer=customer,code=code,year =fdate.year)
			code = th.code

			ddt=[]

			# p = (monthrange(fdate.year, fdate.month))[-1]
			p=31


			new_amount = amount - thrift

			# msgk = p, number,pl,l # return render(request,'Ia/selectloan.html',{'msg':msgk})

			if amount == cash :
				mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch, customer=customer, transdate=transdate, status='CR',  purpose = card, wallet_type='Main')

				kdf= mont_contribution.count()

				if kdf == 0 :
					add_count = 0
				else:
					add_count = mont_contribution.aggregate(Sum('number'))
					add_count = add_count['number__sum']

				if add_count + number <= p:
					# msgk = add_count , lump , p
					# return render(request,'Ia/selectloan.html',{'msg':msgk})

					if add_count == 0:
						if number == 1:
							try:
								tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=1, transdate=transdate, amount=amount,purpose = card,wallet_type='Main',approved_by=varuser)

							except:
								tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id, customer=customer,number=1,recdate=fdate,transdate=transdate, amount=amount,purpose = card,wallet_type='Main',approved_by=varuser,description='Credit',status='CR').save()
								tblIasavings_trans(branch=mybranch, merchant=merchant2, code=code, transac_id= transaction_id,customer=customer, number=1,transdate=transdate, recdate=fdate,amount=amount, status='CR', purpose = card,  wallet_type='Main',  avalability='Not Available', description='Account Maintenance').save()
								ttt.status = 'Approved'
								ttt.save()
								return render(request,'Ia/apsuccess.html',{'company':mybranch,'user':varuser,'customer':customer,'wallet':wallet,'amount':amount})

						elif number > 1:
							try:
								tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=number,transdate=transdate, amount=amount,purpose = card,approved_by=varuser,wallet_type='Main')
							except :
								tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id,customer=customer,number=number,transdate=transdate ,recdate=fdate, amount=amount,purpose = card,approved_by=varuser,wallet_type='Main',description='Credit', status='CR').save()
								tblIasavings_trans(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id,customer=customer,number=1,transdate=transdate,recdate= fdate,amount=thrift,status='CR',purpose = card,wallet_type='Main',avalability='Not Available',description='Account Maintenance').save()
								tblIasavings_trans(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id,customer=customer,number=pl,transdate=transdate,recdate=fdate,amount=new_amount,status='CR',purpose = card,wallet_type='Main',avalability='Available',description='Credit').save()
								ttt.status = 'Approved'
								ttt.save()
								return render(request,'Ia/apsuccess.html',{'company':mybranch,'user':varuser,'customer':customer,'wallet':wallet,'amount':amount})

					elif add_count > 0:
						try:
							tblIamerchantBank.objects.get(branch=mybranch,merchant=merchant2,code=code,customer=customer,number=number,transdate=transdate, purpose = card,approved_by=varuser,wallet_type='Main')
							msg = "you cant post same money twice same day"
						except:
							tblIamerchantBank(branch=mybranch,merchant=merchant2,code=code,transac_id= transaction_id,customer=customer,number=number,transdate=transdate, recdate=fdate,amount=amount,purpose = card,approved_by=varuser,wallet_type='Main',description='Credit',status='CR').save()
							tblIasavings_trans(branch=mybranch,	merchant=merchant2, code=code, transac_id= transaction_id, customer=customer,number=number,transdate=transdate, recdate=fdate,amount=amount, status='CR',purpose = card, wallet_type='Main',avalability='Available', description='Credit').save()
							ttt.status = 'Approved'
							ttt.save()
							return render(request,'Ia/apsuccess.html',{'company':mybranch,'user':varuser,'customer':customer,'wallet':wallet,'amount':amount})


				else:
					msg = "Amount too large"
			else:
				msg = 'amount not applicable'
			return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')


	else:
		return HttpResponseRedirect('/login/user/')



def approveind(request):
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

		if staff.admin==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			merchant =request.POST['merchant']
			mydate2=request.POST['cdate']  #JavaScript Date Object
			cid = request.POST['cid']
			amount=request.POST['total']
			account_type=request.POST['account_type']
			transid=request.POST['transid']

			yday,mday,dday = mydate2.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #Python Date Object

			customer = tblCUSTOMER.objects.get(id =cid,status=1)
			customer1=customer.id
			mymerchant= tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1)

			myadmin = tblIamerchantBank.objects.get(id = transid)

			add =myadmin.amount
			remtotal=myadmin.amount

			return render(request,'Ia/approvalindv.html',{'company':mybranch,
				'merchant':mymerchant,'customer':customer1,
				'user':varuser,'date':mydate,
				'thriftrec':myadmin, 'trannsid':transid,
				'cdate':mydate2,'total':add,'rem':remtotal})

	else:
		return HttpResponseRedirect('/logout/')


def approveindividualcash(request):
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

		if staff.admin==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			merchant =request.POST['merchant']
			mydate=request.POST['date']
			customer=request.POST['customer'] #already a database instance
			amount=request.POST['rem']
			transid=request.POST['transid']

			yday,mday,dday = mydate.split('/')

			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			transdate=date(yday,mday,dday)
			ddt=[]

			merchant=tblIaMERCHANT.objects.get(thrift1a =1,status=1,id=merchant)

			remit = tblIamerchantBank.objects.get( id = transid)

			account_type=remit.account_type
			code=remit.code

			customer=tblCUSTOMER.objects.get(id=customer,status=1)

			mythrift=tblIathrift.objects.get(purpose = card,branch=mybranch,
				customer=customer,number=mday,year=yday)

			customer_thrift = mythrift.thrift

			number= remit.amount / customer_thrift

			pl= number-1

			new_amount = remit.amount - customer_thrift

			mont_contribution = tblIathrift_trans.objects.filter(account_type =account_type ,wallet_type='Main', branch=mybranch,
				merchant=merchant,
				customer=customer,recdate__month=mday).count()


			if mont_contribution < 1:

				if number == 1:
					tblIathrift_trans(
						purpose = card,
						wallet_type='Main',
						branch=mybranch,
						code=code,
						merchant=merchant,
						customer=customer,
						number=1,
						recdate=transdate,
						amount=customer_thrift,
						avalability='Not Available',
						reason='Account Maintenance').save()

				else :
					tblIathrift_trans(
						purpose = card,
						wallet_type='Main',
						branch=mybranch,
						code=code,
						merchant=merchant,
						customer=customer,
						number=1,
						recdate=transdate,
						amount=customer_thrift,
						avalability='Not Available',
						reason='Account Maintenance').save()

					tblIathrift_trans(
						purpose = card,
						wallet_type='Main',
						branch=mybranch,
						code=code,
						merchant=merchant,
						customer=customer,
						number=pl,
						recdate=transdate,
						amount=new_amount,
						avalability='Available',
						reason='Available').save()

			else:
				tblIathrift_trans(
					purpose = card,
					wallet_type='Main',
					branch=mybranch,
					merchant=merchant,
					customer=customer,
					number=number,
					recdate=transdate,
					amount=remit.amount,
					code=code,
					avalability='Available',
					reason='Available').save()

			remit.status='Approved'
			remit.approved_by=varuser
			remit.save()

			return render(request,'Ia/approve_success.html',{'company':mybranch,'tot':1,'user':varuser})

		else:
			form=remittalform()
		return render(request,'Ia/remittals.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')







def all(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.admin==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			# return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.filter(staff=memstaff,thrift1a=1, status=1)

		if request.method == 'POST':
			form = viewremallform(request.POST)
			if form.is_valid():
				# checkbox =request.POST['checkbox']
				mydate=form.cleaned_data['date']
				yday,mday,dday = mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				ddt=[]

				ddd= dday+1

				for d in xrange(ddd):
					if d == 0:
						pass
					else:
						mydate= date(yday,mday,d)

						for merchant in memmerchant:
							thrifing= tblIasavings_trans.objects.filter(branch=mybranch,
								recdate=mydate,wallet_type='Main',remitted='Unremmitted',merchant=merchant)

							mycount= thrifing.count()

							if mycount >0:
								add=thrifing.aggregate(Sum('amount'))
								add = add['amount__sum']
								dl={'date':mydate,'amount':add,'merchant':merchant,'remitted':'Unremmitted'}
								ddt.append(dl)
							else:
								pass

				return render(request,'Ia/allrem.html',{'company':mybranch, 'user':varuser,'thriftrec':ddt,'date':mydate})

		else:
			form=viewremallform()
		return render(request,'Ia/all.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')


def report(request):
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
		if staff.admin==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			if form.is_valid():
				status=form.cleaned_data['status']
				date1=form.cleaned_data['date']
				yday,mday,dday = date1.split('/')

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday)
				month = calendar.month_name[mday]

				allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1

				if checkbox==1:
					if status == 'Remitted':
						for k in allmerchant:
							thriftrec= tblIamerchantBank.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Unremmitted':
						for p in allmerchant:
							thriftrec= tblIasavings_trans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=mydate,merchant=p)
							add =0

							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)

					return render(request,'Ia/remreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'status':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:
								thriftrec= tblIamerchantBank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':mn,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'Unremmitted':
							for kl in allmerchant:
								thriftrec= tblIasavings_trans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

					return render(request,'Ia/histremreport.html',{'company':mybranch, 'user':varuser,
						'thriftrec':all_data,'month':month,'year':yday,'status':status})

		else:
			form=viewallremittedform()
		return render(request,'Ia/report.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def approvalsmenu(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.admin ==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			merchant_id=request.POST['merchant']
			mydate=request.POST['date'] #js date object
			yday,mday,dday=mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			transdate=date(yday,mday,dday)

			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant_id, status=1)

			remit = tblIamerchantBank.objects.filter(
				branch=mybranch,
				recdate = transdate,
				merchant=memmerchant,
				status='Remitted')


			remamount = tblIamerchantBank.objects.filter(
				branch=mybranch,
				recdate=transdate,
				merchant=memmerchant,
				status='Remitted')

			ggt=[]

			for k in remit:
				name=k.customer.surname + "   "+k.customer.firstname
				customer=k.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)
				account_type=k.account_type

				cus_thrift = tblIathrift.objects.get(
					customer=customer,
					# merchant=memmerchant,
					number = mday,
					account_type=account_type,
					year=yday)
				cus_thrift=cus_thrift.thrift
				df={'thrift':cus_thrift,'amount':k.amount,'name':name,'status':'Not Approved'}
				ggt.append(df)

			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)


			remtotal=remamount.aggregate(Sum('amount'))
			remtotal = remtotal['amount__sum']
			remtotal = int(remtotal)

			return render(request,'Ia/approvalhistory.html',{
				'company':mybranch,
				 'merchant':memmerchant,
				 'user':varuser,
				 'date':transdate,
				 'thriftrec':ggt,
				 'cdate':mydate,
				 'total':add,
				 'rem':remtotal})

	else:
		return HttpResponseRedirect('/login/user/')

def approvecash(request):
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

		if staff.admin==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			merchant =request.POST['merchant']

			mydate=request.POST['date'] #JS date object
			dday,mday,yday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			transdate=date(yday,mday,dday) #python date object

			ddt=[]
			merchant=tblIaMERCHANT.objects.get(thrift1a =1,status=1,id=merchant)

			remit = tblIamerchantBank.objects.filter(
				branch=mybranch,
				merchant=merchant,
				recdate = transdate,
				status='Remitted')

			msg='wahalla'

			count=remit.count()

			for k in remit:
				code=k.code
				amount=k.amount
				customer=k.customer.id
				account_type=k.account_type
				customer=tblCUSTOMER.objects.get(id=customer,status=1)
				mythrift=tblIathrift.objects.get(
					purpose = card,
					branch=mybranch,
					customer=customer,
					number = mday,
					year=yday)
				customer_thrift = mythrift.thrift
				number= int(amount / customer_thrift)

				pl= number-1
				new_amount = amount - customer_thrift

				mont_contribution = tblIathrift_trans.objects.filter(
					purpose = card,
					wallet_type='Main',
					branch=mybranch,
					merchant=merchant,
					customer=customer,
					recdate__month=mday).count()

				if mont_contribution < 1:

					if number == 1:
						msg = 'i am 1'
						tblIathrift_trans(
							branch=mybranch,
							merchant=merchant,
							code=code,
							customer=customer,
							number=1,
							recdate=transdate,
							amount=customer_thrift,
							purpose = card,
							wallet_type='Main',
							avalability='Not Available',
							reason='Account Maintenance').save()

					elif number > 1:
						msg = ' i  am 2'
						tblIathrift_trans(
							branch=mybranch,
							merchant=merchant,
							code=code,
							customer=customer,
							number=1,
							recdate=transdate,
							amount=customer_thrift,
							purpose = card,
							wallet_type='Main',
							avalability='Not Available',
							reason='Account Maintenance').save()

						tblIathrift_trans(
							branch=mybranch,
							merchant=merchant,
							code=code,
							customer=customer,
							number=pl,
							recdate=transdate,
							amount=new_amount,
							purpose = card,
							wallet_type='Main',
							avalability='Available',
							reason='Available').save()

				elif mont_contribution > 0 :
					msg = 'i am 3'
					tblIathrift_trans(
						purpose = card,
						wallet_type='Main',
						branch=mybranch,
						merchant=merchant,
						customer=customer,
						code=code,
						number=number,
						recdate=transdate,
						amount=k.amount,
						avalability='Available',
						reason='Available').save()

				k.status='Approved'
				k.approved_by=varuser
				k.save()

			msg=msg
			# return render(request,'Ia/selectloan.html',{'msg':msg})


			return render(request,'Ia/apsuccess.html',{'company':mybranch,'tot':count,'user':varuser})

		else:
			form=remittalform()
		return render(request,'Ia/remittals.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')








@csrf_exempt
def approvvedsalesdetails(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate=acccode.split(':')
			mm = tblIaMERCHANT.objects.get(id=state)
			product='Esusu'

			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wrd_date=date(y,m,d)

			dpp = calendar.day_name[calendar.weekday(y,m,d)]

			return render(request,'Ia/salesdetapproved.html',{'date2':wrd_date,
				'dow':dpp,'trans_id':state,
				'hhh':mm,'product':product})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def salesdetails___3(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate,status=acccode.split(':')
			mm = tblIaMERCHANT.objects.get(id=state)
			product='Esusu'

			branch=mm.branch.id
			mybranch=tblBRANCH.objects.get(id=branch)
			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wrd_date=date(y,m,d)


			dpp = calendar.day_name[calendar.weekday(y,m,d)]

			if status == '':
				msg = 'Select appropriate status'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if status == 'Approved':
				customer=tblIafieldagent.objects.filter(branch=mybranch,
					is_declined=0,
					merchant=state,
					status='Approved',
					recdate=wrd_date)

			elif status =='Declined':
				customer=tblIafieldagent.objects.filter(branch=mybranch,
					is_declined=1,
					merchant=state,
					status='Declined',
					recdate=wrd_date)


			if customer.count() ==0:
				msg= 'NO RECORDS FOUND'
				return render(request,'Ia/selectloan.html',{'msg':msg})
			else:
				add=customer.aggregate(Sum('amount'))
				payable_sum = int(add['amount__sum'])


			return render(request,'Ia/salesdetapproved2.html',{'company':mybranch,'date1':recdate,'product':product,
				'date2':wrd_date, 'trans_id':state,'hhh':mm,'dow':dpp, 'customer':customer,'sales':payable_sum})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')











@csrf_exempt
def salesdetails(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate=acccode.split(':')
			mm = tblIaMERCHANT.objects.get(id=state)
			product='Esusu'

			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wrd_date=date(y,m,d)

			dpp = calendar.day_name[calendar.weekday(y,m,d)]

			return render(request,'Ia/salesdet.html',{'date2':wrd_date,
				'dow':dpp,'trans_id':state,
				'hhh':mm,'product':product})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def salesdetails___2(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate,status=acccode.split(':')
			mm = tblIaMERCHANT.objects.get(id=state)
			product='Esusu'

			branch=mm.branch.id
			mybranch=tblBRANCH.objects.get(id=branch)
			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wrd_date=date(y,m,d)


			dpp = calendar.day_name[calendar.weekday(y,m,d)]

			if status == '':
				msg = 'Select appropriate status'
				return render(request,'Ia/selectloan.html',{'msg':msg})

			if status == 'Unapproved':
				customer=tblIafieldagent.objects.filter(branch=mybranch,
					is_declined=0,
					merchant=state,
					status='Unapproved',
					recdate=wrd_date)

			elif status =='Declined':
				customer=tblIafieldagent.objects.filter(branch=mybranch,
					is_declined=1,
					merchant=state,
					status='Declined',
					recdate=wrd_date)


			if customer.count() ==0:
				msg= 'NO RECORDS FOUND'
				return render(request,'Ia/selectloan.html',{'msg':msg})
			else:
				add=customer.aggregate(Sum('amount'))
				payable_sum = int(add['amount__sum'])


			return render(request,'Ia/salesdet2.html',{'company':mybranch,'date1':recdate,'product':product,
				'date2':wrd_date, 'trans_id':state,'hhh':mm,'dow':dpp, 'customer':customer,'sales':payable_sum})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')

@csrf_exempt
def customerdepcancel(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate=acccode.split(':')

			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wd_date=date(y,m,d)
			customer=tblIafieldagent.objects.get(transac_id = state, status='Unapproved',recdate=wd_date)

			return render(request,'Ia/deletesales.html',{'date1':recdate,
				'date2':wd_date, 'trans_id':state,'hhh':customer})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')


def cancelapprono(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']


		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)

		# transdate=date(yday,mday,dday)
		# dow = calendar.month_name[mday]
		dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]
		product='Esusu'



		remit = tblIafieldagent.objects.filter(branch=mybranch,
			recdate = transdate,
			is_declined=0,
			wallet_type='Main',
			status='Unapproved')


		sdic= {}
		kk=[]


		for j in remit:
			j = j.merchant.id  #uses ID from tblSTAFF
			s = {j:j}
			sdic.update(s)
		klist = sdic.values()
		for p in klist:
			kk.append(p)



		count=remit.count()

		if count>0:
			kpp=[]
			for k in kk:
				merchant= tblIaMERCHANT.objects.get(id=k)

				merch= remit.filter(merchant=merchant)

				merch = remit.filter(merchant=k)

				m1=merch.aggregate(Sum('amount'))
				m2 = m1['amount__sum']
				add3 = int(m2)

				s={'merchant':merchant,'sales':add3,'id':k}
				kpp.append(s)


			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render(request,'Ia/ppp.html',{'company':mybranch,
				'user':varuser,
				'thriftrec':kpp,
				'dates':transdate,
				'dow':dpp,
				'product':product,
				'cdate':mydate,
				'total':add})
		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')




def cancelesuyes(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']



		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)


		dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]
		product='Esusu'


		remit = tblIafieldagent.objects.filter(
			wallet_type='Main',
			recdate = transdate,
			transac_id=trans_id,
			status='Unapproved').update(is_declined=1,status='Declined')


		remit = tblIafieldagent.objects.filter(branch=mybranch,
			recdate = transdate,
			is_declined=0,
			wallet_type='Main',
			status='Unapproved')


		sdic= {}
		kk=[]


		for j in remit:
			j = j.merchant.id  #uses ID from tblSTAFF
			s = {j:j}
			sdic.update(s)
		klist = sdic.values()
		for p in klist:
			kk.append(p)



		count=remit.count()

		if count>0:

			kpp=[]
			for k in kk:
				merchant= tblIaMERCHANT.objects.get(id=k)

				merch= remit.filter(merchant=merchant)

				merch = remit.filter(merchant=k)

				m1=merch.aggregate(Sum('amount'))
				m2 = m1['amount__sum']
				add3 = int(m2)

				s={'merchant':merchant,'sales':add3,'id':k}
				kpp.append(s)


			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render(request,'Ia/reconciliaton_esusu.html',{'company':mybranch,
				'user':varuser,
				'thriftrec':kpp,
				'product':product,
				'dow':dpp,
				'dates':transdate,
				'cdate':mydate,
				'currency':currency,
				'total':add})

		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def reclineme(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate=acccode.split(':')

			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wd_date=date(y,m,d)
			customer=tblIafieldagent.objects.get(id = state, is_declined=1, status='Declined',recdate=wd_date)

			return render(request,'Ia/reclin.html',{'date1':recdate,
				'date2':wd_date, 'trans_id':state,'hhh':customer})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')





def reclppro(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']


		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)


		dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]
		product='Esusu'


		remit = tblIafieldagent.objects.filter( id =trans_id,
			branch=mybranch,
			wallet_type='Main',
			recdate = transdate,
			status='Declined').update(is_declined=0,status='Unapproved')

		# return render(request,'Ia/selectloan.html',{'msg':remit})


		remit = tblIafieldagent.objects.filter(branch=mybranch,
			recdate = transdate,
			is_declined=0,
			wallet_type='Main',
			status='Received')


		sdic= {}
		kk=[]


		for j in remit:
			j = j.merchant.id  #uses ID from tblSTAFF
			s = {j:j}
			sdic.update(s)
		klist = sdic.values()
		for p in klist:
			kk.append(p)



		count=remit.count()

		if count>0:
			kpp=[]
			for k in kk:
				merchant= tblIaMERCHANT.objects.get(id=k)

				merch= remit.filter(merchant=merchant)

				merch = remit.filter(merchant=k)

				m1=merch.aggregate(Sum('amount'))
				m2 = m1['amount__sum']
				add3 = int(m2)

				s={'merchant':merchant,'sales':add3,'id':k}
				kpp.append(s)


			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render(request,'Ia/ppp.html',{'company':mybranch,
				'user':varuser,
				'thriftrec':kpp,
				'dates':transdate,
				'dow':dpp,
				'product':product,
				'cdate':mydate,
				'currency':currency,
				'total':add})
		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def reedit(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			merchant,user,trandate=acccode.split(':')

			dday,mday,yday = trandate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			transdate=date(yday,mday,dday)


			dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]



			chkstaff = tblSTAFF.objects.get(email=user,status=1)
			bra = chkstaff.branch.id
			mybranch= tblBRANCH.objects.get(id = bra)

			currency= mybranch.currency_code

			ddt=[]

			if merchant=='undefined':
				heading = 'Bulk Approval for all unapproved cash'
				thriftrec = tblIafieldagent.objects.filter(branch=bra,
					recdate = transdate,
					is_declined = 0,
					wallet_type='Main',
					status='Unapproved')

			else:
				co=tblIaMERCHANT.objects.get(id=merchant)
				heading=co.staff.surname + " " + co.staff.firstname + " " + co.staff.othername + "'s" + " "+ "unapproved cash"
				thriftrec = tblIafieldagent.objects.filter(branch=bra,
					merchant=co,
					recdate = transdate,
					is_declined = 0,
					wallet_type='Main',
					status='Unapproved')


			mycount= thriftrec.count()
			# return render(request,'Ia/selectloan.html',{'msg':mycount})

			if mycount >0:
				add=thriftrec.aggregate(Sum('amount'))
				add = int(add['amount__sum'])
				dl={'amount':add}
				ddt.append(dl)

				return render(request,'Ia/ppp_all.html',{
					'company':mybranch,
					'dates':trandate,
					'thriftrec':ddt,
					'dow':dpp,
					'heading':heading,
					'merchant':merchant,
					'product':'Esusu',
					'tot':add,
					'date':transdate,
					'ttt':thriftrec})
			else:

				msg = 'This page has expired, please refresh it'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




def approvebulkcash(request):
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
		currency=mybranch.currency_code
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		# return render(request,'Ia/selectloan.html',{'msg':ceo})

		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			amount1 =request.POST['amount'] #carry come
			mydate2=request.POST['dates'] #Javascript date object
			credit_officer=request.POST['merchant']
			mydate22 = request.POST['date']
			cash =request.POST['cash'] #posted

			amount1=int(amount1)
			cash=int(cash)

			dday,mday,yday = mydate2.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object

			fdate= date.today() #record date, the date you took record
			remterr=date(fdate.year,fdate.month,fdate.day)


			if credit_officer=='undefined':

				ttt = tblIafieldagent.objects.filter(branch=mybranch,
					recdate = mydate,
					is_declined = 0,
					wallet_type='Main',
					status='Unapproved')

			else:
				co=tblIaMERCHANT.objects.get(id=credit_officer)

				ttt = tblIafieldagent.objects.filter(branch=mybranch,
						merchant=co,
						recdate = mydate,
						is_declined = 0,
						wallet_type='Main',
						status='Unapproved')



			mdm =[]
			dsr = []
			[mdm.append(k.merchant.id) for k in ttt if k.merchant.id not in mdm] #remove repeatiton

			for gv in mdm:
				merchant=tblIaMERCHANT.objects.get(id=gv)
				tq = ttt.filter(merchant=merchant)
				tm = tq.aggregate(Sum('amount'))
				TotalSales = int(tm['amount__sum'])

				vv = {'mer':merchant,'sales':TotalSales}
				dsr.append(vv)



			if amount1 == cash :
				dddy = datetime.today()
				ddd = dddy.date()
				tti=dddy.time()

				for fld in ttt :
					customer_id = fld.customer.id
					customer=tblIaCUSTOMER.objects.get(id=customer_id)
					transaction_code= fld.transac_id

					code=fld.code

					card= fld.purpose
					cycle=fld.cycle
					mer= fld.merchant.id
					merchant2 =tblIaMERCHANT.objects.get(id=mer)

					mont_contribution = tblIasavings_trans.objects.filter(branch=mybranch,
						customer=customer,
						status='CR',
						code=code,
						purpose = card,
						cycle=cycle,
						wallet_type='Main')

					kdf= mont_contribution.count()


					if kdf == 0 :
						add_count = 0
					else:
						add_count = mont_contribution.aggregate(Sum('number'))
						add_count = int(add_count['number__sum'])

					ty = reconciliation(fld, staff,mybranch,transaction_code, add_count)


				return render(request,'Ia/selectloan.html',{'msg':ty})
				return render(request,'Ia/all_app_success.html',{
					'company':mybranch,
					'fo':merchant2,
					'admin':staff,
					'dsr':dsr,
					'date':ddd,
					'time':tti,
					'currency':currency,
					'user':varuser,
					'amount':amount1})


			else:
				msg = 'amount not applicable'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')



	else:
		return HttpResponseRedirect('/login/user/')






def approvalsmenuyes(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render(request,'Ib/404.html',{'company':mybranch, 'user':varuser})


		# merchant2=request.POST['merchant']
		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']

		# merchanttrans=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,id=merchant2, status=1)

		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)

		try:

			remit = tblIafieldagent.objects.filter( id =trans_id,
				branch=mybranch,
				merchant=merchanttrans,
				wallet_type='Main',
				recdate = transdate,
				status='Received').delete()
		except:
			pass


			###add a delete notification


		remit = tblIafieldagent.objects.filter( branch=mybranch,
			merchant=merchanttrans,
			wallet_type='Main',
			recdate = transdate,
			status='Received')

		count=remit.count()
		# ggt=[]

		if count>0:

			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render(request,'Ia/ppp.html',{'company':mybranch,
				'merchant':merchanttrans,
				'user':varuser,
				'thriftrec':remit,
				'dates':transdate,
				'cdate':mydate,
				'total':add,
				})
		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')

def allapproval(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.admin==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			# return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			merchant =request.POST['merchant']
			mydate=request.POST['date']
			yday,mday,dday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			transdate=date(yday,mday,dday)
		else:
			form=viewallremittedform()
		return render(request,'Ia/all_to.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')



def approvereport(request):
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
		currency=mybranch.currency_code
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form  = form=viewallapprovedform(request.POST)
			status =request.POST['status']
			mydate=request.POST['date'] #javascript date object
			dday,mday,yday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			realmonth=calendar.month_name[mday]

			allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=1,thrift1a=1)


			if status =='Reconciliation':

				transaction_source = tblIafieldagent.objects.filter(branch=mybranch,
					status='Approved',wallet_type='Main',recdate=mydate)
				remm=[]
				all_data=[]

				for k in transaction_source:
					pl=k.merchant.id
					all_data.append(pl)

				msg=list(dict.fromkeys(all_data)) # remove duplicates from list

				for mm in msg:
					merchant = tblIaMERCHANT.objects.get(branch=mybranch,id=mm)
					transs = tblIafieldagent.objects.filter(branch=mybranch,
						status='Approved',merchant=mm, wallet_type='Main',recdate=mydate)
					total =transs.aggregate(Sum('amount'))
					total=int(total['amount__sum'])
					mit = {'merchant':merchant,'trans':transs,'total':total}
					remm.append(mit)


				return render(request,'Ia/appreport.html',{'company':mybranch, 'user':varuser,
						'thriftrec':remm,'date':mydate,'currency':currency, 'status':status})

			if status =='End Of Day':

				transaction_source = tblIafieldagent.objects.filter(branch=mybranch,
					status='Approved',wallet_type='Main',recdate=mydate)
				remm=[]
				all_data=[]
				tot=0

				for k in transaction_source:
					pl=k.merchant.id
					all_data.append(pl)

				msg=list(dict.fromkeys(all_data)) # remove duplicates from list

				for mm in msg:
					merchant = tblIaMERCHANT.objects.get(branch=mybranch,id=mm)
					transs = tblIafieldagent.objects.filter(branch=mybranch,
						status='Approved',merchant=mm, wallet_type='Main',recdate=mydate)
					total =transs.aggregate(Sum('amount'))
					total=total['amount__sum']
					tot = tot + total
					mit = {'merchant':merchant,'total':total, 'status':'Approved'}
					remm.append(mit)


				return render(request,'Ia/appreport_all.html',{'company':mybranch, 'user':varuser,
						'thriftrec':remm,'date':mydate,'status':status,'tot':tot})




			all_data=[]
			return render(request,'Ia/monthrep.html',{'company':mybranch, 'user':varuser,
					'thriftrec':all_data,'status':status,'month':realmonth,'year':yday})


		else:
			form=viewallapprovedform()
		return render(request,'Ia/approvalsreport.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')


def payout(request):
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

		if staff.admin==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant=form.cleaned_data['merchant']

				datte=form.cleaned_data['date'] #JS date Object
				dday,mday,yday = datte.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				month=calendar.month_name[mday] #month_index to month_name

				mydate=date(yday,mday,dday)

				try:
					memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1,branch=mybranch)
				except:
					return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
				ddt=[]
				frf=[]
				allunpaid= tblpayoutrequest.objects.filter(
					merchant=memmerchant,
					branch=mybranch,
					request_date =mydate,
					wallet_type='Main',
					status='Unpaid')

				mycost=[]
				myc=[int(q.customer.id) for q in allunpaid]
				[mycost.append(x) for x in myc if x not in mycost] #removes duplicates in lost

				for kid in mycost:
					customer=tblCUSTOMER.objects.get(id = kid,status=1)

					rtpp = tblpayoutrequest.objects.filter(
						customer=customer,
						request_date=mydate,
						status='Unpaid',
						wallet_type='Main')

					custo=rtpp.aggregate(Sum('amount'))
					custo = custo['amount__sum']

					fd ={'sum':custo,'customer':customer}
					frf.append(fd)

				add = allunpaid.aggregate(Sum('amount'))
				add = add['amount__sum']
				dl={'total':add}
				ddt.append(dl)

				return render(request,'Ia/adminpayout.html',
					{'total':ddt,
					'company':mybranch,
					'merchant':memmerchant,
					'user':varuser,
					'mydate':mydate,
					'date':datte,
					'thriftrec':frf})
			else:
				msg ='Fill up all boxes'

		else:
			form=viewmerchantform()
			msg=''
		return render(request,'Ia/payout.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def withdrawoptions(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,trandate=acccode.split(':')
			customer=tblCUSTOMER.objects.get(id=state)

			return render(request,'Ia/adminwithdrawfund.html',{
				'date1':trandate,
				'customer':state,'hhh':customer})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



def withdrawfunds(request):
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

		if staff.admin==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer_id=request.POST['customer']

			datte=request.POST['date1'] #JS date Object
			yday,mday,dday = datte.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #only useful fo me to know request date

			customer=tblCUSTOMER.objects.get(id=customer_id)
			merchant=customer.merchant.id
			merchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant)


			allreq = tblpayoutrequest.objects.filter(
				status='Unpaid',
				branch=mybranch,
				request_date=mydate,
				customer = customer)

			mycount=allreq.count()

			add=allreq.aggregate(Sum('amount'))
			payable_sum = add['amount__sum']

			account_type_list=[]
			myc=[(unicode(q.account_type),q.recdate) for q in allreq]
			[account_type_list.append(x) for x in myc if x not in account_type_list] #removes duplicates in lost
			yyu= len(account_type_list) #listcount
			t_date= date.today()

			if yyu > 0 :

				for account_type in account_type_list :

					month = unicode(account_type[1]).split('-')[-2] #month_index
					year = unicode(account_type[1]).split('-')[0]

					request_item = tblpayoutrequest.objects.filter(
						status='Unpaid',
						branch=mybranch,
						purpose = card[0],
						customer = customer,
						wallet_type='Main',
						recdate=account_type[1]).delete()

					transactions = tblIathrift_trans.objects.filter(
						branch=mybranch,
						purpose = card[0],
						customer=customer,
						wallet_type='Main',
						avalability='Not Available',
						reason='requested',
						recdate=account_type[1],
						merchant=merchant).delete()


					bankk = tblIamerchantBank.objects.filter(
						status= 'Approved',
						branch=mybranch,
						account_type=	account_type[0],
						wallet_type='Main',
						merchant=merchant,
						recdate=account_type[1],
						customer=customer).delete()

				thrift = tblIathrift.objects.get(
					purpose = card[0],
					branch = mybranch,
					customer=customer,
					number=month,
					year=year)

				thrift_mi=int(thrift.thrift)

				transactions = tblIathrift_trans.objects.get(
					purpose = card[0],
					wallet_type='Main',
					branch=mybranch,
					recdate__month=month,
					avalability='Not Available',
					reason='Account Maintenance',
					customer=customer,
					merchant=merchant).delete()

				thrift.delete()

				try :
					tblpayoutrecord.objects.get(
						status='Paid',
						branch=mybranch,
						customer=customer,
						account_type=account_type[0],
						paid_by=varuser,
						wallet_type='Main',
						amount=payable_sum,
						recdate= mydate,
						merchant=merchant,
						thrift=thrift_mi)
				except :
					tblpayoutrecord(
						status='Paid',
						branch=mybranch,
						customer=customer,

						account_type=account_type[0],
						paid_by=varuser,
						wallet_type='Main',
						amount=payable_sum,
						paid_date=t_date,
						recdate=mydate,
						merchant=merchant,
						thrift=thrift_mi).save()


				customer=customer.surname +" " + customer.firstname + " " + customer.othername
				return render(request,'Ia/reqestwithdrawsuccess.html',{
						'company':mybranch,
						'user':varuser,
						'amount':payable_sum,
						'customer':customer})
			else :
				msg = N,payable_sum, 'cash withdrawn'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/thrift/thrift/payouts/')
	else:
		return HttpResponseRedirect('/login/user/')







@csrf_exempt
def gen_save_details(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate=acccode.split(':')
			mm = tblIaMERCHANT.objects.get(id=state)


			product='Savings'

			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wrd_date=date(y,m,d)

			dpp = calendar.day_name[calendar.weekday(y,m,d)]


			return render(request,'Ia/salesdet_gensave.html',{'date1':wrd_date,# recdate,
			'dow':dpp,'product':product, 'trans_id':state,'hhh':mm})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def gen_save_details_2(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate,status=acccode.split(':')
			mm = tblIaMERCHANT.objects.get(id=state)

			branch=mm.branch.id
			mybranch=tblBRANCH.objects.get(id=branch)
			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wrd_date=date(y,m,d)

			if status == '':
				msg = 'Select appropriate status'
				return render(request,'Ia/selectloan.html',{'msg':msg})
			if status == 'Unapproved':
				customer=tblIbbfieldagent.objects.filter(branch=mybranch,is_declined=0, merchant=state, status='Unapproved',recdate=wrd_date)
			elif status =='Declined':
				customer=tblIbbfieldagent.objects.filter(branch=mybranch,is_declined=1, merchant=state, status='Declined',recdate=wrd_date)

			if customer.count() ==0:
				msg= 'NO RECORDS FOUND'
				return render(request,'Ia/selectloan.html',{'msg':msg})
			else:

				add=customer.aggregate(Sum('amount'))
				payable_sum = int(add['amount__sum'])


			return render(request,'Ia/salesdet_gensave2.html',{'company':mybranch,'date1':recdate,
				'date2':wrd_date, 'trans_id':state,'hhh':mm,'customer':customer,'sales':payable_sum})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def savecanopt(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate=acccode.split(':')

			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wd_date=date(y,m,d)
			customer=tblIbbfieldagent.objects.get(id = state, status='Unapproved',recdate=wd_date)

			return render(request,'Ia/gensavedelopt.html',{'date1':recdate,
				'date2':wd_date, 'trans_id':state,'hhh':customer})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



def cancelgensaveyes(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']


		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)


		dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]
		product='Savings'


		remit = tblIbbfieldagent.objects.filter( id =trans_id,
			branch=mybranch,
			wallet_type='Main',
			recdate = transdate,
			status='Unapproved').update(is_declined=1,status='Declined')


		remit = tblIbbfieldagent.objects.filter(branch=mybranch,
			recdate = transdate,
			is_declined=0,
			wallet_type='Main',
			status='Unapproved')


		sdic= {}
		kk=[]


		for j in remit:
			j = j.merchant.id  #uses ID from tblSTAFF
			s = {j:j}
			sdic.update(s)
		klist = sdic.values()
		for p in klist:
			kk.append(p)



		count=remit.count()

		if count>0:
			kpp=[]
			for k in kk:
				merchant= tblIaMERCHANT.objects.get(id=k)

				merch= remit.filter(merchant=merchant)

				merch = remit.filter(merchant=k)

				m1=merch.aggregate(Sum('amount'))
				m2 = m1['amount__sum']
				add3 = int(m2)

				s={'merchant':merchant,'sales':add3,'id':k}
				kpp.append(s)


			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render(request,'Ia/reconciliaton_savings.html',{'company':mybranch,
				'user':varuser,
				'thriftrec':kpp,
				'dates':transdate,
				'dow':dpp,
				'product':product,
				'cdate':mydate,
				'total':add})
		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')


def cancelgensaveyno(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']


		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)

		# transdate=date(yday,mday,dday)
		# dow = calendar.month_name[mday]
		dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]
		product='Savings'



		remit = tblIbbfieldagent.objects.filter(branch=mybranch,
			recdate = transdate,
			is_declined=0,
			wallet_type='Main',
			status='Unapproved')


		sdic= {}
		kk=[]


		for j in remit:
			j = j.merchant.id  #uses ID from tblSTAFF
			s = {j:j}
			sdic.update(s)
		klist = sdic.values()
		for p in klist:
			kk.append(p)



		count=remit.count()

		if count>0:
			kpp=[]
			for k in kk:
				merchant= tblIaMERCHANT.objects.get(id=k)

				merch= remit.filter(merchant=merchant)

				merch = remit.filter(merchant=k)

				m1=merch.aggregate(Sum('amount'))
				m2 = m1['amount__sum']
				add3 = int(m2)

				s={'merchant':merchant,'sales':add3,'id':k}
				kpp.append(s)


			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render(request,'Ia/reconciliaton1.html',{'company':mybranch,
				'user':varuser,
				'thriftrec':kpp,
				'dates':transdate,
				'dow':dpp,
				'product':product,
				'cdate':mydate,
				'currency':currency,
				'total':add})
		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')

@csrf_exempt
def reclinesave(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			state,recdate=acccode.split(':')

			d,m,y=recdate.split('/')
			y=int(y)
			m=int(m)
			d=int(d)

			wd_date=date(y,m,d)
			customer=tblIbbfieldagent.objects.get(id = state,is_declined=1,
				status='Declined',
				recdate=wd_date)

			return render(request,'Ia/reclin2.html',{'date1':recdate,
				'date2':wd_date, 'trans_id':state,'hhh':customer})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')





def reclgensaveppro(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']


		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)


		dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]
		product='Savings'


		remit = tblIbbfieldagent.objects.filter( id =trans_id,
			branch=mybranch,
			wallet_type='Main',
			recdate = transdate).update(is_declined=0,status='Unapproved')


		remit = tblIbbfieldagent.objects.filter(branch=mybranch,
			recdate = transdate,
			is_declined=0,
			wallet_type='Main',
			status='Unapproved')


		sdic= {}
		kk=[]


		for j in remit:
			j = j.merchant.id  #uses ID from tblSTAFF
			s = {j:j}
			sdic.update(s)
		klist = sdic.values()
		for p in klist:
			kk.append(p)



		count=remit.count()

		if count>0:
			kpp=[]
			for k in kk:
				merchant= tblIaMERCHANT.objects.get(id=k)

				merch= remit.filter(merchant=merchant)

				merch = remit.filter(merchant=k)

				m1=merch.aggregate(Sum('amount'))
				m2 = m1['amount__sum']
				add3 = int(m2)

				s={'merchant':merchant,'sales':add3,'id':k}
				kpp.append(s)


			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render(request,'Ia/reconciliaton_savings.html',{'company':mybranch,
				'user':varuser,
				'thriftrec':kpp,
				'dates':transdate,
				'dow':dpp,
				'product':product,
				'cdate':mydate,
				'total':add})
		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')



def cancelrec(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		currency=mybranch.currency_code

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		mydate=request.POST['date1']
		trans_id = request.POST['trans_id']


		dday,mday,yday=mydate.split('/')
		yday=int(yday)
		mday=int(mday)
		dday=int(dday)

		transdate=date(yday,mday,dday)

		# transdate=date(yday,mday,dday)
		# dow = calendar.month_name[mday]
		dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]
		product='Savings'



		remit = tblIbbfieldagent.objects.filter(branch=mybranch,
			recdate = transdate,
			is_declined=0,
			wallet_type='Main',
			status='Unapproved')


		sdic= {}
		kk=[]


		for j in remit:
			j = j.merchant.id  #uses ID from tblSTAFF
			s = {j:j}
			sdic.update(s)
		klist = sdic.values()
		for p in klist:
			kk.append(p)



		count=remit.count()

		if count>0:
			kpp=[]
			for k in kk:
				merchant= tblIaMERCHANT.objects.get(id=k)

				merch= remit.filter(merchant=merchant)

				merch = remit.filter(merchant=k)

				m1=merch.aggregate(Sum('amount'))
				m2 = m1['amount__sum']
				add3 = int(m2)

				s={'merchant':merchant,'sales':add3,'id':k}
				kpp.append(s)


			add=remit.aggregate(Sum('amount'))
			add = add['amount__sum']
			add = int(add)

			return render(request,'Ia/reconciliaton_savings.html',{'company':mybranch,
				'user':varuser,
				'thriftrec':kpp,
				'dates':transdate,
				'dow':dpp,
				'product':product,
				'cdate':mydate,
				'total':add})
		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def apreedit(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			merchant,user,trandate=acccode.split(':')

			dday,mday,yday = trandate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			transdate=date(yday,mday,dday)
			product='Savings'


			dpp = calendar.day_name[calendar.weekday(yday,mday,dday)]



			chkstaff = tblSTAFF.objects.get(email=user,status=1)
			bra = chkstaff.branch.id
			mybranch= tblBRANCH.objects.get(id = bra)

			currency= mybranch.currency_code

			ddt=[]

			if merchant=='undefined':
				heading = 'Bulk Approval for all unapproved cash'

				thriftrec = tblIbbfieldagent.objects.filter(branch=bra,
					recdate = transdate,
					is_declined = 0,
					wallet_type='Main',
					status='Unapproved')

			else:
				co=tblIaMERCHANT.objects.get(id=merchant)
				heading=co.staff.surname + " " + co.staff.firstname + " " + co.staff.othername + "'s" + " "+ "unapproved cash"

				thriftrec = tblIbbfieldagent.objects.filter(branch=bra,
					merchant=co,
					recdate = transdate,
					is_declined = 0,
					wallet_type='Main',
					status='Unapproved')


			mycount= thriftrec.count()
			# return render(request,'Ia/selectloan.html',{'msg':mycount})

			if mycount >0:
				add=thriftrec.aggregate(Sum('amount'))
				add = int(add['amount__sum'])
				dl={'amount':add}
				ddt.append(dl)


				return render(request,'Ia/ppp_all_gen.html',{
					'company':mybranch,
					'dates':trandate,
					'thriftrec':ddt,
					'dow':dpp,

					'heading':heading,
					'merchant':merchant,

					'product':product,
					'tot':add,
					'date':transdate,
					'ttt':thriftrec})

			else:
				return HttpResponseRedirect('/fts/thrift/approvals/')


		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




def bulkreconhh(request):
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
		currency=mybranch.currency_code
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			amount1 =request.POST['amount'] #carry come
			mydate2=request.POST['dates'] #Javascript date object
			mydate22 = request.POST['date']
			cash =request.POST['cash'] #posted

			amount1=int(amount1)
			cash=int(cash)


			dday,mday,yday = mydate2.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			recdate=date(yday,mday,dday) #python date object

			dddy = datetime.today()
			transdate = dddy.date()
			ttime = dddy.time()


			ttt = tblIbbfieldagent.objects.filter(branch=mybranch,
				recdate = recdate,
				is_declined = 0,
				wallet_type='Main',
				status='Unapproved')

			mdm =[]
			dsr = []
			[mdm.append(k.merchant.id) for k in ttt if k.merchant.id not in mdm]

			for gv in mdm:
				merchant=tblIaMERCHANT.objects.get(id=gv)
				tq = ttt.filter(merchant=merchant)
				tm = tq.aggregate(Sum('amount'))
				TotalSales = tm['amount__sum']

				vv = {'mer':merchant,'sales':TotalSales}
				dsr.append(vv)



			# return render(request,'Ia/selectloan.html',{'msg':dsr})


			if amount1 == cash :
				for cc in ttt :
					merchant= cc.merchant.id
					merchant= tblIaMERCHANT.objects.get(id=merchant)
					customer=cc.customer.id
					customer=tblIaCUSTOMER.objects.get(id=customer)
					trial = tblIbbsavings_trans.objects.filter(
							branch=mybranch,
							amount= cc.amount,
							merchant=merchant,
							customer=customer,
							recdate=recdate,
							description='Credit',
							wallet_type='Main',
							status='CR',
							avalability='Available',
							year=yday)

					if trial.count() == 0:

						tblIbbsavings_trans(branch=mybranch,
							amount= cc.amount,
							merchant=merchant,
							customer=customer,
							recdate=recdate,
							transdate=transdate,
							ttime= ttime,
							description='Credit',
							wallet_type='Main',
							transac_id=cc.transac_id,
							status='CR',
							avalability='Available',
							year=yday).save()


						cc.status ='Approved'
						cc.save()


				return render(request,'Ia/all_app_success2.html',{
					'company':mybranch,
					# 'fo':merchant2,
					'admin':staff,
					'dsr':dsr,
					'date':transdate,
					'time':ttime,
					'user':varuser,
					'amount':amount1})

			else:
				msg = 'amount not applicable'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')



	else:
		return HttpResponseRedirect('/login/user/')



def bulkrecon(request):
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
		currency=mybranch.currency_code
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			amount1 =request.POST['amount'] #carry come
			mydate2=request.POST['dates'] #Javascript date object
			credit_officer=request.POST['merchant']
			mydate22 = request.POST['date']
			cash =request.POST['cash'] #posted

			amount1=int(amount1)
			cash=int(cash)


			dday,mday,yday = mydate2.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object

			fdate= date.today() #record date, the date you took record
			remterr=date(fdate.year,fdate.month,fdate.day)


			if credit_officer=='undefined':

				ttt = tblIbbfieldagent.objects.filter(branch=mybranch,
					recdate = mydate,
					is_declined = 0,
					wallet_type='Main',
					status='Unapproved')

			else:
				co=tblIaMERCHANT.objects.get(id=credit_officer)

				ttt = tblIbbfieldagent.objects.filter(branch=mybranch,
						merchant=co,
						recdate = mydate,
						is_declined = 0,
						wallet_type='Main',
						status='Unapproved')



			mdm =[]
			dsr = []
			[mdm.append(k.merchant.id) for k in ttt if k.merchant.id not in mdm] #remove repeatiton

			for gv in mdm:
				merchant=tblIaMERCHANT.objects.get(id=gv)
				tq = ttt.filter(merchant=merchant)
				tm = tq.aggregate(Sum('amount'))
				TotalSales = int(tm['amount__sum'])

				vv = {'mer':merchant,'sales':TotalSales}
				dsr.append(vv)



			if amount1 == cash :
				dddy = datetime.today()
				ddd = dddy.date()
				tti=dddy.time()

				for ttt in ttt :
					customer_id = ttt.customer.customer.id
					amount=int(ttt.amount)
					customer=tblCUSTOMER.objects.get(branch=mybranch, id=customer_id)
					customer=tblIaCUSTOMER.objects.get(customer=customer)
					wallet=customer.customer.wallet
					customer_code=customer.code




					transaction_code= ttt.transac_id



					mer= ttt.merchant.id


					merchant2 =tblIaMERCHANT.objects.get(id=mer)




					ty = gen_reconciliation(branch,wallet,amount,varuser,transaction_code)


				return render(request,'Ia/all_app_success2.html',{
					'company':mybranch,
					'fo':merchant2,
					'admin':staff,
					'dsr':dsr,
					'date':ddd,
					'time':tti,
					'currency':currency,
					'user':varuser,
					'amount':amount1})


			else:
				msg = 'amount not applicable'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return HttpResponseRedirect('/fts/thrift/approvals/')



	else:
		return HttpResponseRedirect('/login/user/')










def cancelreq(request):
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

		if staff.admin==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer_id=request.POST['customer']
			# account_type=request.POST['account_type']

			datte=request.POST['date1'] #JS date Object
			yday,mday,dday = datte.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			month=calendar.month_name[mday]



			customer=tblCUSTOMER.objects.get(id=customer_id)
			merchant=customer.merchant.id
			merchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant)

			allreq = tblpayoutrequest.objects.filter(
				status='Unpaid',
				branch=mybranch,
				request_date=mydate,
				customer = customer)

			add=allreq.aggregate(Sum('amount'))
			payable_sum = add['amount__sum']


			account_type_list=[]
			myc=[(unicode(q.account_type),q.recdate) for q in allreq]
			[account_type_list.append(x) for x in myc if x not in account_type_list] #removes duplicates in lost
			yyu= len(account_type_list) #listcount


			if yyu > 0 :

				for account_type in account_type_list :

					month = unicode(account_type[1]).split('-')[-2] #month_index
					year = unicode(account_type[1]).split('-')[0]

					request_item = tblpayoutrequest.objects.filter(
						status='Unpaid',
						branch=mybranch,
						purpose = card[0],
						customer = customer,
						wallet_type='Main',
						recdate=account_type[1]).delete()

					transactions = tblIathrift_trans.objects.get(
						branch=mybranch,
						purpose = card[0],
						customer=customer,
						wallet_type='Main',
						avalability='Not Available',
						reason='requested',
						recdate=account_type[1],
						merchant=merchant)

					transactions.avalability='Available'
					transactions.reason='Available'
					transactions.save()


				customer=customer.surname +" " + customer.firstname + " " + customer.othername
				return render(request,'Ia/reqestcancel.html',{
						'company':mybranch,
						'user':varuser,
						'amount':payable_sum,
						'customer':customer})
			else:
				return HttpResponseRedirect('/thrift/thrift/payouts/')

	else:
		return HttpResponseRedirect('/login/user/')





def adminpayfund(request):
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

		if staff.admin==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			merchant= request.POST['merchant']
			datte=request.POST['date'] #date the request was made

			merchant=tblIaMERCHANT.objects.get(thrift1a =1,id=merchant,status=1)

			yday,mday,dday = datte.split('/')

			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			mydate=date(yday,mday,dday)

			month=calendar.month_name[mday]

			ddt=[]

			allunpaid= tblpayoutrequest.objects.filter(merchant=merchant,branch=mybranch,recdate=mydate,
				month=month,status='Unpaid') #request by all customers thru the merchant

			mycost=[]
			myc=[int(q.customer.id) for q in allunpaid]
			[mycost.append(x) for x in myc if x not in mycost] #Unique list of customers who request cash

			mycount= len(mycost) #listcount


			transactions = tblIathrift_trans.objects.filter(
				account_type = 'Main account',
				wallet_type='Main',
				merchant=memmerchant,
				branch=mybranch,
				reason='requested',
				avalability='Available',
				recdate__month=mday)

			code=[]
			for k in allunpaid: #Allunpaid = gross number of requests
				customer=k.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)

				try:
					tblpayoutrecord.objects.get(branch=mybranch,merchant=merchant,customer=customer,recdate=mydate,
						amount=k.amount,status='Paid')
				except:
					tblpayoutrecord(branch=mybranch,merchant=merchant,customer=customer,amount=k.amount,status='Paid',
						recdate=mydate).save()
					code.append(int(k.code))

					k.delete()


			for j in transactions:
				dc=j.code
				customer=j.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)

				for k in code:
					trans_code = int(k.code)
					code.append(trans_code)
					if dc==k:
						k.reason='Withdrawn'
						k.save()
						j.delete()

			return render(request,'Ia/adminpayoutsuccess.html',{'count':mycount,'company':mybranch,'merchant':merchant,'user':varuser})

		else:
			form=viewmerchantform()
		return render(request,'Ia/payout.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def payoutreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.thrift_officer==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			# return render(request,'Ia/404.html')

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if request.method == 'POST':
			form = payoutform(request.POST)
			if form.is_valid():
				status=form.cleaned_data['status']
				date1=form.cleaned_data['date']
				yday,mday,dday = date1.split('/')

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday)
				month = calendar.month_name[mday]

				allmerchant = tblIaMERCHANT.objects.filter(branch=mybranch,status=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1

				if checkbox==1:
					if status == 'Paid':
						for k in allmerchant:
							thriftrec= tblpayoutrecord.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Pending':
						for p in allmerchant:
							thriftrec= tblpayoutrequest.objects.filter(month=month,status='Unpaid', branch=mybranch,recdate=mydate,merchant=p)
							add =0

							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)

					return render(request,'Ia/payoutdayreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'fund':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:
								thriftrec= tblIamerchantBank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':mn,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'Unremmitted':
							for kl in allmerchant:
								thriftrec= tblIasavings_trans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)


		else:
			form=payoutform()
		return render(request,'Ia/payoutreport.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')




#######******** CEO SAVINGS REPORTS*********************
def repome(request):
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
		return render(request,'Ia/reporthome.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')


def cashierreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')
		if staff.ceo == 0:
			msg = 'error'
			return render(request,'Ia/selectloan.html',{'msg':msg})
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

		if request.method=='POST':
			form= endofdayform(request.POST)

			if form.is_valid():


				td=form.cleaned_data['to_date']
				fd =form.cleaned_data['date']
				status=request.POST['status']
				product=request.POST['myproducts']


				businessyear=request.POST['myyear']

				d,m,y = fd.split('/') #JSON FROM Dates Object

				d2,m2,y2 = td.split('/') #JSON TO Dates Object

				if y== y2: #same year quarry

					fyday=int(y)
					fmday=int(m)
					fday=int(d)
					fd=date(fyday,fmday,fday) #python date object

					tyday=int(y2)
					tmday=int(m2)
					tday=int(d2)


					td=date(tyday,tmday,tday) #python date object

					week_start = calendar.day_name[calendar.weekday(fyday,fmday,fday)]
					week_stop = calendar.day_name[calendar.weekday(tyday,tmday,tday)]

					if fmday < tmday: #normal senario
						test_months = range(fmday,tmday+1)
						start_date = fday

						# end_date = tday

					if fmday == tmday: #normal scenario
						test_months = range(fmday,tmday+1)
						if fday < tday: #normal range
							start_date=fday #to day
							end_date=tday #from day


						elif fday > tday:
							start_date=tday
							end_date=fday


						elif fday == tday:
							start_date = end_date = fday


					elif fmday > tmday: #abnornaml case
						test_months = range(tmday,fmday+1)



						td=date(fyday,fmday,fday)
						fd=date(tyday,tmday,tday)

						# msg = f"{fd}, {td}"
					# return render(request,'Ia/selectloan.html',{'msg':test_months})

					week_start = calendar.day_name[calendar.weekday(fyday,tmday,tday)]
					week_stop = calendar.day_name[calendar.weekday(tyday,fmday,fday)]


					detli=[]
					toot_cr=0
					toot_dr = 0
					toot=0




					if status == 'Deposit':
						description='Credit'
						mm=0
					elif status=='Withdrawal':
						description='Debit'
						mm=0
					else:
						status= 'End Of Day'
						mm=1

					bb = tblproductsname.objects.get(branch=mybranch,your_product_name=product)

					totalmerchant=tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1, status=1)

					if bb.product.product == 'Esusu':
						allmerchant=totalmerchant.filter(esusu1a=1)
						product = 'ESUSU'

						for memmerchant in allmerchant:
							merchant_sales=0
							for k in test_months: # test_months is the months covered in the search
								monthname=calendar.month_name[int(k)]

								total_salees = tblIamerchantBank.objects.filter(
													branch=mybranch,
													product='Savings',
													year= y2,
													merchant=memmerchant,
													wallet_type='Main',
													transdate__month=k)


								if k == test_months[0]: #if month is the first month
									if k == test_months[-1]: # if k is last month
										fff=0
										fff= fff + start_date
										while fff <= end_date:
											fd1 =date(tyday,k,fff)
											if mm==0:
												salees = total_salees.filter(transdate=fd1,description=description)

												couunt = salees.count()
												if couunt > 0:
													add=salees.aggregate(Sum('amount'))
													add_cr = add['amount__sum']
													merchant_sales=int(add_cr)
													toot = toot + add_cr
													df = {'sum':merchant_sales,'details':memmerchant,'status':status}
													detli.append(df)

												# return render(request,'Ia/selectloan.html',{'msg':fff})
											elif mm==1: #end of day
												salees = total_salees.filter(transdate=fd1)

												couunt = salees.count()

												if couunt> 0:
													salees_cr = salees.filter(description='Credit')

													if salees_cr.count()>0:
														add_cr=salees_cr.aggregate(Sum('amount'))
														add_cr = add_cr['amount__sum']
														merchant_sales_cr=int(add_cr)
													else:
														merchant_sales_cr=0

													toot_cr = toot_cr + merchant_sales_cr




													salees_dr = salees.filter(description='Debit')
													salees_dr_count = salees_dr.count()

													if salees_dr_count > 0:
														add_dr=salees_dr.aggregate(Sum('amount'))
														add_dr = add_dr['amount__sum']
														merchant_sales_dr=int(add_dr)
													else:
														merchant_sales_dr=0

													toot_dr = toot_dr + merchant_sales_dr
													df = {'month':monthname,'details':memmerchant,'credit':merchant_sales_cr,'debit':merchant_sales_dr}
													detli.append(df)

											fff += 1
										# return render(request,'Ia/selectloan.html',{'msg':fd1})

									else: #boundaries = from_date to month end
										fff=0
										fff= fff + start_date
										end_date = (monthrange(fd.year, k))[-1]
										while fff <= end_date :
											fd1=date(fyday,k,fff)
											if mm==0:
												salees = total_salees.filter(transdate=fd1,description=description)
												couunt = salees.count()
												if couunt> 0:
													add=salees.aggregate(Sum('amount'))
													add_cr = add['amount__sum']
													merchant_sales=int(add_cr)
													toot = toot + add_cr
													df = {'sum':merchant_sales,'details':memmerchant,'status':status}
													detli.append(df)

											elif mm==1: #end of day

												salees = total_salees.filter(transdate=fd1)

												couunt = salees.count()

												if couunt> 0:
													salees_cr = salees.filter(description='Credit')

													if salees_cr.count() >0:
														add_cr=salees_cr.aggregate(Sum('amount'))
														add_cr = add_cr['amount__sum']

														merchant_sales_cr=int(add_cr)
													else:
														merchant_sales_cr=0

													toot_cr = toot_cr + merchant_sales_cr



													salees_dr = salees.filter(description='Debit')

													if salees_dr.count() > 0:
														add_dr=salees_dr.aggregate(Sum('amount'))
														add_dr = add_dr['amount__sum']

														merchant_sales_dr=int(add_dr)
													else:
														merchant_sales_dr = 0
													toot_dr = toot_dr + merchant_sales_dr

													df = {'month':monthname,'details':memmerchant,'credit':merchant_sales_cr,'debit':merchant_sales_dr}
													detli.append(df)

											fff += 1
								else:
									if k == test_months[-1]: #boundaries = 1st to to_date
										fff= 0
										start_date = 1
										fff= fff + start_date
										end_date =  td.day
										while fff <= end_date :
											fd1=date(fyday,k,fff)
											if mm==0:

												salees = total_salees.filter(transdate=fd1,description=description)


												couunt = salees.count()
												if couunt> 0:
													add=salees.aggregate(Sum('amount'))
													add_cr = add['amount__sum']
													merchant_sales=int(add_cr)
													toot = toot + add_cr
													df = {'sum':merchant_sales,'details':memmerchant,'status':status}
													detli.append(df)
											elif mm==1: #end of day
												salees = total_salees.filter(transdate=fd1)

												couunt = salees.count()

												if couunt> 0:
													salees_cr = salees.filter(description='Credit')
													if salees_cr.count()>0:

														add_cr=salees_cr.aggregate(Sum('amount'))
														add_cr = add_cr['amount__sum']

														merchant_sales_cr=int(add_cr)
													else:
														merchant_sales_cr=0

													toot_cr = toot_cr + merchant_sales_cr



													salees_dr = salees.filter(description='Debit')

													if salees_dr.count() > 0:

														add_dr=salees_dr.aggregate(Sum('amount'))
														add_dr = add_dr['amount__sum']

														merchant_sales_dr=int(add_dr)
													else:
														merchant_sales_dr = 0
													toot_dr = toot_dr + merchant_sales_dr
													df = {'month':monthname,'details':memmerchant,'credit':merchant_sales_cr,'debit':merchant_sales_dr}
													detli.append(df)
											fff += 1
									else: # loop thru the whole month

										fff=0
										start_date = 1

										fff= fff + start_date

										end_date= (monthrange(td.year, k))[-1]

										while fff <= end_date :
											fd1=date(fyday,k,fff)

											if mm==0:

												salees = total_salees.filter(transdate=fd1,description=description)


												couunt = salees.count()
												if couunt> 0:
													add=salees.aggregate(Sum('amount'))
													add_cr = add['amount__sum']
													merchant_sales=int(add_cr)
													toot = toot + add_cr
													df = {'sum':merchant_sales,'details':memmerchant,'status':status}
													detli.append(df)

											elif mm==1: #end of day

												salees = total_salees.filter(transdate=fd1)

												couunt = salees.count()

												if couunt> 0:
													salees_cr = salees.filter(description='Credit')
													add_cr=salees_cr.aggregate(Sum('amount'))
													add_cr = add_cr['amount__sum']

													merchant_sales_cr=int(add_cr)

													toot_cr = toot_cr + merchant_sales_cr

													salees_dr = salees.filter(description='Debit')
													add_dr=salees_dr.aggregate(Sum('amount'))
													add_dr = add_dr['amount__sum']

													merchant_sales_dr=int(add_dr)
													toot_dr = toot_dr + merchant_sales_dr
													df = {'month':monthname,'details':memmerchant,'credit':merchant_sales_cr,'debit':merchant_sales_dr}
													detli.append(df)

											fff += 1
						if mm == 0:

							return render(request,'Ia/report_performance.html',{
									'company':mybranch,
									'user':varuser,
									'form':form,
									'toot':int(toot),
									'to':td,
									'product':product,
									'week_stop':week_stop,
									'week_start':week_start,
									'status':status,
									'from' :fd,
									'detli':detli})
						elif mm ==1:

							return render(request,'Ia/report_performance2.html',{
									'company':mybranch,
									'user':varuser,
									'to':td,
									'product':product,
									'week_stop':week_stop,
									'week_start':week_start,
									'status':status,
									'total_credit':toot_cr,
									'total_debit':toot_dr,
									'from' :fd,
									'detli':detli})
					elif bb.product.product == 'Savings':
						allmerchant=totalmerchant.filter(savings1a=1)
						product = 'SAVINGS'
						for memmerchant in allmerchant:
							merchant_sales=0
							for k in test_months: # test_months is the months covered in the search
								monthname=calendar.month_name[int(k)]
								total_salees = tblIbbsavings_trans.objects.filter(
													branch=mybranch,
													year=y2,
													merchant=memmerchant,
													wallet_type='Main',
													transdate__month=k)
								if k == test_months[0]: #if month is the first month
									if k == test_months[-1]: # if k is last month
										fff=0
										fff= fff + start_date
										while fff <= end_date :
											fd1=date(fyday,k,fff)

											if mm==0:

												salees = total_salees.filter(transdate=fd1,description=description)

												couunt = salees.count()

												if couunt> 0:
													add=salees.aggregate(Sum('amount'))
													add_cr = add['amount__sum']
													merchant_sales=int(add_cr)
													toot = toot + add_cr
													df = {'sum':merchant_sales,'details':memmerchant,'status':status}
													detli.append(df)

											elif mm==1: #end of day
												salees = total_salees.filter(transdate=fd1)

												couunt = salees.count()

												if couunt> 0:
													salees_cr = salees.filter(description='Credit')

													if salees_cr.count()>0:
														add_cr=salees_cr.aggregate(Sum('amount'))
														add_cr = add_cr['amount__sum']
														merchant_sales_cr=int(add_cr)
													else:
														merchant_sales_cr=0

													toot_cr = toot_cr + merchant_sales_cr


													salees_dr = salees.filter(description='Debit')
													salees_dr_count = salees_dr.count()

													if salees_dr_count > 0:
														add_dr=salees_dr.aggregate(Sum('amount'))
														add_dr = add_dr['amount__sum']
														merchant_sales_dr=int(add_dr)
													else:
														merchant_sales_dr=0

													toot_dr = toot_dr + merchant_sales_dr
													df = {'month':monthname,'details':memmerchant,'credit':merchant_sales_cr,'debit':merchant_sales_dr}
													detli.append(df)

											fff += 1
									else: #boundaries = from_date to month end
										fff=0
										fff= fff + start_date
										end_date = (monthrange(fd.year, k))[-1]
										while fff <= end_date :
											fd1=date(fyday,k,fff)


											if mm==0:
												salees = total_salees.filter(transdate=fd1,description=description)

												couunt = salees.count()

												if couunt> 0:
													add=salees.aggregate(Sum('amount'))
													add_cr = add['amount__sum']
													merchant_sales=int(add_cr)
													toot = toot + add_cr
													df = {'sum':merchant_sales,'details':memmerchant,'status':status}
													detli.append(df)

											elif mm==1: #end of day
												salees = total_salees.filter(transdate=fd1)

												couunt = salees.count()

												if couunt> 0:
													salees_cr = salees.filter(description='Credit')

													if salees_cr.count()>0:
														add_cr=salees_cr.aggregate(Sum('amount'))
														add_cr = add_cr['amount__sum']
														merchant_sales_cr=int(add_cr)
													else:
														merchant_sales_cr=0

													toot_cr = toot_cr + merchant_sales_cr


													salees_dr = salees.filter(description='Debit')
													salees_dr_count = salees_dr.count()

													if salees_dr_count > 0:
														add_dr=salees_dr.aggregate(Sum('amount'))
														add_dr = add_dr['amount__sum']
														merchant_sales_dr=int(add_dr)
													else:
														merchant_sales_dr=0

													toot_dr = toot_dr + merchant_sales_dr
													df = {'month':monthname,'details':memmerchant,'credit':merchant_sales_cr,'debit':merchant_sales_dr}
													detli.append(df)

											fff += 1
								else:
									if k == test_months[-1]: #boundaries = 1st to to_date
										fff= 0
										start_date = 1
										fff= fff + start_date
										end_date =  td.day
										while fff <= end_date :
											fd1=date(fyday,k,fff)

											if mm==0:

												salees = total_salees.filter(transdate=fd1,description=description)

												couunt = salees.count()
												if couunt> 0:
													add=salees.aggregate(Sum('amount'))
													add_cr = add['amount__sum']
													merchant_sales=int(add_cr)
													toot = toot + add_cr
													df = {'sum':merchant_sales,'details':memmerchant,'status':status}
													detli.append(df)


											elif mm==1: #end of day
												salees = total_salees.filter(transdate=fd1)

												couunt = salees.count()

												if couunt> 0:
													salees_cr = salees.filter(description='Credit')

													if salees_cr.count()>0:
														add_cr=salees_cr.aggregate(Sum('amount'))
														add_cr = add_cr['amount__sum']
														merchant_sales_cr=int(add_cr)
													else:
														merchant_sales_cr=0

													toot_cr = toot_cr + merchant_sales_cr


													salees_dr = salees.filter(description='Debit')
													salees_dr_count = salees_dr.count()

													if salees_dr_count > 0:
														add_dr=salees_dr.aggregate(Sum('amount'))
														add_dr = add_dr['amount__sum']
														merchant_sales_dr=int(add_dr)
													else:
														merchant_sales_dr=0

													toot_dr = toot_dr + merchant_sales_dr
													df = {'month':monthname,'details':memmerchant,'credit':merchant_sales_cr,'debit':merchant_sales_dr}
													detli.append(df)

											fff += 1

									else: # loop thru the whole month
										fff=0
										start_date = 1
										fff= fff + start_date
										end_date= (monthrange(td.year, k))[-1]
										while fff <= end_date :
											fd1=date(fyday,k,fff)

											if mm==0:

												salees = total_salees.filter(transdate=fd1,description=description)

												couunt = salees.count()
												if couunt> 0:
													add=salees.aggregate(Sum('amount'))
													add_cr = add['amount__sum']
													merchant_sales=int(add_cr)
													toot = toot + add_cr
													df = {'sum':merchant_sales,'details':memmerchant,'status':status}
													detli.append(df)

											elif mm==1: #end of day
												salees = total_salees.filter(transdate=fd1)

												couunt = salees.count()

												if couunt> 0:
													salees_cr = salees.filter(description='Credit')

													if salees_cr.count()>0:
														add_cr=salees_cr.aggregate(Sum('amount'))
														add_cr = add_cr['amount__sum']
														merchant_sales_cr=int(add_cr)
													else:
														merchant_sales_cr=0

													toot_cr = toot_cr + merchant_sales_cr


													salees_dr = salees.filter(description='Debit')
													salees_dr_count = salees_dr.count()

													if salees_dr_count > 0:
														add_dr=salees_dr.aggregate(Sum('amount'))
														add_dr = add_dr['amount__sum']
														merchant_sales_dr=int(add_dr)
													else:
														merchant_sales_dr=0

													toot_dr = toot_dr + merchant_sales_dr
													df = {'month':monthname,'details':memmerchant,'credit':merchant_sales_cr,'debit':merchant_sales_dr}
													detli.append(df)

											fff += 1

						if mm == 0:

							return render(request,'Ia/report_performance.html',{
									'company':mybranch,
									'user':varuser,
									'form':form,
									'product':product,
									'toot':int(toot),
									'to':td,
									'week_stop':week_stop,
									'week_start':week_start,
									'status':status,
									'from' :fd,
									'detli':detli})

						elif mm ==1:

							return render(request,'Ia/report_performance2.html',{
									'company':mybranch,
									'user':varuser,
									'to':td,
									'product':product,
									'week_stop':week_stop,
									'week_start':week_start,
									'status':status,
									'total_credit':toot_cr,
									'total_debit':toot_dr,
									'from' :fd,
									'detli':detli})


					else:
						return HttpResponseRedirect('/fts/thrift/reports/sales/cashier/')

				else:
					msg = 'Limit your search to same year'
					return render(request,'Ia/selectloan.html',{'msg':msg})

			else:
				return HttpResponseRedirect('/fts/thrift/reports/sales/cashier/')
		else:


			myy = []



			gb = tblproductsname.objects.filter(branch=mybranch)


			if realdet.esusu1a is True:
				hh= tblmyproducts.objects.get(product='Esusu')
				gb2=gb.get(product=hh)
				myy.append(gb2.your_product_name)



			if realdet.savings1a is True:
				hh= tblmyproducts.objects.get(product='Savings')
				gb2=gb.get(product=hh)
				myy.append(gb2.your_product_name)


			form=endofdayform()
			msg = ''
			detli=0
			toot=0
			return render(request,'Ia/report_performance_get.html',{'company':mybranch,
				'msg':msg,'user':varuser,
				'form':form,'toot':toot,
				'year':yy,
				'prod':myy,
				'detli':detli})
	else:
		return HttpResponseRedirect('/login/user/')



def merchantreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.ceo !=1:
			msg='error'
			return render(request,'Ia/selectloan.html',{'msg':msg, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		form=performanceform()


		if request.method=='POST':


			byear=request.POST['myyear']
			product=request.POST['myproducts']
			reporttype=request.POST['repottype']




			fd=date.today()

			dd = int(fd.day)
			mm = int(fd.month)
			yy = fd.year

			monthname=calendar.month_name[int(mm)]


			tr=0
			pp=0
			g=[]


			bb = tblproductsname.objects.get(branch=mybranch,your_product_name=product)

			ttt = tblIasavings_trans.objects.filter(branch=mybranch,year=byear).exclude(description='Account Maintenance')
			ttt2 = ttt.exclude(description='Interest on Loan')

			tuy = ttt2.filter(status='CR')

			tc=0
			td=0

			total_tg2=[]

			guy22=0
			guy23=0
			llk1=0
			pending=0

			if tuy.count() > 0:
				dd_cr = tuy.aggregate(Sum('amount'))
				dd_cr = int(dd_cr['amount__sum'])
			else:
				dd_cr = 0

			if bb.product.product == 'Esusu':

				pend = tblIafieldagent.objects.filter(branch=mybranch,
					status='Unapproved')

				if pend.count() > 0:
					pendl = pend.aggregate(Sum('amount'))
					pendl = int(pendl['amount__sum'])
				else:
					pendl = 0

				pending = pending + pendl


				if reporttype == 'Cash at hand':

					guy = ttt2.filter(status='DR')

					guy1 =guy.filter(description='Loan')
					for l in guy1:
						code9 = l.code
						total_tg2.append(code9)

					msg=list(dict.fromkeys(total_tg2)) #remove repeatition

					for code in msg:
						guy2 =ttt2.filter(code=code).exclude(description='Loan')

						guy2_cr = guy2.filter(status= 'CR')
						if guy2_cr.count() > 0:
							tg2 = guy2_cr.aggregate(Sum('amount'))
							tg2 = int(tg2['amount__sum'])
						else:
							tg2 = 0

						guy22 = guy22  + tg2


						guy2_dr = guy2.filter(status='DR')
						if guy2_dr.count() > 0:
							tg3 = guy2_dr.aggregate(Sum('amount'))
							tg3 = int(tg3['amount__sum'])
						else:
							tg3 = 0

						guy23 = guy23  + tg3


					if guy.count() > 0:
						dd_dr = guy.aggregate(Sum('amount'))
						dd_dr = int(dd_dr['amount__sum'])
					else:
						dd_dr = 0


					# tuy = ttt2.filter(status='CR')
					LR = tuy.filter(description= 'Loan Repayment')
					if LR.count() > 0:
						llk = LR.aggregate(Sum('amount'))
						llk = int(llk['amount__sum'])
					else:
						llk = 0

					llk1  = llk1 + llk


					dd_dr = dd_dr - guy22

					dd_cr = dd_cr - llk1


					if dd_dr <= dd_cr:
						sdd = int(dd_cr - dd_dr)
					else:
						sdd = 0

					# sdd =  dd_cr,  dd_dr,guy22#_cr.count()

					byear=int(byear)

					fd=date(byear,mm,dd)


					msg = "Total Customers' Balances  as at"
				elif reporttype == 'Cash trapped in Loans':


					guy = ttt2.filter(description='Loan')

					for l in guy:
						code9 = l.code
						total_tg2.append(code9)

					msg=list(dict.fromkeys(total_tg2))

					for code in msg:
						guy2 =ttt2.filter(code=code).exclude(description='Loan')

						guy2_cr = guy2.filter(status= 'CR')
						if guy2_cr.count() > 0:
							tg2 = guy2_cr.aggregate(Sum('amount'))
							tg2 = int(tg2['amount__sum'])
						else:
							tg2 = 0

						guy22 = guy22  + tg2



						guy2_dr = guy2.filter(status='DR')
						if guy2_dr.count() > 0:
							tg3 = guy2_dr.aggregate(Sum('amount'))
							tg3 = int(tg3['amount__sum'])
						else:
							tg3 = 0

						guy23 = guy23  + tg3





					if guy.count() > 0:
						dd_dr = guy.aggregate(Sum('amount'))
						dd_dr = int(dd_dr['amount__sum'])
					else:
						dd_dr = 0


					dd_dr = dd_dr - guy22



					sdd= dd_dr

					byear=int(byear)

					fd=date(byear,mm,dd)


					msg = 'Total Unrecovered loans as at  '


			elif bb.product.product == 'Savings':



				pend = tblIbbfieldagent.objects.filter(branch=mybranch,
					status='Unapproved')

				if pend.count() > 0:
					pendl = pend.aggregate(Sum('amount'))
					pendl = int(pendl['amount__sum'])
				else:
					pendl = 0

				pending = pending + pendl


				ttt = tblIbbsavings_trans.objects.filter(branch=mybranch,year=byear)
				ttt2 = ttt.exclude(description='Interest on Loan')


				if reporttype == 'Cash at hand':


					guy = ttt2.filter(status='DR')

					if guy.count() > 0:
						dd_dr = guy.aggregate(Sum('amount'))
						dd_dr = int(dd_dr['amount__sum'])
					else:
						dd_dr = 0


					# return render(request,'Ia/selectloan.html',{'msg':dd_dr})


					tuy = ttt2.filter(status='CR')

					LR = tuy.exclude(description= 'Loan Repayment')


					if LR.count() > 0:
						llk = LR.aggregate(Sum('amount'))
						llk = int(llk['amount__sum'])
					else:
						llk = 0


					sdd = int(llk - dd_dr)

					byear=int(byear)

					fd=date(byear,mm,dd)


					msg = "Total Customers' Balances  as at"

				elif reporttype == 'Cash trapped in Loans':
					guy = ttt2.filter(description='Loan')

					for l in guy:
						code9 = l.code
						total_tg2.append(code9)

					msg=list(dict.fromkeys(total_tg2))

					for code in msg:
						guy2 =ttt2.filter(code=code).exclude(description='Loan')

						guy2_cr = guy2.filter(status= 'CR')
						if guy2_cr.count() > 0:
							tg2 = guy2_cr.aggregate(Sum('amount'))
							tg2 = int(tg2['amount__sum'])
						else:
							tg2 = 0

						guy22 = guy22  + tg2



						guy2_dr = guy2.filter(status='DR')
						if guy2_dr.count() > 0:
							tg3 = guy2_dr.aggregate(Sum('amount'))
							tg3 = int(tg3['amount__sum'])
						else:
							tg3 = 0

						guy23 = guy23  + tg3





					if guy.count() > 0:
						dd_dr = guy.aggregate(Sum('amount'))
						dd_dr = int(dd_dr['amount__sum'])
					else:
						dd_dr = 0


					dd_dr = dd_dr - guy22



					sdd= dd_dr

					byear=int(byear)

					fd=date(byear,mm,dd)


					msg = 'Total Unrecovered loans as at  '



			return render(request,'Ia/dailyreport.html',{'branch':mybranch,'user':varuser,'msg':msg,
				'pending':pending,'total':sdd,'product':product,
				'year':fd,'monthname':monthname,
				'y2':byear })

		else:

			yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()


			realdet = tblapp.objects.get(branch=mybranch)
			myy = []
			rep=[]

			gb = tblproductsname.objects.filter(branch=mybranch)
			if staff.esusu1a is True:
				if realdet.esusu1a is True:
					hh= tblmyproducts.objects.get(product='Esusu')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)
					rep.append("Cash at hand")

			if staff.savings1a is True:
				if realdet.savings1a is True:
					hh= tblmyproducts.objects.get(product='Savings')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)
					rep.append("Cash at hand")

			if staff.loans1acash is True:
				if realdet.loans1acash is True:
					rep.append("Cash trapped in Loans")


			new_list = []

			[new_list.append(item) for item in rep if item not in new_list] #remove repeatition from list


			return render(request,'Ia/reportmerchant.html',{'company':mybranch,
				'prod':myy,'year':yy,'form':form,'rep':new_list,
				'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')





@csrf_exempt
def getmereportajaxdate(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				user = post['userid']
				user,fd,td,business_year = user.split(':')
				chkstaff = tblSTAFF.objects.get(email=user,status=1)
				bra = chkstaff.branch.id

				to = td
				frm =fd

				if fd =='':
					fd=date.today()
				if td =='':
					td=date.today()

				if fd < td:
					to = fd
					frm=td

				return render(request,'Ia/dailyreportdated.html',{
						'to':to,
						 'from' :frm,
						 'detli':selenco(bra,fd,td)})


	return HttpResponseRedirect('/login/user/')





def adminreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.ceo !=1:
			msg='error'
			return render(request,'Ia/selectloan.html',{'msg':msg, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		yy = tblbusinessyear.objects.filter(branch=mybranch).order_by('id').reverse()


		realdet = tblapp.objects.get(branch=mybranch)
		myy = []


		if request.method=='POST':
			monthname=request.POST['month']
			business_year=request.POST['myyear']


			product=request.POST['myproducts']
			reporttype =request.POST['repottype']


			bb = tblproductsname.objects.get(branch=mybranch,your_product_name=product)

			if bb.product.product == 'Esusu':
				g=[]
				tr=0
				pp = 0
				cd=0
				kk=0
				gg=0
				cr=0
				dr=0
				pending=0

				tth = tblIathrift.objects.filter(branch=mybranch,month=monthname,year=business_year)
				for k in tth:
					code = k.code
					g.append(code)

				for h in g:
					tuy = tblIasavings_trans.objects.filter(branch=mybranch,code=h)


					sav = tuy.filter(status ='CR')
					if sav.count() > 0:
						crt = sav.aggregate(Sum('amount'))
						crt = int(crt['amount__sum'])
					else:
						crt = 0

					cr = cr + crt


					tlo =tuy.filter(status='DR')
					if tlo.count() > 0:
						crd = tlo.aggregate(Sum('amount'))
						crd = int(crd['amount__sum'])
					else:
						crd = 0

					dr = dr + crd



					sav = tuy.filter(description='Account Maintenance')
					if sav.count() > 0:
						add = sav.aggregate(Sum('amount'))
						add = int(add['amount__sum'])
					else:
						add = 0

					tr = tr + add


					tlo =tuy.filter(description='Interest on Loan')
					if tlo.count() > 0:
						adl = tlo.aggregate(Sum('amount'))
						adl = int(adl['amount__sum'])
					else:
						adl = 0

					pp = pp + adl


					pend = tblIafieldagent.objects.filter(branch=mybranch,
						status='Unapproved',code=h)

					if pend.count() > 0:
						pendl = pend.aggregate(Sum('amount'))
						pendl = int(pendl['amount__sum'])
					else:
						pendl = 0

					pending = pending + pendl

				if reporttype == 'Cash at hand':

					if tr > pp:
						tr = tr
						pp=pp
					else:
						tr = 0
						pp=0

				elif reporttype == 'Cash trapped in Loans':

					if tr > pp:
						tr = 0
						pp=0
					else:
						tr = tr
						pp=pp



			elif bb.product.product == 'Savings':

				month_index = datetime.strptime(monthname,"%B") #converts month_name to month_index

				g=[]
				tr=0
				pp = 0
				cd=0
				kk=0
				gg=0
				cr=0
				dr=0
				pending=0

				tuy = tblIbbsavings_trans.objects.filter(branch=mybranch,
					transdate__month= month_index.month,
					description='Service Charge',
					year=business_year)


				if tuy.count() > 0:
					crt = tuy.aggregate(Sum('amount'))
					crt = int(crt['amount__sum'])
				else:
					crt = 0



				# return render(request,'Ia/selectloan.html',{'msg':crt})

				# cr = cr + crt


				pend = tblIbbfieldagent.objects.filter(branch=mybranch,
					status='Unapproved',recdate__month=month_index.month, year=business_year)

				if pend.count() > 0:
					pendl = pend.aggregate(Sum('amount'))
					pendl = int(pendl['amount__sum'])
				else:
					pendl = 0

				pending = pending + pendl

				if reporttype == 'Cash at hand':

					if tr > pp:
						tr = tr
						pp=pp
					else:
						tr = 0
						pp=0

					tr = crt

				elif reporttype == 'Cash trapped in Loans':

					if tr > pp:
						tr = 0
						pp=0
					else:
						tr = tr
						pp=pp


			return render(request,'Ia/mydailysales.html',{'user':varuser,
				'company':mybranch,'total':tr,'pending':pending,
				'monthname':monthname,'year':business_year,
				'tloan':pp})



		else:
			gb = tblproductsname.objects.filter(branch=mybranch)

			rep=[]

			gb = tblproductsname.objects.filter(branch=mybranch)
			if staff.esusu1a is True:
				if realdet.esusu1a is True:
					hh= tblmyproducts.objects.get(product='Esusu')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)
					rep.append("Cash at hand")

			if staff.savings1a is True:
				if realdet.savings1a is True:
					hh= tblmyproducts.objects.get(product='Savings')
					gb2=gb.get(product=hh)
					myy.append(gb2.your_product_name)
					rep.append("Cash at hand")

			# if staff.loans1acash is True:
			#     if realdet.loans1acash is True:
			#         rep.append("Cash trapped in Loans")


			new_list = []

			[new_list.append(item) for item in rep if item not in new_list] #remove repeatition from list

			tdate= date.today()

			return render(request,'Ia/reportadmin.html',{'company':mybranch,
			 'prod':myy,'year':yy,'rep':new_list,'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def getdetailprofit(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				user = post['userid']

				monthname,business_year, user= user.split(':')


				chkstaff = tblSTAFF.objects.get(email=user,status=1)
				bra = chkstaff.branch.id
				bra= tblBRANCH.objects.get(id = bra)

				g=[]
				tr=[]
				pp = 0

				tth = tblIathrift.objects.filter(branch=bra,month=monthname,year=business_year)
				for k in tth:
					code = k.code
					g.append(code)


				for h in g:
					try:
						tuy = tblIasavings_trans.objects.get(branch=bra,  description='Account Maintenance', status='CR',code=h)
						tr.append(tuy)
					except:
						pass

				return render(request,'Ia/profdet.html',{'tuy':tr,'branch':bra})


			else:
				return HttpResponseRedirect('/fts/thrift/reports/sales/admn/')
		else:
			return HttpResponseRedirect('/fts/thrift/reports/sales/admn/')
	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def getdetailloans(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				user = post['userid']

				monthname,business_year, user= user.split(':')


				chkstaff = tblSTAFF.objects.get(email=user,status=1)
				bra = chkstaff.branch.id
				bra= tblBRANCH.objects.get(id = bra)

				g=[]
				tr=[]
				pp = 0

				tth = tblIathrift.objects.filter(branch=bra,month=monthname,year=business_year)
				for k in tth:
					code = k.code
					g.append(code)


				for h in g:
					try:
						tuy = tblIasavings_trans.objects.get(branch=bra,  description='Interest on Loan', status='CR',code=h)
						tr.append(tuy)
					except:
						pass

				return render(request,'Ia/loandet.html',{'tuy':tr,'branch':bra})


			else:
				return HttpResponseRedirect('/fts/thrift/reports/sales/admn/')
		else:
			return HttpResponseRedirect('/fts/thrift/reports/sales/admn/')
	else:
		return HttpResponseRedirect('/login/user/')

##########LOAN***********************


def LOANHOME(request):
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

		if staff.admin==1:
			return render(request,'Ia/loanhome.html',{'company':mybranch, 'user':varuser})


		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def getunremcash(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				user = post['userid']

				monthname,business_year, user= user.split(':')


				chkstaff = tblSTAFF.objects.get(email=user,status=1)
				bra = chkstaff.branch.id
				bra= tblBRANCH.objects.get(id = bra)

				g=[]
				tr=[]
				pp = 0

				tth = tblIathrift.objects.filter(branch=bra,month=monthname,year=business_year)
				for k in tth:
					code = k.code
					g.append(code)

				mm = tblIaMERCHANT.objects.filter(branch=bra,status=1)
				ff=[r.id for r in mm ]


				for h in g:#the codes
					for b in ff: #the merchants
						merchant= tblIaMERCHANT.objects.get(id=b,status=1)

						try:
							kjk=tblIafieldagent.objects.filter(branch=bra,
								code =h,
								status='Received',
								wallet_type='Main',
								merchant=merchant)

							if kjk.count() > 0:

								dd =[f.recdate.day for f in kjk]


								ad1 = kjk.aggregate(Sum('amount'))
								add = ad1['amount__sum']

								j ={'merchant':merchant,'sum':add,'dates':dd}
								tr.append(j)
						except:
							pass


				return render(request,'Ia/unremdet.html',{'tuy':tr,'branch':bra,'ff':ff})


			else:
				return HttpResponseRedirect('/dashboard/')
		else:
			return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def getmerchantname(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			kk=[]
			data=tblIaMERCHANT.objects.get(thrift1a =1,id=acccode,status=1)
			data =data.staff.id
			data = tblSTAFF.objects.get(id =data)
			j = data.surname #+ " " + data.firstname+ " " + data.othername
			kk.append(j)
			return HttpResponse(json.dumps(kk), content_type='application/json')
		else:
			gdata = ""
			return render(request,'index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')









@csrf_exempt
def getcashid(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			kk = []
			sdic = {}
			data = Userprofile.objects.get(email = acccode, ceo=1)

			branchcode = data.branch.id
			branchcode=tblBRANCH.objects.get(id=branchcode)

			allcashier = Userprofile.objects.filter(cashier=1,status=1,branch=branchcode)

			for j in allcashier:
				j = j.staffrec.id  #uses ID from tblSTAFF
				s = {j:j}
				sdic.update(s)
			klist = sdic.values()
			for p in klist:
				kk.append(p)
			return HttpResponse(json.dumps(kk), content_type='application/json')

		# else:
		# 	gdata = ""
		# 	return render(request,'index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def getcashname(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			kk=[]

			data=tblSTAFF.objects.get(id=acccode)
			j = data.surname
			kk.append(j)
			return HttpResponse(json.dumps(kk), content_type='application/json')
		else:
			gdata = ""
			return render(request,'index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def getcashreportajax(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']
				ID,name,dates,report= acccode.split(':')
				stlist = []

				# if dates == "":
				# 	dates =date.today()
				# else:
				# 	dates = request.POST['date']

				dday,mday,yday = dates.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				oydate=date(yday,mday,dday)
				weekday=int(date(yday,mday,dday).isocalendar()[1])

				relcashier = tblSTAFF.objects.get(id=ID)
				relcashier=relcashier.email

				if report == 'daily':
					merc = tblIamerchantBank.objects.filter(remitted_by =relcashier,recdate=oydate)
				elif report == 'weekly':
					merc= tblIamerchantBank.objects.filter(remitted_by=relcashier,weekno=weekday)

				elif report== 'monthly':
					merc=tblIamerchantBank.objects.filter(remitted_by=relcashier,recdate__month=mday)

				if merc.count() == 0:
					add = 0
				else:
					addw = merc.aggregate(Sum('amount'))
					add = addw['amount__sum']
				return render(request,'Ia/dailyreport.html',{'name':name,'total':add,'report':report})

			else:
				return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
		else:
			return render(request,'Ia/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')





@csrf_exempt
def getadminid(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			kk = []
			sdic = {}
			data = Userprofile.objects.get(email = acccode, ceo=1)

			branchcode = data.branch.id
			branchcode=tblBRANCH.objects.get(id=branchcode)

			alladmin = Userprofile.objects.filter(admin=1,status=1,branch=branchcode)

			for j in alladmin:
				j = j.staffrec.id
				s = {j:j}
				sdic.update(s)
			klist = sdic.values()
			for p in klist:
				kk.append(p)
			return HttpResponse(json.dumps(kk), content_type='application/json')

		# else:
		# 	gdata = ""
		# 	return render(request,'index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def getadminname(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			kk=[]
			data=tblSTAFF.objects.get(id=acccode)
			j = data.surname
			kk.append(j)
			return HttpResponse(json.dumps(kk), content_type='application/json')
		else:
			gdata = ""
			return render(request,'index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def getadminreportajax(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']
				ID,name,dates,report= acccode.split(':')
				stlist = []

				# if dates == "":
				# 	dates =date.today()
				# else:
				# 	dates = request.POST['date']

				dday,mday,yday = dates.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				oydate=date(yday,mday,dday)
				weekday=int(date(yday,mday,dday).isocalendar()[1])

				relcashier = tblSTAFF.objects.get(id=ID)
				relcashier=relcashier.email

				if report == 'daily':
					merc = tblIamerchantBank.objects.filter(remitted_by =relcashier,recdate=oydate)
				elif report == 'weekly':
					merc= tblIamerchantBank.objects.filter(remitted_by=relcashier,weekno=weekday)

				elif report== 'monthly':
					merc=tblIamerchantBank.objects.filter(remitted_by=relcashier,recdate__month=mday)

				if merc.count() == 0:
					add = 0
				else:
					addw = merc.aggregate(Sum('amount'))
					add = addw['amount__sum']
				return render(request,'Ia/dailyreport.html',{'name':name,'total':add,'report':report})

			else:
				return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
		else:
			return render(request,'Ia/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def getadminreportajax(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']
				ID,name,dates,report= acccode.split(':')
				stlist = []

				# if dates == "":
				# 	dates =date.today()
				# else:
				# 	dates = request.POST['date']

				dday,mday,yday = dates.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				oydate=date(yday,mday,dday)
				weekday=int(date(yday,mday,dday).isocalendar()[1])

				relcashier = tblSTAFF.objects.get(id=ID)
				relcashier=relcashier.email

				if report == 'daily':
					merc = tblIamerchantBank.objects.filter(approved_by =relcashier,recdate=oydate)
				elif report == 'weekly':
					merc= tblIamerchantBank.objects.filter(approved_by=relcashier,weekno=weekday)

				elif report== 'monthly':
					merc=tblIamerchantBank.objects.filter(approved_by=relcashier,recdate__month=mday)

				if merc.count() == 0:
					add = 0
				else:
					addw = merc.aggregate(Sum('amount'))
					add = addw['amount__sum']
				return render(request,'Ia/dailyreport.html',{'name':name,'total':add,'report':report})

			else:
				return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
		else:
			return render(request,'Ia/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')



def customerslist(request):
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
		if staff.ceo==1 :
			client_list = tblCUSTOMER.objects.filter(branch=mybranch)
			return render(request,'Ia/cust_list.html',{'company':mybranch,'user':varuser,'client_list':client_list})

		elif staff.thrift_officer== 1:
			memmerchant=tblIaMERCHANT.objects.get(thrift1a =1,staff=memstaff,status=1)
			client_list = tblCUSTOMER.objects.filter(branch=mybranch)
			return render(request,'Ia/cust_list_merc.html',{'company':mybranch,'user':varuser,'client_list':client_list})
		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')


def switches(request):
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

		if staff.ceo==0:
				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = switchesform(request.POST)
			if form.is_valid():
				mymerchant=form.cleaned_data['merchant']

				merch_count = tblIaMERCHANT.objects.filter(branch=mybranch,status=1).count()
				if merch_count> 1:

					try :
						msg = 'Coming soon'
						mmme= tblIaMERCHANT.objects.get(thrift1a =1,branch=mybranch,status=1,id=mymerchant)
						cus_list = tblCUSTOMER.objects.filter(branch=mybranch,status=1)
						if cus_list > 0 :
							form = newswitchform()
							return render(request,'Ia/switchproc.html',{'company':mybranch,'user':varuser,
								'merchant':mmme,'customer':cus_list,'form':form})
						else :
							msg = 'No customers found'
					except:
						msg = 'Invalid ID'
				else:
					msg='YOU MUST HAVE A MINIMUM OF 2 FIELD WORKERS'
		else:
			form=switchesform()
			msg = ''
		return render(request,'Ia/switch.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def getallstall(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			mrp = tblIaMERCHANT.objects.get(thrift1a =1,id=acccode)
			branch=mrp.branch.id
			branch=tblBRANCH.objects.get(id=branch)
			merc = tblIaMERCHANT.objects.filter(branch=branch,status=1).exclude(id=acccode)
			kk=[]
			kk.append('-----')
			for jj in merc :
				gh =  jj.id
				kk.append(gh)

			return HttpResponse(json.dumps(kk), content_type='application/json')

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def getbutton(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			if acccode== '-----':
				return render(request,'Ia/selmerch.html')

			else:
				merchant=tblIaMERCHANT.objects.get(id=acccode)
				return render(request,'Ia/switchmerc.html',{'merchant':merchant})
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')


@csrf_exempt
def openoption(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':

			if 'ggg' in request.POST :
				a= request.POST['ggg']

				# post = request.POST.copy()

				# acccode = post['userid']
				# if acccode== '-----':
				return render(request,'Ia/selmerch.html',{'sd':a})

			else:
			# 	merchant=tblIaMERCHANT.objects.get(id=acccode)
				return render(request,'Ia/switchmerc.html')
		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')




























def mysmss(request):
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

		return render(request,'Ia/buysmsm.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')












###Receipts*********************

def receipts(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'Ia/404.html')

		if staff.ceo==0:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblIaMERCHANT.objects.get(branch=mybranch, thrift1a =1,staff=memstaff,status=1)
		except:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			location=request.POST['location'] #month in figures
			yyr=request.POST['business_year']

			ddat = request.POST['mydate']

			rectype = request.POST['receipt_type']

			ok=0

			if rectype=='dep':
				status='CR'
				ok=3
				nature='Deposit'
			elif rectype =='wit':
				status='DR'
				ok=3
				nature='Withdrawal'
			elif rectype=='recon':
				status='CR'
				nature='Reconciliation'
				ok=4


			llit =[]


			cc = tblCUSTOMER.objects.filter(branch=mybranch,location=location)


			if ok ==3:

				p=0



				for kk in cc:
					wallet=kk.wallet
					try:
						c2 = tblIaCUSTOMER.objects.get(customer = kk)
						g = tblIamerchantBank.objects.filter(branch=mybranch,customer=c2,transdate=ddat,status=status)
						if g.count() > 0:
							cde=g[p].code
							tth=tblIathrift.objects.get(code=cde)
							cycle=tth.cycle
							card=tth.purpose


							total_savings= int(account_balance(mybranch, c2,cycle,card))
							ncr=g.aggregate(Sum('amount'))
							ncr = ncr['amount__sum']

							cy = {'total':ncr,'mycustomer':g,'status':nature,'total_savings':total_savings,'thrift':tth.thrift}

							llit.append(cy)

					except:
						g=0
					p=p+1


				return render(request,'Ia/genreciept.html',{
					'company':mybranch,
					'receipt':llit})





			elif ok ==4:

				for kk in cc:

					try:
						c2 = tblIaCUSTOMER.objects.get(customer = kk)
						g = tblIamerchantBank.objects.filter(branch=mybranch,customer=c2,transdate=ddat,status=status)

						if g.count() > 0:

							for bv in g:
								if bv.merchant.staff.ceo == 0:

									ncr=g.aggregate(Sum('amount'))
									ncr = ncr['amount__sum']

									cy = {'total':ncr,'mycustomer':bv,'status':nature}

									llit.append(cy)

					except:
						g=0


				return render(request,'Ia/recon.html',{
					'company':mybranch,
					'receipt':llit,
					'admin':staff})


				return render(request,'Ia/all_app_success.html',{
					'company':mybranch,
					'fo':merchant2,
					'admin':staff,
					'date':ddd,
					'time':tti,
					'currency':currency,
					'user':varuser,
					'amount':amount1})



		else:
			return render(request,'Ia/receipts.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



###**************Customer edit **********
@csrf_exempt
def editcusnamepop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1)


			return render(request,'Ia/editname.html',{'user':user,'customer':details,'wallet':wallet})



		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def editcusname(request):
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

		if staff.thrift_officer==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			wallet =request.POST['wallet']

			surname =request.POST['surname']
			firstname =request.POST['firstname']
			othername = request.POST['othername']


			cus=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
			cus.surname=surname
			cus.firstname=firstname
			cus.othername=othername
			cus.save()


			return HttpResponseRedirect('/fts/customer/viewwallet/'+wallet+'/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def editcusemailpop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1)


			return render(request,'Ia/editemail.html',{'user':user,'customer':details,'wallet':wallet})



		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def editemail(request):
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

		if staff.thrift_officer==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			wallet =request.POST['wallet']

			email =request.POST['newemail']



			cus=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)


			cus.email=email
			cus.save()



			return HttpResponseRedirect('/fts/customer/viewwallet/'+wallet+'/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')








@csrf_exempt
def editcusphonelpop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1)


			return render(request,'Ia/editphone.html',{'user':user,'customer':details,'wallet':wallet})



		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def editphone(request):
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

		if staff.thrift_officer==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			wallet =request.POST['wallet']

			newphone =request.POST['newphone']
			if newphone != "":
				cus=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)
				cus.phone=newphone
				cus.save()



			return HttpResponseRedirect('/fts/customer/viewwallet/'+wallet+'/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')


















































@csrf_exempt
def editlocationpop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1)

			loc = tblbusinesslocations.objects.filter(branch=mybranch)


			return render(request,'Ia/editloc.html',{'user':user,'customer':details,'wallet':wallet,'k':loc})



		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def editlocation(request):
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

		if staff.thrift_officer==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			wallet =request.POST['wallet']

			location =request.POST['location']

			cus=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)

			cus.location=location
			cus.save()

			return HttpResponseRedirect('/fts/customer/viewwallet/'+wallet+'/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def editaddrpop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				status=1)




			return render(request,'Ia/editaddr.html',{'user':user,'customer':details,'wallet':wallet})



		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def editaddr(request):
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

		if staff.thrift_officer==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			wallet =request.POST['wallet']

			addre =request.POST['newadd']

			cus=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)

			cus.Address=addre
			cus.save()

			return HttpResponseRedirect('/fts/customer/viewwallet/'+wallet+'/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')




@csrf_exempt
def editstapop(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']
			wallet,user=acccode.split(':')

			staff = Userprofile.objects.get(email=user,status=1, thrift1a=1)


			staffdet=staff.staffrec.id
			branch=staff.branch.id

			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompany=tblCOMPANY.objects.get(id=comp_code)

			mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

			memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

			mem=tblIaMERCHANT.objects.filter(staff=memstaff, thrift1a=1, status=1)
			memmerchant=mem.count()


			if staff.thrift_officer==0  or memmerchant<1:

				return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
			else:
				memmerchant= mem.get(staff=memstaff, thrift1a=1, status=1)


			details=tblCUSTOMER.objects.get(branch=mybranch,
				wallet=wallet,
				# status=1
				)

			if details.status == True:
				selected= 'checked'
				status='Active'

			else:

				selected='unchecked'
				status='Inactive'



			return render(request,'Ia/editstatus.html',{'user':user,'customer':details,'wallet':wallet,'selected':selected,'status':status})



		else:
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def editsta(request):
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

		if staff.thrift_officer==0 :
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})



		if request.method == 'POST':
			wallet =request.POST['wallet']


			if 'myststus' in request.POST:
				stat =1 #request.POST['myststus']

			else:
				stat= 0


			cus=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet)

			cus.status= stat
			cus.save()

			return HttpResponseRedirect('/fts/customer/viewwallet/'+wallet+'/')

		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/user/')



