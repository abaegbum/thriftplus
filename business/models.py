from django.db import models

from partner.models import *


from sysadmin.mixing import FileCleanupMixin


class tblCOMPANY(FileCleanupMixin, models.Model):
	partner = models.ForeignKey(tblPARTNER,on_delete=models.CASCADE)
	name =models.CharField(max_length=500)
	code = models.CharField(max_length=15)
	web = models.CharField(max_length=200)
	ig=models.CharField(max_length=50)
	twitter = models.CharField(max_length=40)
	fb= models.CharField(max_length=50)
	youtube=models.CharField(max_length=50)
	engine=models.CharField(max_length=50)
	size=models.CharField(max_length=40)
	ux= models.BooleanField(default=False)
	status= models.BooleanField(default=False)
	logo = models.ImageField(upload_to='company_logo/', null=True,
		blank=True,default='company_logo/logo.jpg')
	

	def __unicode__(self):
		return '%s %s %s'%(self.name,self.web,self.size)


tblCOMPANY.setup_file_cleanup()



class tblBRANCH(models.Model):
	company=models.ForeignKey(tblCOMPANY,on_delete=models.CASCADE)
	code=models.CharField(max_length=40)
	country_code=models.CharField(max_length=6, default='234')
	Address = models.CharField(max_length=300)
	phone= models.CharField(max_length=11)
	types=models.CharField(max_length=50)
	status = models.BooleanField(default=False)
	currency_code = models.CharField(max_length=300)
	currency_description= models.CharField(max_length=300)

	def __unicode__(self):
		return '%s %s %s'%(self.company,self.Address,self.types)

class tblmanager(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	name=models.CharField(max_length=200)
	phone=models.CharField(max_length=40)
	photo=models.ImageField(upload_to='staff-pix', null=True,
		blank=True,default='staff-pix/thrift.png')
	code=models.CharField(max_length=40)

	def __unicode__(self):
		return '%s %s %s'%(self.name,self.code,self.phone)


class tblaccountDetails(models.Model):
	company=models.ForeignKey(tblCOMPANY,on_delete=models.CASCADE) #use tblbranch instaed
	account=models.CharField(max_length=40)
	bank = models.CharField(max_length=10)
	code= models.CharField(max_length=40)

	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.date,self.customer)


		
class tblapp(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	partner = models.ForeignKey(tblPARTNER,on_delete=models.CASCADE)


	thrift1a=models.BooleanField(default=False) #step this down
	
	esusu1a=models.BooleanField(default=False) #dEsusu
	esusu1aloan=models.BooleanField(default=False) #dEsusu


	savings1a=models.BooleanField(default=False) #General savings
	loans1acash=models.BooleanField(default=False) #cash loans
	loans1aitems=models.BooleanField(default=False) #items loans


	investment=models.BooleanField(default=False) #fixed deposit
	fixeddepo1a=models.BooleanField(default=False) #fixed deposit
	targetsave1a=models.BooleanField(default=False) #target savings


	ecomerce=models.BooleanField(default=False) #ecommerce

	thrift3b=models.BooleanField(default=False) #corporat C

	def __str__(self):
		return f"{self.partner} {self.branch} thrift:{self.thrift1a}"



class tblvas(models.Model):
	company=models.ForeignKey(tblCOMPANY,on_delete=models.CASCADE) #use tblbranch instaed
	partner = models.ForeignKey(tblPARTNER,on_delete=models.CASCADE)
	ux= models.BooleanField(default=False)
	otp= models.BooleanField(default=False)
	sms= models.BooleanField(default=False)
	email= models.BooleanField(default=False)
	

	# def __str__(self):
	# 	return f"{self.email} {self.otp} thrift:{self.partner}"


	def __unicode__(self):
		return '%s %s %s'%(self.email,self.otp,self.partner)




class tblsmssenderid(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)	
	senderId= models.CharField(max_length=40)
	status=models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.senderId,self.status) 


class tblsmsbuy(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)	
	amount= models.IntegerField()
	sms_trans_id= models.CharField(max_length=40)
	credited_status=models.BooleanField()
	date=models.DateField()
	time=models.TimeField()

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.amount,self.status)

class tblsmstrans(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	balance=models.CharField(max_length=40)
	balance_before=models.CharField(max_length=40)
	balance_after=models.CharField(max_length=40)
	sms_trans_id= models.CharField(max_length=40, default=0)
	date=models.DateField()
	time=models.TimeField()


	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.balance_before,self.balance)
