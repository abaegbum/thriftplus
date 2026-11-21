from django.db import models


from staff.models import *


class Userprofile(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	staffrec=models.ForeignKey(tblSTAFF,on_delete=models.CASCADE)
	email=models.EmailField()
	password=models.CharField(max_length=20)

	code=models.CharField(max_length=41)
	ceo=models.BooleanField(default=False)


	
	thrift1a=models.BooleanField(default=False) #the App itself
	thrift_officer = models.BooleanField(default=False) #merchant
	admin=models.BooleanField(default=False)    #admin



	esusu1a=models.BooleanField(default=False) #dEsusu
	esusu1aloan=models.BooleanField(default=False) #dEsusu


	savings1a=models.BooleanField(default=False) #General savings
	loans1acash=models.BooleanField(default=False) #loans
	loans1aitems=models.BooleanField(default=False) #items loans

	fixeddepo1a=models.BooleanField(default=False) #fixed deposit
	targetsave1a=models.BooleanField(default=False) #target savings


	thrift1b=models.BooleanField(default=False) #investment banking
	thrift1b_officer = models.BooleanField(default=False)
	thrift1b_admin=models.BooleanField(default=False)
	thrift1b_cashier = models.BooleanField(default=False)


	loan1b=models.BooleanField(default=False) #investment banking loan
	loan1b_admin=models.BooleanField(default=False)
	loan1b_officer = models.BooleanField(default=False)	
	

	thrift3a=models.BooleanField(default=False) #Corporate C
	thrift3a_officer = models.BooleanField(default=False)
	thrift3a_admin=models.BooleanField(default=False)
	thrift3a_cashier = models.BooleanField(default=False)

	loan3a = models.BooleanField(default=False)
	loan3a_admin=models.BooleanField(default=False)
	loan3a_officer = models.BooleanField(default=False)


	thrift3b=models.BooleanField(default=False) #Cooprative
	thrift3b_officer = models.BooleanField(default=False)
	thrift3b_admin=models.BooleanField(default=False)
	thrift3b_cashier = models.BooleanField(default=False)

	loan3b = models.BooleanField(default=False)
	loan3b_admin=models.BooleanField(default=False)
	loan3b_officer = models.BooleanField(default=False)



	status=models.BooleanField(default=False)
	partner=models.BooleanField(default=False)

	def __unicode__(self):
		return '%s %s %s'%(self.email,self.partner,self.admin)



class tblthriftpackages(models.Model):
	package=models.CharField(max_length= 50)
	appendage=models.CharField(max_length= 50)
	staff_count= models.CharField(max_length=40)
	customer_count=models.CharField(max_length=40)
	status =models.BooleanField(default=False)
	cost=models.CharField(max_length= 50)
	weight=models.CharField(max_length= 50)

	def __unicode__(self):
		return '%s %s %s'%(self.package,self.staff_count,self.customer_count)

class tblsubscription(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	package=models.ForeignKey(tblthriftpackages,on_delete=models.CASCADE)
	duration=models.CharField(max_length=40)
	start=models.DateField()
	end=models.DateField()
	receipt=models.CharField(max_length=320)
	status=models.CharField(max_length=320,default='INACTIVE')
	amount=models.CharField(max_length=320,default='0')
	app=models.CharField(max_length=320)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.package,self.duration)


class tblsubpending(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	package=models.ForeignKey(tblthriftpackages,on_delete=models.CASCADE)
	duration=models.CharField(max_length=40)

	receipt=models.CharField(max_length=320)
	app=models.CharField(max_length=320)
	amount =models.CharField(max_length=20)
	status=models.CharField(max_length=320)


	def __str__(self):
	    return f"{self.branch} {self.package} {self.duration}"



class tblsubpendingcoop(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	duration=models.CharField(max_length=40)
	receipt=models.CharField(max_length=320)
	app=models.CharField(max_length=320)
	amount =models.CharField(max_length=20)
	status=models.CharField(max_length=320)


	def __str__(self):
	    return f"{self.branch} {self.app} {self.duration}"




class tbldefaultpass(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	password=models.CharField(max_length=320)


	def __unicode__(self):
		return '%s %s'%(self.branch,self.password)


class tblbusinesslocations(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	location=models.CharField(max_length=320)
	code=models.CharField(max_length=320)


	def __unicode__(self):
		return '%s %s'%(self.branch,self.location)


class tblswitchpro(models.Model):
	datte=models.DateField()
	status=models.BooleanField(default=False)


	def __unicode__(self):
		return '%s %s'%(self.datte,self.status)



class tblrollover(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	status=models.BooleanField(default=False)
	year=models.CharField(max_length=8,default='2023')


	def __unicode__(self):
		return '%s %s'%(self.branch,self.status)


class tblcarding(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	fresh=models.CharField(max_length=4)
	reissue=models.CharField(max_length=4)


	def __unicode__(self):
		return '%s %s'%(self.branch,self.fresh)



class tblmyproducts(models.Model):
	product=models.CharField(max_length=40)
	code=models.CharField(max_length=40)
	def __unicode__(self):
		return '%s %s'%(self.product,self.code)


class tblproductsname(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	product=models.ForeignKey(tblmyproducts,on_delete=models.CASCADE)
	your_product_name=models.CharField(max_length=40)


	def __unicode__(self):
		return '%s %s'%(self.branch,self.your_product_name)



class tblbusinessyear(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	year=models.CharField(max_length=8,default='2023')

	def __unicode__(self):
		return '%s %s'%(self.branch,self.year)


class tblbusinesspresence(models.Model):
	country=models.CharField(max_length=80,default='2023')
	country_code=models.CharField(max_length=8,default='2023')
	currency_code=models.CharField(max_length=8,default='2023')
	status=models.BooleanField(default=False)
	currency_description= models.CharField(max_length=80)

	def __unicode__(self):
		return '%s %s'%(self.country,self.currency_code)



class tblplatformdiscount(models.Model):
	package=models.ForeignKey(tblthriftpackages,on_delete=models.CASCADE)
	duration=models.CharField(max_length=40)
	discount=models.CharField(max_length=320)
	status=models.CharField(max_length=320,default='INACTIVE')

	def __unicode__(self):
		return '%s %s %s'%(self.duration,self.discount,self.status)
