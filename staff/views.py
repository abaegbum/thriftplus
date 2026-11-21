import xlrd
import openpyxl
from django.contrib import messages



from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from staff.forms import *
from sysadmin.models import *
from staff.models import *
from datetime import date
import calendar







from staff.utils import *
from thriftplus.utils import *
from Ia.models import *
from IIIb.models import *

from django.db.models import Max,Sum
today=date.today()





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

		if staff.ceo==0 :
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})

		if staff.thrift3b==1:
			return render(request,'staff/3bwelcome.html',{'company':mybranch, 'user':varuser})
		else:
			return render(request,'staff/welcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/user/')


def newst(request):
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
			return render(request,'404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']


			if 'photo' in request.FILES:
				photo=request.FILES['photo']
			else:
				photo = 'staff-pix/user.png'

			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])
			try:
				phone=int(phone)
			except:
				return render(request,'staff/staffdet.html',{'company':mybranch, 'user':varuser})

			wallet=phone

			pin = generate_staff_pin()

			password = generate_password()


			countt=tblSTAFF.objects.filter(email=email) #whether active or not

			if countt.count() < 1 :

				tblSTAFF(surname=surname,
					firstname=firstname,
					othername=othername,
					status= True,
					phone=phone,
					ceo=0,
					Address=address,
					photo=photo,
					code=pin,
					email=email,
					branch=mybranch,
					types='Field').save()
			else:

				msg = f"this email is already registered with {branch} thank you"

							
			myuser = countt.get(branch=mybranch,email=email)

			uu =Userprofile.objects.filter(staffrec=myuser,email=email)

			if uu.count()<1:
				Userprofile(status= True,
					branch=mybranch,
					code=pin,
					ceo=0,
					staffrec=myuser,
					password=password,
					email=email).save()


			if staff.thrift3b==1:

				ff= tblIIIbcoop.objects.filter(branch=mybranch,staff=myuser)
				
				if ff.count() == 0:
					coop = tblIIIbcoop.objects.create(branch=mybranch,staff=myuser, cooperators_code=pin,status=1,thrift3b=1 )
				

				else:

					coop=ff.get()

				if not tblIIIbthrift.objects.filter(branch =mybranch,staff =coop).exists():
					tblIIIbthrift.objects.create(branch =mybranch,staff =coop,can_get_loan = False, can_buy_commodity = False)


				uu.update(thrift3b=1, thrift3b_officer=1)




						
				#send email to cooperator, informing them of their login details
				try:
					staff_registration(email,surname,password,firstname,mybranch)
				except:
					mn=0

				return render(request,'staff/success3b.html',{'company':mybranch,'user':varuser,'email':email})
			
			else:
				
				#send email to cooperator, informing them of their login details
				try:
					staff_registration(email,surname,password,firstname,mybranch)
				except:
					mn=0

				return render(request,'staff/success.html',{'company':mybranch,'user':varuser,'email':email})
			

		else:

			if staff.thrift3b==1:
				return render(request,'staff/membership.html',{'company':mybranch, 'user':varuser})

			return render(request,'staff/staffdet.html',{'company':mybranch, 'user':varuser})


	else:
		return HttpResponseRedirect('/login/user/')



