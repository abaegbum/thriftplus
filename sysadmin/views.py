from django.shortcuts import render
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt




# from . import utils   # from sysadmin.utils import * 
from . import models   # from sysadmin.models import *


from customer.models import *
from Ia.utils import * 
 


# def index(request):
# 	if request.method=='POST':
# 		email=request.POST['email']
# 		password=request.POST['password']
		
					
# 		user=Userprofile.objects.filter(email=email,password=password,status=1)
# 		if user.count() ==1:
# 			user=user.get()
# 			request.session['userid'] = user.email
# 			varuser = request.session['userid']
# 			return  HttpResponseRedirect('/dashboard/')

# 		else:

# 			cc = tblCUSTOMER.objects.filter(wallet=email,status=1,phone=password)
# 			if cc.count==1:
# 				cc=cc.get()
# 				request.session['userid'] = email
# 				varuser = request.session['userid']
# 				return  HttpResponseRedirect('/home/')


# 		msg='Invalid login details'
# 		return render(request,'login.html',{'varerr':msg})


# 	else:
# 		new_fresh()
		
# 		return render(request,'index.html')






# Wrapper to make a view handle both normal and api request
def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), content_type="application/json")

    return wrap



def tutorial2(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/user/')



def setuppas(request):
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
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			password=request.POST['password']

			tbldefaultpass(branch=mybranch,password=password).save()

			return render(request,'sysadmin/pas.html',{'company':mybranch,
				'user':varuser,
				'comp':mybranch})



		else:

	
			sub_history = tbldefaultpass.objects.filter(branch=mybranch)
			if sub_history.count() ==1:
				sub_history =sub_history.get(branch=mybranch)
			else:
				sub_history=[]


			return render(request,'sysadmin/mypass.html',{'company':mybranch,
				'user':varuser,
				'comp':mybranch,
				'history':sub_history})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def passpop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']

    		try:
	    		mycom = tbldefaultpass.objects.get(branch=acccode) 

	    		return render(request,'sysadmin/app_trans.html',{'income':mycom})

	    	except :
	    		msg='error !!!'
	    		return render(request,'Ia/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def changpasspop(request):
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
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		

		if request.method=='POST': 
			branch1= request.POST['branch']
			pass1=request.POST['pass1']
			pass2=request.POST['pass2']

			if pass2 != "":


				if int(branch)==int(branch1):
					if pass1 == pass2:
						f=tbldefaultpass.objects.get(branch=mybranch)
						f.password=pass1
						f.save()
						return render(request,'sysadmin/passchangesuccess.html',{'company':mybranch, 'user':varuser})
					else:
						return HttpResponseRedirect('/sysadmin/sysadmin/setup/password/')

				else:
					return HttpResponseRedirect('/login/user/')
			else:
				return HttpResponseRedirect('/sysadmin/sysadmin/setup/password/')

		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')



def location(request):
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
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			loc=request.POST['loc']
			loc=loc.lower()

			try:
				t= tblbusinesslocations.objects.get(branch=mybranch,location=loc)
				msg = 'location already exists'
			except:
				code=generate_trans_pin()
				tblbusinesslocations(branch=mybranch,location=loc,code=code).save()
				msg = 'Location saved successfullly'
		else:
			msg = ''



		allloc = tblbusinesslocations.objects.filter(branch=mybranch)


		return render(request,'sysadmin/myloc.html',{'company':mybranch,
			'user':varuser,
			'msg':msg,
			'history':allloc,
			'comp':mybranch})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def delloc(request):
	if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
		if request.method == 'POST':
			post = request.POST.copy()
			acccode = post['userid']

			mycom = tblbusinesslocations.objects.get(code=acccode)

			df= tblIalocations.objects.filter(location=mycom.location)

			if df.count() == 0:
				return render(request,'sysadmin/deleloc.html',{'income':mycom})
			else:
				msg = 'dg'
				return render(request,'sysadmin/deleloc2.html',{'income':mycom})

		else:
			return HttpResponseRedirect('/login/user/')
	else:
		return HttpResponseRedirect('/login/user/')


def dellocyes(request,vid):
	if 'userid' in request.session:
		user=request.session['userid']

		staff=Userprofile.objects.get(email=user, status=1)
		branch=staff.branch.id
		mybranch=tblBRANCH.objects.get(id=branch)

		# tbliaM

		k = tblbusinesslocations.objects.filter(branch =mybranch)
		ss=k.get(code=vid)
		loc=str(ss.location)
		ss.delete()
		msg='{} deleted successfullly'.format(loc)


		# return render(request,'sysadmin/myloc.html',{'company':mybranch,
		# 	'user':user,
		# 	'msg':msg,
		# 	'history':k,
		# 	'comp':mybranch})

		return HttpResponseRedirect('/sysadmin/sysadmin/setup/locations/')

	else:
		return HttpResponseRedirect('/login/user/')



def carding(request):
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
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			fresh=request.POST['fresh']
			replace=request.POST['replace']

			try:
				tblcarding.objects.get(branch=mybranch)
			except:

				tblcarding(branch=mybranch,fresh=fresh,reissue=replace).save()

			return render(request,'sysadmin/cardsus.html',{'company':mybranch,
				'user':varuser,
				'comp':mybranch})



		else:

	
			sub_history = tblcarding.objects.filter(branch=mybranch)
			if sub_history.count() ==1:
				sub_history =sub_history.get(branch=mybranch)
				return render(request,'sysadmin/mycards.html',{'company':mybranch,
					'user':varuser,
					'comp':mybranch,
					'history':sub_history})

			elif sub_history.count()==0:
				return render(request,'sysadmin/mycards.html',{'company':mybranch,
					'user':varuser,
					'comp':mybranch,
					'history':sub_history})
			else:
				msg = 'error'


				return render(request,'Ia/selectloan.html',{'company':mybranch,
					'user':varuser,
					'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def freshpop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']

    		try:
	    		mycom = tblcarding.objects.get(branch=acccode) 

	    		return render(request,'sysadmin/freshchange.html',{'income':mycom})

	    	except :
	    		msg='error !!!'
	    		return render(request,'Ia/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def savefreshpop(request):
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
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		

		if request.method=='POST': 
			branch1= request.POST['branch']
			fresh1=request.POST['fresh1']


			if int(branch)==int(branch1):
				f=tblcarding.objects.get(branch=mybranch)
				f.fresh=fresh1
				f.save()
			
				return render(request,'sysadmin/mycards.html',{'company':mybranch,
					'user':varuser,
					'comp':mybranch,
					'history':f})


			else:
				return HttpResponseRedirect('/sysadmin/sysadmin/setup/carding/')


		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')



@csrf_exempt
def repop(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']

    		try:
	    		mycom = tblcarding.objects.get(branch=acccode) 

	    		return render(request,'sysadmin/reissuepop.html',{'income':mycom})

	    	except :
	    		msg='error !!!'
	    		return render(request,'Ia/selectloan.html',{'msg':msg})

    	else:
    		return HttpResponseRedirect('/login/user/')
    else:
    	return HttpResponseRedirect('/login/user/')



def saverepop(request):
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
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})
		

		if request.method=='POST': 
			branch1= request.POST['branch']
			fresh1=request.POST['fresh1']


			if int(branch)==int(branch1):
				f=tblcarding.objects.get(branch=mybranch)
				f.reissue=fresh1
				f.save()
			
				return render(request,'sysadmin/mycards.html',{'company':mybranch,
					'user':varuser,
					'comp':mybranch,
					'history':f})


			else:
				return HttpResponseRedirect('/sysadmin/sysadmin/setup/carding/')


		else:
			return HttpResponseRedirect('/login/user/')

	else:
		return HttpResponseRedirect('/login/user/')



def myproduct(request):
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
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			esusu=request.POST['esusu']
			general=request.POST['general']

			mycom = tblmyproducts.objects.get(product='Esusu')
			cv=tblproductsname(branch=mybranch,product=mycom, your_product_name=esusu).save()



			mycom = tblmyproducts.objects.get(product='Savings')
			cv=tblproductsname(branch=mybranch,product=mycom,your_product_name=general).save()



			return render(request,'sysadmin/myproducts_post.html',{'company':mybranch,
				'user':varuser,
				'comp':mybranch})



		else:
			sub_history = tblproductsname.objects.filter(branch=mybranch)

			gh=[]

			app = tblapp.objects.get(branch=mybranch)
			if app.esusu1a==1:
				esusu=1
			else:
				esusu=0

			ppp= tblmyproducts.objects.get(product='Esusu')


			sub_history_esusu=sub_history.filter(product=ppp)

			if sub_history_esusu.count() ==1:
				sub_history_esusu=sub_history_esusu.get()

			else:

				sub_history_esusu = 0
			
			esu= {'App_name':'Esusu','App_status':esusu, 'App_label':sub_history_esusu}
			gh.append(esu)


			if app.savings1a==1:
				savings =1
			else:
				savings=0


			ppp= tblmyproducts.objects.get(product='Savings')


			sub_history_savings=sub_history.filter(product=ppp)

			if sub_history_savings.count() ==1:
				sub_history_savings=sub_history_esusu.get()
			else:
				sub_history_savings = 0
			
		

			sav= {'App_name':'General Savings','App_status':savings, 'App_label':sub_history_savings}
			gh.append(sav)

			



			if sub_history.count() <=2:				

				return render(request,'sysadmin/myproducts.html',{'company':mybranch,
					'user':varuser,
					'comp':mybranch,
					'history':sub_history,
					'gh':gh})

			else:
				msg = 'error'


				return render(request,'Ia/selectloan.html',{'company':mybranch,
					'user':varuser,
					'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



def myproduct(request):
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
			return render(request,'Ia/404.html',{'company':mybranch, 'user':varuser})


		if request.method=='POST':
			for key,value in request.POST.items():
				if key.startswith('entry_'):
					appname = key.split('_')[1]
					mycom = tblmyproducts.objects.get(product=appname)
					cv=tblproductsname.objects.filter(branch=mybranch,product=mycom)
					if cv.count() == 1:
						cv=cv.get()
						cv.your_product_name=value
						cv.save()
					else:
						tblproductsname(branch=mybranch,product=mycom, your_product_name=value).save()

			return render(request,'sysadmin/myproducts_post.html',{'company':mybranch,
				'user':varuser,
				'comp':mybranch})



		else:
			sub_history = tblproductsname.objects.filter(branch=mybranch)

			gh=[]

			app = tblapp.objects.get(branch=mybranch)
			if app.esusu1a==1:
				esusu=1
			else:
				esusu=0

			ppp= tblmyproducts.objects.get(product='Esusu')


			sub_history_esusu=sub_history.filter(product=ppp)

			if sub_history_esusu.count() ==1:
				sub_history_esusu=sub_history_esusu.get()
				sub_history_esusu=sub_history_esusu.your_product_name

			else:

				sub_history_esusu = ""


			if esusu==1:		
				esu= {'App_name':'Esusu','App_status':esusu, 'App_label':sub_history_esusu}
				gh.append(esu)


			if app.savings1a==1:
				savings =1
			else:
				savings=0


			ppp= tblmyproducts.objects.get(product='Savings')


			sub_history_savings=sub_history.filter(product=ppp)

			if sub_history_savings.count() ==1:
				sub_history_savings=sub_history_savings.get()
				sub_history_savings=sub_history_savings.your_product_name
			else:
				sub_history_savings = ""
			
		

			if savings==1:

				sav= {'App_name':'Savings','App_status':savings, 'App_label':sub_history_savings}
				gh.append(sav)

			if sub_history.count() <=2:				

				return render(request,'sysadmin/myproducts.html',{'company':mybranch,
					'user':varuser,
					'comp':mybranch,
					'history':sub_history,
					'gh':gh})

			else:
				msg = 'error'


				return render(request,'Ia/selectloan.html',{'company':mybranch,
					'user':varuser,
					'msg':msg})

	else:
		return HttpResponseRedirect('/login/user/')



