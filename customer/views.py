# Create your views here.

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json

from customer.forms import *
from customer.models import *



from Ia.models import *
from Ia.utils import *
from thriftplus.utils import *


# from Ib.models import *
# from Ib.utils import *
# from Ib.utils import *

from customer.utils import *

from num2words import num2words

from sysadmin.models import *



from datetime import *
import calendar

#######import only merchant.models******
from calendar import monthrange

from django.core.serializers.json import json

from django.db.models import Max,Sum

import random
import datetime


def createwallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render(request,'customer/selectloan.html',{'msg':msg})





		staffdet=staff.staffrec.id

		branch_code=staff.branch.code
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,code=branch_code)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		msg = ''

		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']

			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']
			location = request.POST['location']


			# phone=generate_phone()
			wallet=generate_phone() ########1

			if 'photo' in request.FILES: #if image is attached
				photo=request.FILES['photo']
			else:
				photo = 'customerpix/user.png'


			phone=str(phone)

			try:
				countt=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)

			except:
				pin =  generate_trans_pin()

				dddy = datetime.datetime.today()
				fdate = dddy.date()
				ttime=dddy.time()

				tblCUSTOMER(surname=surname,
					firstname=firstname,
					othername=othername,
					phone=phone,
					Address=address,
					wallet=wallet,
					location=location,
					created_by=memstaff,
					created_date=fdate,
					ttime =ttime,
					code=pin,
					email=email,
					branch=mybranch,
					status=1,
					photo=photo).save()



				try:
					wallet_registration(email)
				except:
					pass

			customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)


			if staff.thrift1a == 1: #if esusu is activated
				memmerchant = tblIaMERCHANT.objects.get(branch=mybranch,staff=memstaff, thrift1a=1,status=1)
				
				cs=tblIaCUSTOMER.objects.filter(branch=mybranch,customer=customer)


				if cs.count() == 0:
					tblIaCUSTOMER(branch=mybranch,merchant=memmerchant,customer=customer,
						status=1,code=pin,sms=0,get_email=1, withdr_status=1).save()

				try:
					customer_activationIa(email)
				except:
					pass


			return render(request,'customer/success.html',{'company':mybranch,
				'wallet':wallet,
				'user':varuser,
				'surname':surname,
				'firstname':firstname,
				'othername':othername})

		else:

			history = checkhighestsub(mybranch)



			gh = tblIaCUSTOMER.objects.filter(branch=mybranch).count()
			ddt = date.today()



			# return render(request,'customer/selectloan.html',{'msg':history})




			if history['status'] == 'Running':
				if gh > history['numbers'] :

					msg = 'you cannot proceed beyond this point, until you do something about your subscription'
					return render(request,'customer/selectloan4.html',{'company':mybranch,'msg':msg,'user':varuser})

				else:

					if int(gh) < int(history['numbers']):
						msg=''



						pincode = tblbusinesslocations.objects.filter(branch=mybranch)
						if pincode.count() > 0 :

							if staff.ceo == 1:



								return render(request,'customer/createwallet.html',{'company':mybranch,
									'user':varuser,
									'msg':msg,
									'k':pincode})


							elif staff.thrift_officer == 1:
								mm = tblIaMERCHANT.objects.get(branch=mybranch,staff=memstaff)

								pincode = tblIalocations.objects.filter(branch=mybranch,merchant=mm)

								return render(request,'customer/createwallet_field.html',{'company':mybranch,
									'user':varuser,
									'msg':msg,
									'k':pincode})


						else:

							msg = 'you are yet to set up the locations covered by your business'
							return render(request,'customer/loc.html',{'company':mybranch, 'user':varuser,'msg':msg})# ('customer/loc.html',{'msg':msg})

					else:
						msg= 'you have reched the maximum customer count allowed for your package'
						return render(request,'customer/selectloan4.html',{'company':mybranch,'msg':msg})



			else:
				msg = 'Kindly check your suscription status'
				return render(request,'customer/selectloan4.html',{'company':mybranch,'msg':msg,'user':varuser})




	else:
		return HttpResponseRedirect('/login/user/')





def editwallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render(request,'customer/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if request.method == 'POST':
			form= viewwalletform(request.POST)
			msg='Try again later'

			if form.is_valid():
				wallet=form.cleaned_data['wallet']
				try:
					customer=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
					msg=''
					return render(request,'customer/myeditwallet.html',{'company':mybranch,
					'user':varuser,'wallet':wallet,'form':form,'customer':customer})

				except:
					msg='INVALID WALLET ADDRESS'
					return render(request,'customer/selectloan.html',{'msg':msg})
		else:
			form = viewwalletform()
			msg=''

		return render(request,'customer/editwallet.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def doedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render(request,'customer/selectloan.html',{'msg':msg})


		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.ceo == 0:
			return render(request,'customer/404.html',{'company':mybranch, 'user':varuser})
		msg = ''

		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']
			wallet= request.POST['wallet']

			if 'photo' in request.FILES:
				photo=request.FILES['photo']
			else:
				photo = 'customerpix/user.png'


				ccc = tblCUSTOMER.objects.filter(branch=mybranch,wallet=wallet, status=1).update(
					surname=surname,firstname= firstname, othername=othername,
					Address=address,email=email,photo=photo)


				try:
					wallet_edit(email)
				except:
					pass

				return render(request,'customer/editwallet_successful.html',{'company':mybranch,'user':varuser,'wallet':wallet})


		# return render(request,'customer/createwallet.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def viewwallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']


		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render(request,'customer/selectloan.html',{'msg':msg})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				wallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(branch=mybranch, wallet=wallet,status=1)
					return render(request,'customer/walletdetails.html',{'company':mybranch,'user':varuser,'details':details})
				except:
					msg = 'invalide wallet address'
					return render(request,'customer/viewwallet.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			else:
				pass
		else:
			form=viewwalletform()
		return render(request,'customer/viewwallet.html',{'company':mybranch,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')





def customerslist(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			msg = ' your account is no longer active, kindly contact your boss'

			return render(request,'customer/selectloan.html',{'msg':msg})



		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompany=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblIaMERCHANT.objects.get(staff=memstaff,status=1)

		location= tblIalocations.objects.filter(branch=mybranch,merchant=memmerchant)
		locc=[a.location for a in location]
		# location='locogoma' 
		# return render(request,'customer/selectloan.html',{'msg':locc})
		if staff.ceo==1 :
			client_list = tblCUSTOMER.objects.filter(branch=mybranch).order_by('surname','firstname','othername')
			return render(request,'customer/cust_list.html',{'company':mybranch,'user':varuser,'client_list':client_list})

		elif staff.thrift_officer== 1:
			allclient=[]
			for location in locc:
				mylist = tblCUSTOMER.objects.filter(branch=mybranch,location=location)
				client_list= {'cus':mylist}
				allclient.append(client_list)		
			return render(request,'customer/cust_list_merc.html',{'company':mybranch,'user':varuser,'clients':client_list})
		else:
			return render(request,'customer/404.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')






# ##********************customers****************************
def cus_list(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'customer/404.html')

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
			return render(request,'customer/404.html',{'company':mybranch, 'user':varuser})
		else:
			memmerchant= gg.get()


		if staff.admin:
			cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch)
		else:
			cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch)
			# cutlist = tblIaCUSTOMER.objects.filter(branch=mybranch,merchant=memmerchant)

		form = locationform()
		if staff.ceo==1:
			return render(request,'customer/custlist.html',{'company':mybranch,'form':form, 'user':varuser,'client_list':cutlist})
		else:
			return render(request,'customer/custlist_to.html',{'company':mybranch,'form':form, 'user':varuser,'client_list':cutlist})
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
				return render(request,'customer/noloc.html',{'user':user,'location':location})

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

				return render(request,'customer/listcajax.html',{'dat':gg,'user':user,'location':location})


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
				return render(request,'customer/selectloan.html',{'msg':msg})

			if location=='-----':
				msg = 'Select Area'

				return render(request,'customer/selectloan.html',{'msg':msg})

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

			return render(request,'customer/listcajax.html',{'dat':gg,'user':user,'location':location})


	else:
		return HttpResponseRedirect('/login/user/')