def massReg(request):
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


		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.thrift1a:

			try:
				memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
			except:
				return render(request,'404cr.html',{'company':mybranch, 'user':varuser})

		msg = ''

		if request.method == 'POST':
			excel_file = request.FILES['excel']
			
			myusers=tblSTAFF.objects.filter(branch=mybranch)
			lg= Userprofile.objects.filter(branch=mybranch, status=1)

			address='lagos'

			photo = 'staff-pix/user.png'


	        # ✅ Ensure the file name is exactly "tac.xlsx"
			if excel_file.name != "tac.xlsx":
				messages.error(request, "Invalid file name. Please upload tac.xlsx only.")
				return redirect(massReg)

	        # ✅ Load the workbook
			wb = openpyxl.load_workbook(excel_file)
			sheet = wb.active  # first sheet


			# ✅ Validate that F1 is 'Email'
			header_e1 = str(sheet.cell(row=1, column=6).value).strip().lower()
			if header_e1 != "email":
				messages.error(request, "Invalid column name. Column F1 must be 'Email'")
				return redirect(massReg)

			for row in sheet.iter_rows(min_row=2, values_only=True):
			    # Skip the first column (S/N) and take the next 5
			    surname, firstname, othername, phone, email = row[1:6]

			    # Handle case where Othername is empty
			    if othername is None:
			        othername = ""   # or keep None if your model allows it

			    password = generate_password()
			    pin = generate_staff_pin()

			    # ✅ Avoid duplicate emails
			    if not tblSTAFF.objects.filter(email=email).exists():
			        tblSTAFF.objects.create(
			            branch=mybranch,
			            surname=surname,
			            firstname=firstname,
			            othername=othername,
			            email=email,
			            status=True,
			            phone=phone,
			            ceo=0,
			            Address=address,
			            photo=photo,
			            code=pin,
			            types='Field'
			        )

			    myuser = myusers.get(email=email)

			    if not Userprofile.objects.filter(email=email).exists():
			        Userprofile.objects.create(
			            status=True,
			            branch=mybranch,
			            code=pin,
			            ceo=0,
			            staffrec=myuser,
			            password=password,
			            email=email
			        )


			    lg.filter(email=email).update(thrift3b=1, thrift3b_officer=1)


			    if staff.thrift3b==1:
			    	ff= tblIIIbcoop.objects.filter(staff=myuser)

			    	if ff.count() == 0:
			    		coop = tblIIIbcoop.objects.create(branch=mybranch,
									staff=myuser,
									cooperators_code=pin,
									status=1,
									thrift3b=1 )

			    	else:
			    		coop=ff.get()



			    	if not tblIIIbthrift.objects.filter(branch =mybranch,staff =coop).exists():
			    		tblIIIbthrift.objects.create(branch =mybranch,staff =coop,can_get_loan = False, can_buy_commodity = False)


			    password = lg.get(email=email).password
			    business = mybranch.company.name


			    try:
			    	staff_registration(email,surname,password,firstname,mybranch)
			    except:
			    	mn=0



			messages.success(request, f"  Data uploaded successfully.")
			
			return redirect(massReg) #function redirect,name redirect,url redirect
			# return redirect('success_page')

			return render(request, 'upload.html')



			return render(request,'staff/success.html',{'company':mybranch,'user':varuser,'email':email})



		if staff.thrift3b==1:
			return render(request,'staff/massregthreeb.html',{'company':mybranch, 'user':varuser,'msg':msg})
		else:
			return render(request,'staff/massreg.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')






def regmerchant2(request): #from daily contr service
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

		if staff.ceo==0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})


		mystafflist = tblSTAFF.objects.filter(status=1, branch=mybranch).count()


		if request.method== 'POST':
			form = fieldofficerfform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']
				mystaff = tblSTAFF.objects.filter(email=email,status=1, branch=mybranch) #check status
				mycount=mystaff.count()

				if mycount == 1: #user is a staff
					querry_email = tblSTAFF.objects.get(email=email)

					try:
						ibco = tblMERCHANT.objects.get(branch = mybranch, thrift1a=1,staff=querry_email)
						if ibco.status == False:
							msg = 'credit officer is inactive'

						elif ibco.status == True:
							msg='ALREADY REGISTERED'

					except:
						diff = Userprofile.objects.get(email=email,status=1)
						diff.thrift_officer=1 #role
						diff.thrift1a=1 #app
						diff.save()
						form = fieldofficerfform()
						msg="SUCCESSFUL"

						try:
							sendMailCO_ON(email)
						except:
							pass


				elif mycount == 0:
					msg = 'THIS EMAIL IS NOT REGISTERED'
			else:
				msg = 'INVALID ENTRY'
		else:
			form =fieldofficerfform()
			msg=''

		meer = tblMERCHANT.objects.filter(branch=mybranch,thrift1a=1)
		mycolist = tblMERCHANT.objects.filter(status=1, thrift1a=1, branch=mybranch).count()
		inactiveco = tblMERCHANT.objects.filter(status=0, thrift1a=1, branch=mybranch).count()

		return render(request,'staff/merch.html',{'staffcount':mystafflist, 'ggg': mycolist,'company':mybranch,'msg':msg, 'user':varuser,'form':form,'merchant':meer})

	else:
		return HttpResponseRedirect('/login/user/')






