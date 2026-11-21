from django.shortcuts import render
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt



from . import utils
from partner.utils import *


from partner.forms import *


from sysadmin.models import *
from staff.models import *
from Ia.models import *
from sms.models import *
from IIIb.models import *
from customer.models import *



from datetime import *
import calendar
from calendar import monthrange
import random





# from Ib.models import *
# from IIIb.models import *

from django.db.models import Max,Sum
today=date.today()





def repair(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')


		if request.method == 'POST':
			wallet = request.POST['wallet']
			month_index = request.POST['month']
			cycle = request.POST['cycle']


			thriftcode = request.POST['thriftcode']


			month_name = calendar.month_name[int(month_index)]

			details=tblCUSTOMER.objects.get(wallet=wallet,status= True)


			year=2026

			customer1=tblIaCUSTOMER.objects.get(customer=details)

			thrift= tblIathrift.objects.filter(branch=details.branch,year=year,month=month_name,customer=customer1)

			ttp = thrift.filter(cycle=cycle ).values_list('code',flat=True)



			fa = tblIafieldagent.objects.filter(branch=details.branch)
			f = fa.filter(code__in=ttp)

			cus = tblIasavings_trans.objects.filter(branch=details.branch)
			sd = cus.filter(code__in = ttp)

			ofi = tblIamerchantBank.objects.filter(branch=details.branch)
			cc = ofi.filter(code__in = ttp)

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


			return render(request,'partner/repair.html',{'company':mybranch,'user':varuser,'msg':s,'wallet':wallet,'month':month_name,'cycle':cycle2})



		msg=0

		return render(request,'partner/repair.html',{'company':mybranch,'user':varuser,'ms':msg})

	else:
		return HttpResponseRedirect('/login/user/')




def welcome(request):

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

		if staff.partner==0:
			return render(request,'partner/404.html')

		return render(request,'partner/welcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')




def restart(request):

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

		if staff.partner==0:
			return render(request,'partner/404.html')

		x=[]

		if request.method == 'POST':
			email=request.POST['email']
			df =tblSTAFF.objects.filter(email=email)
			mybranch=tblBRANCH.objects.filter(id__in=df)
			f ={'staff':df,'branch':mybranch}
			x.append(f)
			return render(request,'partner/reset1.html',{'company':mybranch, 'user':varuser,
				'mybranch':x,'email':email})

		else:
			return render(request,'partner/reset.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



def rrr(request):

	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch2=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.partner==0:
			return render(request,'partner/404.html')

		x=[]

		if request.method == 'POST':
			email=request.POST['email']

			df =tblSTAFF.objects.filter(email=email)
			d=[a.branch.id for a in df]
			mybranch=tblBRANCH.objects.get(id__in=d)

			# f = tblCOMPANY.objects.filter(branch= mybranch).delete()

			d= tblBRANCH.objects.filter(id__in = d).delete()

			s = tblmanager.objects.filter(branch= mybranch).delete()


			sd= tblapp.objects.filter(branch= mybranch).delete()

			ds= tblCUSTOMER.objects.filter(branch= mybranch).delete()

			fd = tblIaMERCHANT.objects.filter(branch= mybranch).delete()

			xfd = tblIaCUSTOMER.objects.filter(branch= mybranch).delete()

			d= tblIalocations.objects.filter(branch= mybranch).delete()

			dvs = tblIathrift.objects.filter(branch= mybranch).delete()

			f=tblIafieldagent.objects.filter(branch= mybranch).delete()

			dv= tblIamerchantBank.objects.filter(branch= mybranch).delete()



			srr=tblIasavings_trans.objects.filter(branch= mybranch).delete()


			r=  tblIacards.objects.filter(branch= mybranch).delete()

			dsd= tblIapayoutrequest.objects.filter(branch= mybranch).delete()


			sx= tblIapayoutrecord.objects.filter(branch= mybranch).delete()


			df=tblIbbfieldagent.objects.filter(branch= mybranch).delete()

			gh=  tblIbbsavings_trans.objects.filter(branch= mybranch).delete()

			df= tblIastandardloan.objects.filter(branch= mybranch).delete()
			dfs=  tblIagrace.objects.filter(branch= mybranch).delete()

			tg= tblloandetails.objects.filter(branch= mybranch).delete()

			sea= tblloanrepay.objects.filter(branch= mybranch).delete()

			sd= tblIatv.objects.filter(branch= mybranch).delete()

			fg= tblIbco.objects.filter(branch= mybranch).delete()

			cxv =  tblIbCUSTOMER.objects.filter(branch= mybranch).delete()

			cxv =  tblIbsavings_trans.objects.filter(branch= mybranch).delete()

			cxv =  tblIbMERCHANTbank.objects.filter(branch= mybranch).delete()
			cxv =  tblIbfieldagent.objects.filter(branch= mybranch).delete()

			cxv =  tblIbpayoutrequest.objects.filter(branch= mybranch).delete()

			cxv =  tblIbCashier.objects.filter(branch= mybranch).delete()


			cxv =  tblIbinterest.objects.filter(branch= mybranch).delete()

			cxv =  tblIbstandardloan.objects.filter(branch= mybranch).delete()

			cxv =  tblIbbankdetail.objects.filter(branch_code= mybranch).delete()


			cxv =  tblIbloanrequests.objects.filter(branch= mybranch).delete()



			cxv =  tblIbloanrepaymentplan.objects.filter(branch= mybranch).delete()

			cxv =  tblIbloantransaction.objects.filter(branch= mybranch).delete()


			cxv =  tblIbgrace.objects.filter(branch= mybranch).delete()


			cxv =  tblIIIbcoop.objects.filter(branch= mybranch).delete()

			cxv =  tblIIIIbassets_authorization.objects.filter(branch= mybranch).delete()

			cxv =  tblIIIbclientsubscription.objects.filter(branch= mybranch).delete()

			cxv =  tblIIIbprorations_schedule.objects.filter(branch= mybranch).delete()

			cxv =  tblIIIbapprovals.objects.filter(branch= mybranch).delete()

			cxv =  tblIIIbprorations.objects.filter(branch= mybranch).delete()

			cxv =  tblIIIbdisbursals.objects.filter(branch= mybranch).delete()

			cxv =  tblstandardloanIIIB.objects.filter(branch= mybranch).delete()

			cxv =  tblstandardsavingIIIB.objects.filter(branch= mybranch).delete()

			cxv =  tblIIIb_bankdetail.objects.filter(branch_code= mybranch).delete()

			cxv =  tblIIIbloandapplications.objects.filter(branch= mybranch).delete()

			cxv =  tblIIIbcommapplications.objects.filter(branch= mybranch).delete()


			cxv =  tblmaxloanIIIB.objects.filter(branch= mybranch).delete()


			cxv =  tblIIIbsavingsaccount.objects.filter(branch= mybranch).delete()


			cxv =  tblSTAFF.objects.filter(branch= mybranch).delete()



			cxv =  tblMERCHANT.objects.filter(branch= mybranch).delete()


			cxv =  Userprofile.objects.filter(branch= mybranch).delete()


			cxv =  tblsubscription.objects.filter(branch= mybranch).delete()


			cxv =  tblsubpending.objects.filter(branch= mybranch).delete()

			cxv =  tbldefaultpass.objects.filter(branch= mybranch).delete()


			cxv =  tblbusinesslocations.objects.filter(branch= mybranch).delete()


			cxv =  tblrollover.objects.filter(branch= mybranch).delete()


			cxv =  tblcarding.objects.filter(branch= mybranch).delete()


			cxv =  tblproductsname.objects.filter(branch= mybranch).delete()



			cxv =  tblbusinessyear.objects.filter(branch= mybranch).delete()

			d='ok'

		return render(request,'partner/reset.html',{'company':mybranch2, 'user':varuser,'d':d})

	else:
		return HttpResponseRedirect('/login/user/')












def registration(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)

		if staff.partner==0:
			return render(request,'partner/404.html')
		if request.method == 'POST':
			name=request.POST['Name']
			web=request.POST['website']
			insta = request.POST['instagram']
			facebook = request.POST['facebook']
			twit= request.POST['twitter']
			youtube = request.POST['youtube']

			mycom = tblCOMPANY.objects.filter(name=name)


			if 'logo' in request.FILES: #if image is attached
				logo=request.FILES['logo']
			else:
				logo = 'company_logo/thrift.png'


			if mycom.count() ==0:
				company_code = generate_pin()
				tblCOMPANY(engine='tts',
					web=web,
					code=company_code,
					name=name,
					twitter=twit,
					youtube=youtube,
					fb=facebook,
					ux=0,
					status=1,
					logo=logo,
					partner=partnerfff,
					ig=insta,size=20).save()



			else:
				msg= 'busines already exists'

			com = tblCOMPANY.objects.get(name=name)

			return render(request,'partner/busregistersuccess.html',{'company':mybranch,
				'user':varuser,
				'business':com})

		else:
			return render(request,'partner/register.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def branch(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')


		if request.method == 'POST':
			form = companyform(request.POST)

			if form.is_valid():
				companygg= form.cleaned_data['company']

				try:
					trial=request.POST['trial']
				except:
					trial = 2

				k = tblCOMPANY.objects.filter(id =companygg)

				if k.count() ==1:
					cc = k.get()
					br = tblBRANCH.objects.filter(company=cc)

					if br.count() ==1:
						br=br.get()

						return render(request,'partner/branchsuccess.html',{'company':mybranch,'user':varuser,'comp':br,'trial':trial})

					elif br.count() ==0:
						bp  = tblbusinesspresence.objects.filter(status=1)
						return render(request,'partner/branch_reg.html',{'company':mybranch,'user':varuser,'comp':cc,'data':bp})
				else:
					msg = 'Details not found'

		else:
			form = companyform()
			msg=''

		return render(request,'partner/branch.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')


def address(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.partner==0:
			return render(request,'partner/404.html')

		if request.method == 'POST':
			address= request.POST['address']
			phone = request.POST['phone']
			company=request.POST['company']

			country=request.POST['country']
			trial=request.POST['trial']

			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])


			try:
				phone=int(phone)
			except:
				msg = 'Incomplete phone number'
				return render(request,'partner/branch.html',{'company':mybranch,'user':varuser})

			det=[]
			partner=tblPARTNER.objects.get(email=varuser)

			k = tblCOMPANY.objects.filter(id =company,partner=partner)
			kc =k.count()
			if kc ==1:
				k =k.get(id=company)

				branch_code = generate_pin()

				bc= tblBRANCH.objects.filter(company=k,
					status=1,
					Address=address)

				if bc.count() == 0:

					bp = tblbusinesspresence.objects.get(country_code=country)

					tblBRANCH(company=k,code=branch_code, currency_description= bp.currency_description,
						status=1,
						Address=address,
						country_code=bp.country_code,
						phone=phone,
						types='Head',
						currency_code=bp.currency_code).save()

				bb = tblBRANCH.objects.get(company=k)


				ddt = date.today()

				yyr= ddt.year
				mmt= ddt.month
				ddd=ddt.day


				bby= tblbusinessyear.objects.filter(branch=bb,year=ddt.year)
				if bby.count() == 0:
					tblbusinessyear(branch=bb,year=ddt.year).save()

				rro = tblrollover.objects.filter(branch=bb,year=ddt.year)
				if rro.count() == 0 :
					tblrollover(branch=bb,year=ddt.year,status=1).save()


				f= tblapp.objects.filter(branch=bb)
				if f.count() == 0:
					tblapp(branch=bb,partner=partner).save()

				return render(request,'partner/branchsuccess.html',{'company':mybranch,'user':varuser,'comp':bb,'trial':trial})


			else:
				return render(request,'partner/branch.html',{'company':mybranch,'user':varuser})


		else:

			return HttpResponseRedirect('/partner/partner/business/branch/')

	else:
		return HttpResponseRedirect('/login/user/')



def ceo(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)
		if staff.partner==0:
			return render(request,'partner/404.html')

		if request.method == 'POST':
			form = companyform(request.POST)
			detail =[]

			if form.is_valid():
				companygg= form.cleaned_data['company']
				try:
					trial=request.POST['trial']
				except:
					trial=2


			k2 = tblCOMPANY.objects.filter(id =companygg,partner=partnerfff)

			if k2.count() ==1:
				k=k2.get()
				ad= tblBRANCH.objects.filter(company=k) #long object
				if ad.count()==1:
					ad= ad.get()

					oona = Userprofile.objects.filter(branch=ad, ceo = 1)
					if oona.count()==1:
						oona=oona.get()
						sdr = tblSTAFF.objects.get(email= oona.email)

						return render(request,'partner/ceosuccess1.html',{'company':ad,'user':varuser,'business':k,'staff':sdr,'trial':trial})

					else:

						jk = {'name':k.name.upper(),'address':ad,'id':k.id}
						detail.append(jk)


						return render(request,'partner/ceoreg.html',{'company':mybranch,'user':varuser,'comp':detail,'trial':trial})

				else:
					msg='address not found'
			else:
				msg = 'Reocrd not found'
		else:
			form = companyform()
			msg=''

		return render(request,'partner/ceo.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def regceo(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)

		if staff.partner==0:
			return render(request,'partner/404.html')

		if request.method == 'POST':

			company=request.POST['company']
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']


			try:
				trial = request.POST['trial']
			except:
				trial = 2

			phone=phone.split(' ')
			phone = int(phone[0]+phone[1]+phone[2])


			try:
				phone=int(phone)
			except:
				msg = 'Incomplete phone number'
				return render(request,'thrift/ceoreg.html',{'company':mybranch, 'user':varuser,'msg':msg})



			k = tblCOMPANY.objects.get(id =company,partner=partnerfff)
			branch= tblBRANCH.objects.get(company=k)
			business_name=k.name
			branch_code=branch.code

			passw=generate_pin()


			staff= tblSTAFF.objects.filter(email=email)

			if staff.count() ==0:
				tblSTAFF(branch=branch,status = 1, ceo=1, code=branch_code,surname=surname,firstname=firstname,
					othername=othername,photo='staff-pix/user.png',email=email,
					phone=phone,Address=address,types='Field').save()

			else:
				msg = "email already in use"

				return render(request,'partner/selectloan2.html',{'msg':msg})



			staff= staff.get()

			uu = Userprofile.objects.filter(status=1,email=email)


			if uu.count() ==0:

				Userprofile(status=1,branch=branch,code=branch_code,ceo=1,
					staffrec=staff,password=passw,email=email).save()


			#send email to the ceo, telling him of his login details

			try:
				backoffice_reg(email,passw,surname,firstname,business_name )
			except:
				gh=0




			return render(request,'partner/ceosuccess1.html',{'company':branch,
				'business':k,'user':varuser,'staff':staff,'trial':trial})

		else:
			return HttpResponseRedirect('/partner/partner/business/ceo/')

	else:
		return HttpResponseRedirect('/login/user/')



def app(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')

		if request.method == 'POST':
			form = companyform(request.POST)
			myy =[]

			if form.is_valid():
				company= form.cleaned_data['company']

				company = tblCOMPANY.objects.filter(id=company)


				try:
					trial=request.POST['trial']
				except:
					trial = 2


				if company.count() ==1:
					company=company.get()

					branches = tblBRANCH.objects.filter(company = company, status=1 )

					if branches.count() == 1:

						bbb=branches[0]

						owner=Userprofile.objects.filter(branch=bbb,ceo=1)

						if owner.count()== 0:
							msg='no ceo found'

							return render(request,'partner/comp_details_ceo.html',{'company':mybranch,
								'user':varuser,
								'business':company})

						else:

							details={'business':branches,'owner':owner}

							return render(request,'partner/comp_details.html',{'company':mybranch,
								'user':varuser,
								'trial':trial,
								'business':company,
								'branch':details})

					else:
						msg = 'Address not found'

				else:
					msg ='Details not found'
					return render(request,'partner/app.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

			else:
				msg=''
		else:
			form = companyform()
			msg=''

		return render(request,'partner/app.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')


def app3(request,bid):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')


		try:
			trial=request.POST['trial']
		except:
			trial = 2


		myy =[]


		my_ad = tblBRANCH.objects.filter(code =bid)
		ad_count = my_ad.count()

		if ad_count ==1:
			ad = my_ad.get()
			cid = ad.company.id
			company=tblCOMPANY.objects.get(id=cid,partner=partnerfff)

		else:
			msg ='Details not found'
			return render(request,'partner/app.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})



		my_apps = tblapp.objects.filter(branch=ad,partner=partnerfff)
		my_apps_count = my_apps.count()

		if my_apps_count ==1:
			apps = my_apps.get()


			if apps.thrift1a is True:
				dc= 'checked'

				if apps.esusu1a is True:
					esu= 'checked'
					esu_status='disabled'
					esu_value =1
				else:
					esu='unchecked'
					esu_status='enabled'
					esu_value =0


				if apps.esusu1aloan is True:
					esuloan= 'checked'
					esuloan_status='disabled'
					esuloan_value =1
				else:
					esuloan='unchecked'
					esuloan_status='enabled'
					esuloan_value =0

				if apps.savings1a is True:
					sav= 'checked'
					save_status='disabled'
					sav_value =1
				else:
					sav='unchecked'
					save_status='enabled'
					sav_value =0


				if apps.loans1acash is True:
					loc= 'checked'
					loc_status='disabled'
					loc_value =1
				else:
					loc='unchecked'
					loc_status='enabled'
					loc_value =0


				if apps.loans1aitems is True:
					loit= 'checked'
					loit_status='disabled'
					loit_value =1
				else:
					loit='unchecked'
					loit_status='enabled'
					loit_value =0


				if apps.fixeddepo1a is True:
					fixeddepo= 'checked'
					fxd_status='disabled'
					fxd_value =1
				else:
					fixeddepo='unchecked'
					fxd_status='enabled'
					fxd_value =0


				if apps.targetsave1a is True:
					tagsave= 'checked'
					tag_status='disabled'
					tag_value =1
				else:
					tagsave='unchecked'
					tag_status='enabled'
					tag_value =1

				s= { 'name':ad.company.name.upper(),'address':ad.Address,
				'id':ad.id,'dc':dc,

				'esu':esu, 'es':esu_status,'ev':esu_value,

				'esuloan':esuloan, 'esloan':esuloan_status,'evloan':esuloan_value,

				'sav':sav, 'sa':save_status,'sv':sav_value,
				'loancash':loc, 'cl':loc_status,'lcv':loc_value,
				'loanitem':loit, 'il':loit_status,'liv':loit_value,
				'fxd':fixeddepo, 'fx':fxd_status,'fxdv':fxd_value,
				'tagsave':tagsave, 'tgg':tag_status,'tgv':tag_value}

				myy.append(s)

				return render(request,'partner/applist1.html',{'company':mybranch,'user':varuser,'list':myy,'trial':trial})

			elif apps.thrift3b is True:

				coop= 'checked'



				s= { 'name':ad.company.name.upper(),'address':ad.Address,
				'id':ad.id,'dc':coop}

				myy.append(s)
				return render(request,'partner/applist.html',{'company':mybranch,'user':varuser,'list':myy})



			else:

				s= { 'name':ad.company.name.upper(),'address':ad.Address,'id':ad.id}

				myy.append(s)


				return render(request,'partner/appchoose.html',{'company':mybranch,'user':varuser,'list':myy,'trial':trial})



		return render(request,'partner/app.html',{'company':mybranch,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def app_update(request):

	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)


		if staff.partner==0:
			return render(request,'partner/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST' :
			branch_code= request.POST['branch']

			branch = tblBRANCH.objects.get(id=branch_code)

			# bb = branch
			# oldd = tblapp.objects.get(branch=branch)


			ceo=tblSTAFF.objects.get(branch=branch,ceo=1)


			if 'dc' in request.POST: ##****if you made any selection**8
				dc=request.POST['dc']
				try:
					trial=request.POST['trial']
				except:
					trial=2


				ddt = date.today()
				yyr= ddt.year
				mmt= ddt.month
				ddd=ddt.day

				p = (monthrange(ddt.year, ddt.month))[-1]

				nd = ddd + int(trial)

				if nd <= p:
					eend= date(yyr,mmt,nd)

				elif nd > p:
					if mmt == 12:
						mmt = 1
						yyr+=1

					else:
						mmt+=1

					nd = nd - p

					eend= date(yyr,mmt,nd)


				tp =tblthriftpackages.objects.get(package='Onboarding')

				sub = []


				if dc =='DC':

					app='DC'

					ff=0
					if 'esu' in request.POST: #Ajo
						esu=1
						sub.append('Esusu')
						ff=ff+ 1
						app ='Esusu'
					else:
						esu = 0

					if 'esuloan' in request.POST:
						esuloan=1
						sub.append('Ajo Loan')
						ff=ff+ 1
					else:
						esuloan = 0


					if esu ==1:

						onb= tblsubscription.objects.filter(branch=branch,package=tp,app =app)

						if onb.count() == 0:

							tblsubscription(status='Running',
								branch=branch,
								package=tp,
								duration=1,
								start =ddt,
								end = eend,
								app =app,
								amount=tp.cost,
								receipt=generate_pin()).save()





					if 'sav' in request.POST: #Normal Savings
						sav=1
						sub.append('Savings')
						ff=ff+ 1
					else:
						sav = 0

					if 'lc' in request.POST:
						lc=1
						sub.append('Cash Loans')
						ff=ff+ 1
						sav =1
					else:
						lc=0

					if 'li' in request.POST:
						li=1
						sub.append('Asset Loan')
						ff=ff+ 1

						sav =1
					else:
						li=0



					if sav ==1:

						app ='General Savings'

						onb= tblsubscription.objects.filter(branch=branch,package=tp,app =app)

						if onb.count() == 0:

							tblsubscription(status='Running',
								branch=branch,
								package=tp,
								duration=1,
								start =ddt,
								end = eend,
								app =app,
								amount=tp.cost,
								receipt=generate_pin()).save()

					if 'ecommerce' in request.POST:
						ecommerce=1
						sub.append('Ecommerce')
						ff=ff+ 1
					else:
						ecommerce = 0



					if ecommerce ==1:
						app ='Ecommerce'

						onb= tblsubscription.objects.filter(branch=branch,package=tp,app =app)

						if onb.count() == 0:

							tblsubscription(status='Running',
								branch=branch,
								package=tp,
								duration=1,
								start =ddt,
								end = eend,
								app =app,
								amount=tp.cost,
								receipt=generate_pin()).save()




					if 'tagsave' in request.POST:
						tagsave=1
						sub.append('Target Savings')
						ff=ff+ 1
					else:
						tagsave=0

					if 'fxd' in request.POST:
						fxd=1
						sub.append('Fixed Deposit')
						ff=ff+ 1
					else:
						fxd=0

					if tagsave ==1 or fxd ==1:
						inv =1

						app='Investment'

						onb= tblsubscription.objects.filter(branch=branch,package=tp,app =app)

						if onb.count() == 0:

							tblsubscription(status='Running',
								branch=branch,
								package=tp,
								duration=1,
								start =ddt,
								end = eend,
								app =app,
								amount=tp.cost,
								receipt=generate_pin()).save()


					else:
						inv=0


					if ff > 0:
						thrift1a=1
					else:
						thrift1a=0



					tblapp.objects.filter(branch=branch).update(
						thrift1a=thrift1a,

						esusu1a=esu,
						esusu1aloan=esuloan,


						savings1a=sav,
						loans1acash=lc,
						loans1aitems=li,

						investment=inv,
						fixeddepo1a=fxd,
						targetsave1a=tagsave)



					ssd = tblIaMERCHANT.objects.filter(branch=branch)
					sdr=ssd.count()
					if sdr < 1 :
						tblIaMERCHANT(branch=branch,
							direc_credit=1,
							direct_withdraw=1,
							code=generate_pin(),
							staff= ceo,
							status=1,
							thrift1a=1,

							esusu1a=esu,
							esusu1aloan=esuloan,


							savings1a=sav,
							loans1acash=lc,
							loans1aitems=li,

							fixeddepo1a=fxd,
							targetsave1a=tagsave).save()




					h=	Userprofile.objects.filter(branch=branch)
					if esu ==0 or esuloan ==0 or sav== 0 or lc==0 or li == 0 or tagsave==0 or fxd==0:

						ed=h.exclude(staffrec=ceo).update(
								thrift1a=thrift1a,
								esusu1a=False,
								esusu1aloan=False,
								thrift_officer= True,
								admin = False,
								savings1a= False,
								loans1acash=False,
								loans1aitems=False,
								fixeddepo1a=False,
								targetsave1a=False)



						ssd.exclude(staff=ceo).update(
								thrift1a=thrift1a,
								esusu1a=False,
								esusu1aloan=False,
								savings1a=False,
								loans1acash=False,
								loans1aitems=False,

								fixeddepo1a= False,
								targetsave1a= False)


					h.filter(staffrec=ceo).update(

							thrift1a=thrift1a,

							esusu1a=esu,
							esusu1aloan=esuloan,

							thrift_officer=True,
							admin =True,


							savings1a=sav,
							loans1acash=lc,
							loans1aitems=li,

							fixeddepo1a=fxd,
							targetsave1a=tagsave)



					return render(request,'partner/app_update_success.html',{'company':branch,
						'user':varuser,
						'comp':branch,
						'sub':str(sub)})

				elif dc == 'Coop':
					app='Coop'
					sub = 'Co-operatives'

					tblapp.objects.filter(branch=branch).update(thrift3b=1)
					Userprofile.objects.filter(branch=branch,ceo=1).update(thrift3b=1, thrift3b_officer=1,thrift3b_admin=1)


					s= tblIIIbcoop.objects.filter(branch= branch,staff= ceo)

					if s.count() == 0:

						coop =tblIIIbcoop.objects.create(branch=branch,staff= ceo, status=True, cooperators_code= generate_pin(),thrift3b = True)

					else:
						coop=s.get()

					if not tblIIIbthrift.objects.filter(branch =branch,staff =coop).exists():
						tblIIIbthrift.objects.create(branch =branch,staff =coop,can_get_loan = True, can_buy_commodity = True)






					onb= tblsubscription.objects.filter(branch=branch,package=tp,app =app)



					if onb.count() == 0:

						tblsubscription(status='Running',
							branch=branch,
							package=tp,
							duration=1,
							start =ddt,
							end = eend,
							app =app,
							amount=tp.cost,
							receipt=generate_pin()).save()

					return render(request,'partner/app_update_success.html',{'company':branch,
						'user':varuser,
						'comp':branch,
						'sub':str(sub)})


			else: ##****if you forgot to  make any selection**

				return render(request,'partner/404.html',{'company':branch, 'user':varuser})

		else:
			return HttpResponseRedirect('/partner/partner/business/App/')

	else:
		return HttpResponseRedirect('/login/user/')




def app_update_online_version(request):

	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)


		if staff.partner==0:
			return render(request,'partner/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST' :  #Thrifts*********************
			branch_code= request.POST['branch']
			branch = tblBRANCH.objects.get(id=branch_code)

			# memstaff=tblSTAFF.objects.get(branch=branch,email=varuser)

			sub = []
			unsub=[]
			oldd = tblapp.objects.get(branch=branch)


			k = random.randint(0,9)
			y = random.randint(0,9)
			x = random.randint(0,9)
			z = random.randint(0,9)
			a = random.randint(0,9)
			pin =  str(k) + str(y) + str(x) + str(z)+ str(a)


			######*****************#daily contribution*****************8
			if 'dc' in request.POST:
				dc=request.POST['dc']
			else:
				dc =0

			tblapp.objects.filter(branch=branch).update(thrift1a=dc)
			tblCUSTOMER.objects.filter(branch=branch, status=1).update(dc=dc)
			Userprofile.objects.filter(branch = branch).update(thrift1a=dc)

			ceo = Userprofile.objects.get(branch = branch, ceo=1)
			ceo.admin=dc
			ceo.cashier=dc
			ceo.thrift_officer=dc
			ceo.save()

			ceo_staff= ceo.staffrec.id
			ceo_staff=tblSTAFF.objects.get(id=ceo_staff)

			sdr = tblIaMERCHANT.objects.filter(branch=branch, staff=ceo_staff).count()
			if sdr < 1 :
				tblIaMERCHANT(branch=branch,
					direc_credit=1,
					direct_withdraw=1,
					code=pin,
					staff= ceo_staff ,
					status=1,thrift1a=1).save()

			tblIaMERCHANT.objects.filter(branch=branch).update(thrift1a=dc)


				#### handl the entry at tblmerhant



			if 'gs' in request.POST: ###########investment banking*****************************
				gs=request.POST['gs']

			else:
				gs = 0

			tblapp.objects.filter(branch=branch).update(thrift1b=gs)

			Userprofile.objects.filter(branch = branch).update(thrift1b=gs)

			Userprofile.objects.filter(branch = branch, ceo=1).update(thrift1b_admin=gs,thrift1b_cashier=gs,thrift1b_officer=gs)

			tblCUSTOMER.objects.filter(branch=branch, status=1).update(ivb=gs)





			if 'glm' in request.POST: ######loan* for variable thrift******************
				glm=request.POST['glm']
				Userprofile.objects.filter(branch = branch).update(loan1b=1)
				tblapp.objects.filter(branch=branch).update(loan1b=1)

			else:
				Userprofile.objects.filter(branch = branch).update(loan1b=0)
				tblapp.objects.filter(branch=branch).update(loan1b=0)






			if 'mcc' in request.POST: ##################################Cooporative*********************************************
				mcc=request.POST['mcc']
				Userprofile.objects.filter(branch = branch).update(thrift3a=1)
				Userprofile.objects.filter(branch = branch, ceo=1).update(thrift3a_admin=1,thrift3a_cashier=1)
				tblapp.objects.filter(branch=branch).update(thrift3a=1)


			else:
				Userprofile.objects.filter(branch = branch).update(thrift3a=0)
				Userprofile.objects.filter(branch = branch, ceo=1).update(thrift3a_admin=0,thrift3a_cashier=0)
				tblapp.objects.filter(branch=branch).update(thrift3a=0)









			if 'mcp' in request.POST: ##################################Corporate C*********************************************
				mcp=request.POST['mcp']
			else:
				mcp = 0

			tblapp.objects.filter(branch=branch).update(thrift3b=mcp)
			Userprofile.objects.filter(branch = branch).update(thrift3b=mcp)

			Userprofile.objects.filter(branch = branch, ceo=1).update(thrift3b_admin=mcp,thrift3b_cashier=mcp,thrift3b_officer=mcp)


			ceo = Userprofile.objects.get(branch = branch, ceo=1)

			ceo_staff= ceo.staffrec.id
			ceo_staff=tblSTAFF.objects.get(id=ceo_staff)
			sdr = tblIIIbcoop.objects.filter(branch=branch, staff=ceo_staff).count()

			pin = generate_pin()

			# if sdr < 1 :
			# 	tblIIIbcoop(branch=branch, cooperators_code=pin, staff= ceo_staff ,status=1,thrift3b=mcp).save()


			# tblIIIbcoop.objects.filter(branch=branch).update(thrift3b=mcp)


			neww = tblapp.objects.get(branch=branch)

			if oldd.thrift1a == 0 :
				if neww.thrift1a == 1 :
					msg1 = 'Thrift1a'
					sub.append(msg1)
			else :
				if neww.thrift1a == 0 :
					msg1 = 'Thrift1a'
					unsub.append(msg1)


			if oldd.thrift1b == 0 :
				if neww.thrift1b == 1 :
					msg1 = 'Thrift1b'
					sub.append(msg1)
			else :
				if neww.thrift1b == 0 :
					msg1 = 'Thrift1b'
					unsub.append(msg1)



			if oldd.loan1b == 0 :
				if neww.loan1b == 1 :
					msg1 = 'Loan1b'
					sub.append(msg1)
			else :
				if neww.loan1b == 0 :
					msg1 = 'Loan1b'
					unsub.append(msg1)



			if oldd.thrift3a == 0 :
				if neww.thrift3a == 1:
					msg1 = 'Thrift3a'
					sub.append(msg1)
			else :
				if neww.thrift3a == 0 :
					msg1 = 'Thrift3a'
					unsub.append(msg1)

			if oldd.thrift3b == 0 :
				if neww.thrift3b == 1 :
					msg1 = 'Thrift3b'
					sub.append(msg1)
			else :
				if neww.thrift3b == 0 :
					msg1 = 'Thrift3b'
					unsub.append(msg1)



			return render(request,'partner/app_update_success.html',{'company':branch,
				'user':varuser,
				'unsub':unsub,
				'comp':branch,
				'sub':sub})

	else:
		return HttpResponseRedirect('/login/user/')


def subscription(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')


		if request.method == 'POST':
			form = companyform(request.POST)

			if form.is_valid():
				companygg= form.cleaned_data['company']

			try:
				k = tblCOMPANY.objects.get(id =companygg,partner=partnerfff)

			except :
				msg = 'Details not found'
				return render(request,'partner/selectloan.html',{'msg':msg})


			br = tblBRANCH.objects.get(company=k)
			sub_history = tblsubscription.objects.filter(branch=br)
			return render(request,'partner/subscription_detail.html',{'company':mybranch,
				'user':varuser,
				'comp':br,
				'history':sub_history,
				'form':form})

		else:
			form = companyform()
			msg=''

			return render(request,'partner/subscription.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def package(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				user = post['userid']
				app,pack,business=user.split(':')

				if app == '':
					msg = 'select desired app'
					return render(request,'Ib/selectloan.html',{'msg':msg})
				if pack == '-----':
					msg = 'select subscription package'

					return render(request,'Ib/selectloan.html',{'msg':msg})

	 #            elif user == 'Trial':

				else:
					return render(request,'partner/package.html',{'package':pack,'business':business,'app':app})

			else:
				return HttpResponseRedirect('/vts/thrift/reports/sales/admn/')
		else:
			return render(request,'Ib/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')



def paid(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		# mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		partnerfff=tblPARTNER.objects.get(email=varuser)

		toofy = date.today()
		pd = str(toofy)
		y,m,d=pd.split('-')
		y=int(y)
		m=int(m)
		d=int(d)


		if staff.partner==0:
			return render(request,'partner/404.html')


		if request.method == 'POST':
			business=request.POST['business'] #unicode
			package=request.POST['package'] #unicode
			duration=request.POST['duration'] #unicode
			app=request.POST['app'] #unicode

			# msg =  packy	eturn render('Ib/selectloan.html',{'msg':msg})


			if duration == '-----':
				msg =  'select duration'
				return render(request,'Ib/selectloan.html',{'msg':msg})

			duration=int(duration)

			mybranch= tblBRANCH.objects.get(id=business)

			pk=tblthriftpackages.objects.get(appendage=package, status=True)



			sub_history = tblsubscription.objects.filter(branch=mybranch)# customer_branch)



			uy= [x.id for x in sub_history]
			sub_history=sub_history.get(id=uy[-1])



			if sub_history.status== 'Running':
				start = sub_history.end

				if monthrange(start.year, start.month)[-1] == start.day: #if end of month

					if start.month == 12:
						start = date(start.year+1, 1,1)
					else:
						start = date(start.year, start.month, start.day+ 1)

				else:
					start = date(start.year, start.month, start.day+1) #date constructor


				status= 'Queing'

			elif sub_history.status == 'Expired':

				start = date.today()

				status= 'Running'


			code = generate_pin()


			end = start.month + int(duration)

			if end > 12:
				kj= end - 12
				km =monthrange(start.year+1, kj)[-1]

				if km >=start.day+1 :
					end=date(start.year+1, kj, start.day)
				else:
					end=date(start.year+1, kj, start.day-1)
			else:
				kj= end
				end=date(start.year, kj, start.day)


			tblsubscription(status= status,
				branch=mybranch,
				receipt=code,
				duration=duration,
				package=pk,
				start=start,
				app=app,
				amount=pk.cost,
				end=end).save()


			return render(request,'partner/reg_sussess.html')


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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')


		if request.method == 'POST':
			code = request.POST['code']
			try:
				fg=tblsubpending.objects.get(receipt=code)
				owner=Userprofile.objects.get(branch=fg.branch.id,ceo=1)

				return render(request,'partner/extend_details.html',{'company':mybranch,
					'user':varuser,
					'owner':owner,
					'fg':fg})

			except:
				msg='INVALID CODE'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return render(request,'partner/extend.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def chckoutextw(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')

		if request.method == 'POST':

			code = request.POST['mycode']
			vb= tblsubpending.objects.filter(receipt=code)
			vbc=vb.count()

			if vbc==1:
				vb=vb.get(receipt=code)
				duration=vb.duration
				appendage=vb.package.appendage
				package=tblthriftpackages.objects.get(appendage=appendage)

				customer_branch = vb.branch.id
				customer_branch=tblBRANCH.objects.get(id=customer_branch)

				customer_comp=tblBRANCH.objects.get(id=customer_branch.id)


				sub_history = tblsubscription.objects.filter(branch=customer_branch)



				uy= [x.id for x in sub_history]
				sub_history=sub_history.get(id=uy[-1])

				start = sub_history.end
				day_range = (monthrange(start.year, start.month))[-1]



				if sub_history.status== 'Running':
					# start = sub_history.end

					if start.month == 12:
						start = date(start.year+1, 1,1)
					else:
						ddy = start.day

						# day_range = (monthrange(start.year, start.month))[-1]

						if ddy == day_range :
							start = date(start.year,start.month+1,1)
						else:
							start = date(start.year, start.month, ddy+1)

					status= 'Queing'

				elif sub_history.status == 'Expired':

					start = date.today()

					status= 'Running'



				elif sub_history.status== 'Queing':
					# start = sub_history.end

					if start.month == 12:
						start = date(start.year+1, 1,1)
					else:
						ddy = start.day

						# day_range = (monthrange(start.year, start.month))[-1]

						if ddy == day_range :
							start = date(start.year,start.month+1,1)
						else:
							start = date(start.year, start.month, ddy+1)

					status= 'Queing'


				else:
					return HttpResponseRedirect('/partner/partner/business/extension/')


				vb.delete()

				end = start.month + int(duration)

				if end > 12:
					kj= end - 12
					km =monthrange(start.year+1, kj)[-1]

					if km >=start.day+1 :
						end=date(start.year+1, kj, start.day)
					else:
						end=date(start.year+1, kj, start.day-1)
				else:
					kj= end
					end=date(start.year, kj, start.day)


				tblsubscription(status= status,
					branch=customer_branch,
					receipt=code,
					duration=duration,
					package=package,
					start=start,
					app='DC',
					amount=vb.amount,
					end=end).save()



				return render(request,'partner/ext_success.html',{'company':customer_comp,'user':varuser,'duration':duration})

			else:
				return HttpResponseRedirect('/partner/partner/business/extension/')


	else:
		return HttpResponseRedirect('/login/user/')




def chckoutext_ori(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')

		if request.method == 'POST':

			code = request.POST['mycode']
			vb= tblsubpending.objects.filter(receipt=code)
			vbc=vb.count()

			if vbc==1:
				vb=vb.get(receipt=code)
				duration=vb.duration
				package= vb.package.package
				app = vb.app
				package=tblthriftpackages.objects.get(package = package )


				customer_branch = vb.branch.id
				customer_branch=tblBRANCH.objects.get(id=customer_branch)


				sub_history = tblsubscription.objects.filter(branch=customer_branch)


				sub_history = tblsubscription.objects.filter(branch=customer_branch,app =app)

				uy= [x.id for x in sub_history]
				sub_history=sub_history.get(id=uy[-1])

				focals = sub_history.end
				today=focals.day
				next_day = today +	1
				start_month = focals.month
				start_year = focals.year

				day_range = (monthrange(start_year, start_month))[-1]

				if sub_history.status == 'Expired':

					start = date.today()
					today = start.day
					start_month=start.month
					start_year=start.year
					next_day=today + 1
					status= 'Running'

				else:#running or queing

					if next_day > day_range:
						next_day = 1
						start_month = start_month +1

					if start_month > 12:
						start_month = start_month - 12
						start_year = start_year + 1

					start = date(start_year,start_month,next_day)

					status= 'Queing'

				vb.delete()


				end_month = start_month + int(duration)
				prev_day = today -1


				if end_month > 12:
					end_month= end_month - 12
					end_year = start_year + 1

				km =monthrange(end_year, end_month)[-1]



				if prev_day > km :
					prev_day = km

				end=date(end_year, end_month,prev_day)


				# msg = focals,start, end
				# msg = prev_day,km



				tblsubscription(status= status,
					branch=customer_branch,
					receipt=code,
					duration=duration,
					package=package,
					start=start,
					app=app,
					amount=vb.amount,
					end=end).save()



				return render(request,'partner/ext_success.html',{'company':customer_branch,'user':varuser,'duration':duration})

			else:
				return HttpResponseRedirect('/partner/partner/business/extension/')

		else:
			return HttpResponseRedirect('/partner/partner/business/extension/')
	else:
		return HttpResponseRedirect('/login/user/')



def chckoutext(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')

		if request.method == 'POST':

			code = request.POST['mycode']
			vb= tblsubpending.objects.filter(receipt=code)
			vbc=vb.count()

			if vbc==1:
				vb=vb.get(receipt=code)
				duration=vb.duration
				package= vb.package.package
				app = vb.app
				package=tblthriftpackages.objects.get(package = package )


				customer_branch = vb.branch.id
				customer_branch=tblBRANCH.objects.get(id=customer_branch)


				sub_history = tblsubscription.objects.filter(branch=customer_branch)

				sub_history = tblsubscription.objects.filter(branch=customer_branch,app =app)

				uy= [x.id for x in sub_history]
				sub_history=sub_history.get(id=uy[-1])

				focals = sub_history.end
				start_day=focals.day
				next_day = start_day +	1
				start_month = focals.month
				start_year = focals.year

				day_range_start = (monthrange(start_year, start_month))[-1]

				if sub_history.status == 'Expired':
					start = date.today()
					start_day = start.day
					start_month=start.month
					start_year=start.year
					next_day=start.day
					status= 'Running'


				else:#running or queing

					status= 'Queing'
					start_day=next_day

				vb.delete()


				if next_day > day_range_start:
					next_day = 1
					start_month=start_month + 1
					if start_month > 12:
						start_month = start_month -  12
						start_year=start_year + 1

				start = date(start_year,start_month,next_day)



				end_month = start_month + int(duration)

				if end_month > 12:
					end_month= end_month - 12
					end_year = start_year + 1
				else:
					end_year=start_year


				prev_day= start_day - int(duration)
				if prev_day == 0:
					prev_day = monthrange(end_year, end_month)[-1]


				end=date(end_year, end_month,prev_day)



				tblsubscription(status= status,
					branch=customer_branch,
					receipt=code,
					duration=duration,
					package=package,
					start=start,
					app=app,
					amount=vb.amount,
					end=end).save()



				return render(request,'partner/ext_success.html',{'company':customer_branch,'user':varuser,'duration':duration})

			else:
				return HttpResponseRedirect('/partner/partner/business/extension/')

		else:
			return HttpResponseRedirect('/partner/partner/business/extension/')
	else:
		return HttpResponseRedirect('/login/user/')



def renew(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')


		if request.method == 'POST':
			form = companyform(request.POST)

			if form.is_valid():
				companygg= form.cleaned_data['company']

			try:
				k = tblCOMPANY.objects.get(id =companygg,partner=partnerfff)

			except :

				return HttpResponseRedirect('/dashboard/')


			br = tblBRANCH.objects.get(company=k)
			sub_history = tblsubscription.objects.filter(branch=companygg)
			return render(request,'partner/renew_detail.html',{'company':mybranch,
				'user':varuser,
				'comp':br,
				'history':sub_history,
				'form':form})

		else:
			form = companyform()
			msg=''

			return render(request,'partner/renew.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')




def manageall(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)

		if staff.partner==0:
			return render(request,'partner/404.html')


		if request.method=='POST':
			receipt=request.POST['receipt']
			extend=request.POST['extend']

			ddate = date.today()

			v= tblsubscription.objects.get(receipt=receipt)

			ddt = v.end


			if v.status == 'Running': #use end date (ddt)


				p = (monthrange(ddt.year, ddt.month))[-1]

				additional= int(extend) + int(ddt.day)


				if additional <= p:
					ddd=date(ddt.year,ddt.month, additional)

				else:

					additional =  additional - p

					if ddt.month == 12:
						ddd=date((ddt.year +1 ),1, additional)
					else:
						ddd=date(ddt.year, (ddt.month + 1), additional)



			elif v.status == 'Expired': #use todays date (ddate)


				p = (monthrange(ddate.year, ddate.month))[-1]

				additional= int(extend) + int(ddate.day)


				if additional <= p:
					ddd=date(ddate.year,ddate.month, additional)

				else:

					additional =  additional - p

					if ddt.month == 12:
						ddd=date((ddate.year +1 ),1, additional)
					else:
						ddd=date(ddate.year, (ddate.month + 1), additional)




			v.end=ddd
			v.save()

			if ddd >= ddate:
				v.status='Running'

			else:
				v.status='Expired'

			v.save()




		return render(request,'partner/manage.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def manageajax(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if  "userid" in request.session:
			varuser=request.session['userid']
			staff=Userprofile.objects.get(email=varuser, status=1)
			staffdet=staff.staffrec.id
			branch=staff.branch.id
			mycompany=staff.branch.company
			company=mycompany.name
			comp_code=mycompany.id
			ourcompay=tblCOMPANY.objects.get(id=comp_code)
			mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
			partnerfff=tblPARTNER.objects.get(email=varuser)



			if request.method == 'POST':
				post = request.POST.copy()
				status = post['userid']


				if  status == '-----':
					msg = 'Select status from the list'
					return render(request,'partner/selectloan.html',{'msg':msg})


				if staff.partner==0:
					return render(request,'partner/404.html')


				details=[]

				t=tblCOMPANY.objects.all().exclude(id=1)
				for comp in t:
					branches= tblBRANCH.objects.filter(company=comp)
					for bra in branches:
						sub_history = tblsubscription.objects.filter(branch=bra)

						uy= [x.id for x in sub_history]



						try:
							sub_history=sub_history.get(id=uy[-1])

							if sub_history.status=='Running':
								if status == 'Running':
									details.append(sub_history)
							elif sub_history.status=='Expired':
								if status == 'Expired':
									details.append(sub_history)
						except:
							kk=0




				return render(request,'partner/manage1.html',{'company':details})

			else:
				return HttpResponseRedirect('/login/user/')

		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def datepop(request):
		if  "userid" in request.session:
			if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
				if request.method == 'POST':
					varuser = request.session['userid']
					varerr =""
					post = request.POST.copy()
					acccode = post['userid']

					getdetails = tblsubscription.objects.get(receipt= acccode)


					return render(request,'partner/datepop.html',{'branch':getdetails,'receipt':acccode})

				else:
					gdata = ""
					return render(request,'index.html',{'gdata':gdata})
			else:

				gdata = ""
				return render(request,'getlg.htm',{'gdata':gdata})
		else:
			return HttpResponseRedirect('/login/')



#### **** VAS ****************
def vas(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')


		if request.method == 'POST':
			email = request.POST['email']
			amount = request.POST['amount']
			try:
				fg=tblSTAFF.objects.get(email=email)
				owner=Userprofile.objects.get(branch=fg.branch.id,ceo=1)

				return render(request,'partner/vas_details.html',{'company':mybranch,
					'user':varuser,
					'owner':owner,
					'amount':amount,
					'fg':fg})

			except:
				msg='INVALID EMAIl'
				return render(request,'Ia/selectloan.html',{'msg':msg})

		else:
			return render(request,'partner/vas.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def vasprocess(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render(request,'partner/404.html')

		if request.method == 'POST':

			amount = request.POST['amount']
			email = request.POST['email']


			fg=tblSTAFF.objects.get(email =email)
			customer_branch= fg.branch.id
			customer_branch=tblBRANCH.objects.get(id=customer_branch)

			owner=Userprofile.objects.get(branch=fg.branch.id,ceo=1)


			sms_trans_id = generate_pin()

			fdate= datetime.today()
			ddate = fdate.date()
			ttime= fdate.time()


			sms_trans  = tblsmstrans.objects.filter(branch=customer_branch)

			sms = tblsmsbuy.objects.filter(branch=customer_branch,	amount= amount,date=ddate)

			if sms.count() == 0:

				tblsmsbuy(branch=customer_branch,
					amount= amount,
					credited_status=False,
					sms_trans_id= sms_trans_id,
					date=ddate,	time=ttime).save()

			sms2 = sms.get(branch=customer_branch, amount=amount,date=ddate)

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


				tblsmstrans(branch=customer_branch,
					balance=balance,
					balance_before=balance_before,
					balance_after=balance_after,
					sms_trans_id= sms2.sms_trans_id,
					date=ddate,
					time=ttime).save()


				df = sms.get(sms_trans_id=sms2.sms_trans_id)
				df.credited_status=True
				df.save()
				msg = f'Your SMS purchase of {amount} was sucessfull'
			else:
				msg = 'you already purchased sms today'

			return render(request,'partner/vas_success.html',{'company':mybranch,'amount':amount,'msg':msg})

		else:
			return HttpResponseRedirect('/partner/partner/business/extension/')
	else:
		return HttpResponseRedirect('/login/user/')