def deactivate(request):
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

		if staff.ceo==0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			email= request.POST['email']

			mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email,status=1) #check status
			mycount=mystaff.count()

			if mycount == 1:
				querry_email = tblSTAFF.objects.get(email=email)

				try:
					ibco=Userprofile.objects.get(staffrec=querry_email,status=1)

					if ibco.ceo ==0 :
						ibco.status=0
						msg='Account Deactivated successfully!!!'
						ibco.save()

						try:
							sendMailCO_ON(email)

						except:
							m=9
					else:
						msg='Account cant be Deactivated'

				except:
					msg = 'this account is already inactive'

					# return render(request,'staff/selectloan.html',{'msg':msg})

				else:
					msg = 'Cant deactivate the account'
			else:
				msg = 'Invalid email'
		else:
			msg=''

		return render(request,'staff/merch.html',{'company':mybranch,'msg':msg, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')



def activate(request):
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
		msg=''

		if staff.ceo==0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			email= request.POST['email']

			mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email) #check status
			mycount=mystaff.count()

			if mycount == 1:
				querry_email = tblSTAFF.objects.get(email=email)

				try:
					ibco=Userprofile.objects.get(staffrec=querry_email,status=0)

					if ibco.ceo ==0 :
						ibco.status=1
						msg='Account Deactivated successfully!!!'
						ibco.save()

						try:
							sendMailCO_ON(email)

						except:
							m=9

					else:
						msg='Account cant be Deactivated'

				except:
					msg = 'this account is already active'

			else:
				msg = 'Invalid email'
		else:
			msg=''


		return render(request,'staff/activate.html',{'company':mybranch,'msg':msg, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')


def delete(request):
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

		if staff.ceo==0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})

		msg='This function has been depreciated'

		return render(request,'staff/delete.html',{'company':mybranch,'msg':msg, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/user/')



def resetuu(request):
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

		if staff.ceo==0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			form = staffform(request.POST)

			email=form.cleaned_data['email']
			mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email,status=1) #check status
			mycount=mystaff.count()

			if mycount == 1:
				querry_email = tblSTAFF.objects.get(email=email)
				pin = querry_email.code

				try:
					ibco = tblMERCHANT.objects.get(branch = mybranch, staff=querry_email)
					if ibco.thrift1b == 0:
						msg = 'nor efr'

					elif ibco.thrift1b == 1:
						msg='ALREADY REGISTERED'

				except:
					diff = Userprofile.objects.get(email=email,status=1)
					diff.thrift_officer=1
					diff.save()
					tblMERCHANT(branch = mybranch,code=pin, staff=querry_email,thrift1a=1).save()
					form = staffform()
					msg="SUCCESSFUL"
					try:
						sendMailCO_ON(email)
						tblMERCHANT(status=1,branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()
					except:
						tblMERCHANT(status=1, branch=mybranch,thrift1a=1, staff=querry_email,code=querry_email.code).save()

			else:
				msg = 'THIS EMAIL IS NOT REGISTERED OR STAFF IS INACTIVE'


		else:
			form = staffform()
			msg=''

		return render(request,'staff/reset.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/user/')

def reset(request):
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

		if staff.ceo==0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			# if form.is_valid():
			form = staffform(request.POST)
			email=request.POST['email']

			try:
				diff = Userprofile.objects.get(email=email,status=1)

			except:
				msg  = 'THIS EMAIL IS NOT REGISTERED OR STAFF IS INACTIVE'



			comp_pass = tbldefaultpass.objects.filter(branch=mybranch)
			if comp_pass.count() == 1:
				comp_pass= comp_pass.get(branch=mybranch)
				diff.password = comp_pass.password

			else:
				diff.password=='thrift'

			diff.save()
			msg="Password reset successful"


			try:
				sendMailCO_ON(email)
			except:
				pass


		else:
			msg=''

		form = staffform()
		return render(request,'staff/reset.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')





def tutorial(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.ceo==0:
			return render(request,'404.html',{'company':mybranch, 'user':varuser})

		return render(request,'staff/adminwelcome.html',{'company':mybranch, 'user':varuser})
		# pass
	else:
		return HttpResponseRedirect('/login/user/')


def roles(request):
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

		if staff.ceo==0:
			return render(request,'404.html',{'company':mybranch, 'user':varuser})

		# stafflist = Userprofile.objects.filter(branch=mybranch,status=1).order_by('staffrec__surname')
		mystafflist = Userprofile.objects.filter(branch=mybranch,status=1).order_by('staffrec__surname')
		
		if staff.thrift3b==1:

			return render(request,'staff/stafflist3b.html',{
				'company':mybranch,
				'user':varuser,
				'list':mystafflist})
		else:

			return render(request,'staff/stafflist.html',{
				'company':mybranch,
				'user':varuser,
				'list':mystafflist})

	else:
		return HttpResponseRedirect('/login/user/')




def listofstatt(request):
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

		if staff.ceo==0:
			return render(request,'404.html',{'company':mybranch, 'user':varuser})



		stafflist = tblSTAFF.objects.filter(branch=mybranch,status=1).exclude(email='njc@gmail.com')
		# stafflist = Userprofile.objects.filter(branch=mybranch,status=1).exclude(email='njc@gmail.com')
		# mystafflist=[]
		# for  k in stafflist:
		# 	name=k.staffrec.surname + "  " + k.staffrec.firstname +"  "+ k.staffrec.othername
		# 	ID = k.staffrec.id
		# 	s= {'name':name,'id':ID}
		# 	mystafflist.append(s)

		return render(request,'staff/listofstaff.html',{'company':mybranch, 'user':varuser,'list':stafflist})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def setroles(request):
	if  "userid" in request.session:
		if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				stafflist = tblSTAFF.objects.get(id = acccode)
				userlist = Userprofile.objects.get(staffrec=stafflist,status=1)
				branch_code = stafflist.branch.id

				appplist = tblapp.objects.get(branch=branch_code)

				myy=[]
				name = stafflist.surname.upper() + " " + stafflist.firstname.upper()# + " " + stafflist.othername.upper()

				if appplist.thrift3b:
					

	##########thrift IIIB *********************
					if userlist.thrift3b_admin is True:
						thrift3b_admin= 'checked'
					else:
						thrift3b_admin='unchecked'

					if userlist.thrift3b_cashier is True:
						thrift3b_officer='checked'
					else:
						thrift3b_officer='unchecked'

					s= {'name':name ,
						'thr3bad':thrift3b_admin,
						'thr3bo':thrift3b_officer,
						'app':appplist}



				elif appplist.thrift1a:

	#######thrifts IA********************
					if userlist.cashier is True:
						cashier= 'checked'
					else:
						cashier='unchecked'

					if userlist.admin is True:
						admin='checked'
					else:
						admin='unchecked'


	#######thrifts IB********************
					if userlist.thrift1b_cashier is True:
						thrift1bcashier= 'checked'
					else:
						thrift1bcashier='unchecked'

					if userlist.thrift1b_admin is True:
						thrift1badmin='checked'
					else:
						thrift1badmin='unchecked'

	#############loan IB*******************
					if userlist.loan1b_officer is True:
						loan1b_officer= 'checked'
					else:
						loan1b_officer='unchecked'

					if userlist.loan1b_admin is True:
						loan1b_admin='checked'
					else:
						loan1b_admin='unchecked'

	##########thrift IIIA *********************
					if userlist.thrift3a_admin is True:
						thrift3a_admin= 'checked'
					else:
						thrift3a_admin='unchecked'

					if userlist.thrift3a_cashier is True:
						thrift3a_officer='checked'
					else:
						thrift3a_officer='unchecked'



	#############loan IIIB*******************
					if userlist.loan3b_officer is True:
						loan3b_officer= 'checked'
					else:
						loan3b_officer='unchecked'

					if userlist.loan3b_admin is True:
						loan3b_admin='checked'
					else:
						loan3b_admin='unchecked'

	####coop*****************

					s= {'name':name ,
					'cash':cashier,'adm':admin,
					'thr1bc':thrift1bcashier,'thr1bad':thrift1badmin,
					'loan1bo':loan1b_officer,'loan1ba':loan1b_admin,
					'thr3aad':thrift3a_admin,'thr3ao':thrift3a_officer,
					'thr3bad':thrift3b_admin,'thr3bo':thrift3b_officer,
					'loan3ba':loan3b_admin , 'loan3bo':loan3b_officer,
					'app':appplist}



				myy.append(s)
				return render(request,'staff/staffroles.html',{'list':myy,'ID':acccode})
			else:
				gdata = ""
				return render(request,'index.html',{'gdata':gdata})
		else:
			gdata = ""
			return render(request,'getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/user/')



def updaterole(request,vid):
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

		if staff.ceo==0:
			return render(request,'404.html',{'company':mybranch, 'user':varuser})

		thestaff = tblSTAFF.objects.get(id=vid)

		appplist = tblapp.objects.get(branch=mybranch)

		if appplist.thrift3b:
			k=0

### thrift IIIB**************************


			updates = {
			    "thrift3b_cashier": 'thr3bc' in request.POST,
			    "thrift3b_admin": 'thr3bad' in request.POST,
			}

			Userprofile.objects.filter(staffrec=thestaff).update(**updates)



		elif appplist.thrift1a:
			
	 #Thrift IA*********************
			if 'mycashier' in request.POST:
				cashier=request.POST['mycashier']
				Userprofile.objects.filter(staffrec= thestaff).update(cashier=cashier)
			else:
				Userprofile.objects.filter(staffrec= thestaff).update(cashier=0)


			if 'myadmin' in request.POST:
				admin=request.POST['myadmin']
				Userprofile.objects.filter(staffrec= thestaff).update(admin=1)
			else:
				Userprofile.objects.filter(staffrec= thestaff).update(admin=0)


	#thrift IB************************

			if 'thr1bc' in request.POST:
				ao=request.POST['thr1bc']

			else:
				ao =0

			Userprofile.objects.filter(staffrec= thestaff).update(thrift1b_cashier=ao)

			if 'thr1bad' in request.POST:
				sa=request.POST['thr1bad']

			else:
				sa =0

			Userprofile.objects.filter(staffrec= thestaff).update(thrift1b_admin=sa)


	###loan IB**************************
			if 'loan1bcashier' in request.POST:
				lc=request.POST['loancashier']
				Userprofile.objects.filter(staffrec= thestaff).update(loan1b_officer=lc)
			else:
				Userprofile.objects.filter(staffrec= thestaff).update(loan1b_officer=0)

			if 'loan1badmin' in request.POST:
				la=request.POST['loanadmin']
				Userprofile.objects.filter(staffrec= thestaff).update(loan1b_admin=la)
			else:
				Userprofile.objects.filter(staffrec= thestaff).update(loan1b_admin=0)

	### thrift IIIA**************************

			if 'thr3ac' in request.POST:
				co=request.POST['thr3ac']
				Userprofile.objects.filter(staffrec= thestaff).update(thrift3a_cashier=co)
			else:
				Userprofile.objects.filter(staffrec= thestaff).update(thrift3a_cashier=0)

			if 'thr3aad' in request.POST:
				ca=request.POST['thr3aad']
				Userprofile.objects.filter(staffrec= thestaff).update(thrift3a_admin=ca)
			else:
				Userprofile.objects.filter(staffrec= thestaff).update(thrift3a_admin=0)







		return HttpResponseRedirect('/staff/staff/roleplay/')

	else:
		return HttpResponseRedirect('/login/user/')

def viewdetail(request):
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

		if staff.ceo==0:
			return render(request,'404.html',{'company':mybranch, 'user':varuser})

		if request.method=='POST':
			form = staffform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']

				mystaff = tblSTAFF.objects.filter(branch=mybranch, email=email,status=1) #check status
				mycount=mystaff.count()

				if mycount == 1:
					msg= ''
					querry_email = tblSTAFF.objects.get(email=email)

					return render(request,'staff/myprofile.html',{'company':mybranch,
						'details':querry_email,
						'user':varuser,'form':form})

				else:
					msg = 'THIS EMAIL IS NOT REGISTERED'
			else:
				msg = 'INVALID ENTRY'
		else:
			form = staffform()
			msg=''
		if staff.thrift3b==1:
			return render(request,'staff/profdetail3b.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})
		else:
			return render(request,'staff/profdetail.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/user/')






####CREDIT OFFICERS****************
def regfieldagent(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1, thrift1a=1)
		except:
			return render(request,'staff/404.html')


		staffdet=staff.staffrec.id
		branch_code=staff.branch.code
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,code=branch_code)

		if staff.ceo==0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})


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

						return render(request,'staff/credit_activate_post.html',{
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
								return render(request,'staff/selectloan2.html',{'company':mybranch,'msg':msg})

							else:

								if int(gh_count) < int(history['staff_count']):
									form =fieldofficerfform()
									msg=''


									return render(request,'staff/actCO2.html',{
										'company':mybranch,
										'id':mybranch.id,
										'msg':querry_email,
										'products':g,
										'user':varuser})


								else:
									msg= 'You have reached the maximum number of credit officer(s) allowed for your package'
									return render(request,'staff/selectloan2.html',{'company':mybranch,'msg':msg})

						else:
							msg = 'you cannot proceed beyond this point, until you do something about your subscription'
							return render(request,'staff/selectloan2.html',{'company':mybranch,'msg':msg})



				elif mycount == 0:
					msg = 'THIS EMAIL IS NOT REGISTERED'
					return render(request,'staff/selectloan2.html',{'company':mybranch,'msg':msg})
			else:
				return HttpResponseRedirect('/staff/staff/merchant/')
				msg = 'INVALID ENTRY'



		else:

			form =fieldofficerfform()

			return render(request,'staff/credit_activate_get.html',{
					'company':mybranch,
					'user':varuser,
					'form':form})

	else:
		return HttpResponseRedirect('/login/user/')



def services_update(request):

	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)

		staffdet=staff.staffrec.id
		branch_code=staff.branch.code
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,code=branch_code)






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

			return render(request,'staff/credit_activate_post2.html',{
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
			return render(request,'staff/404.html')

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



		return render(request,'staff/credit_manage_get.html',
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


			return render(request,'staff/credit_manage_name_pop.html',{
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
			return render(request,'staff/404.html')


		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompany=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompany,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if staff.admin==0 :
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})



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

			return HttpResponseRedirect('/staff/staff/merchant/manage/')


		else:
			return HttpResponseRedirect('/staff/staff/merchant/manage/')
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


			return render(request,'staff/credit_manage_loc_pop.html',{'merchant':mn,'loc':mp})
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

			return HttpResponseRedirect('/staff/staff/merchant/manage/')
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
			return render(request,'staff/404.html')
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.admin==0:
			return render(request,'staff/404.html',{'company':mybranch, 'user':varuser})


		msg = ''

		meer = tblIaMERCHANT.objects.filter(branch=mybranch,thrift1a=1,status=1).order_by('status')

		if staff.admin == 1:
			return render(request,'staff/credit_myco.html',{'company':mybranch,'msg':msg, 'user':varuser,'merchant':meer})


		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')



