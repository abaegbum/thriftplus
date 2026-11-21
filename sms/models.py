from django.db import models

from business.models import *
from customer.models import *
from Ia.models import *



class tblsmscustmerbuy(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE,default=1) #who registered me
	amount= models.IntegerField()
	sms_trans_id= models.CharField(max_length=40)
	credited_status=models.BooleanField()

	is_declined=models.BooleanField(default=False)
	
	date=models.DateField()
	time=models.TimeField()

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.amount,self.status)

class tblsmscustmertrans(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)
	balance=models.CharField(max_length=40)
	balance_before=models.CharField(max_length=40)
	balance_after=models.CharField(max_length=40)
	sms_trans_id= models.CharField(max_length=40, default=0)
	date=models.DateField()
	time=models.TimeField()


	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.balance_before,self.balance)


#customers who subscribe to 1a services
class tblIaSMS(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)


	esusu1a=models.BooleanField(default=False) #dEsusu
	esusu1aloan=models.BooleanField(default=False) #dEsusu


	savings1a=models.BooleanField(default=False) #General savings
	loans1acash=models.BooleanField(default=False) #cash loans
	loans1aitems=models.BooleanField(default=False) #items loans


	fixeddepo1a=models.BooleanField(default=False) #fixed deposit
	targetsave1a=models.BooleanField(default=False) #target savings


	# active_loan=models.BooleanField(default=False) #if you got loan


	ecomerce=models.BooleanField(default=False) #ecommerce

	thrift3b=models.BooleanField(default=False) #corporat C



	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.customer,self.thrift3b)

# class tblsmssenderidappbusiness(models.Model):
# 	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)	
# 	App= models.CharField(max_length=40)
# 	status=models.CharField(max_length=40)
# 	balance=models.CharField(max_length=40)
# 	sender_ID=models.CharField(max_length=40)
# 	unit_price=models.CharField(max_length=40,default=3.50)


# 	def __unicode__(self):
# 		return '%s %s %s'%(self.branch,self.App,self.balance) 


# class tblcustomersms(models.Model):
# 	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
# 	customer=models.ForeignKey(tblCUSTOMER,on_delete=models.CASCADE)
# 	App= models.CharField(max_length=40)
# 	status=models.BooleanField()
# 	balance=models.CharField(max_length=40)
# 	S = models.CharField(max_length=6)

# 	def __unicode__(self):
# 		return '%s %s %s'%(self.customer,self.App,self.balance)


# class tblcustomersmsperiodicity_transaction(models.Model):
# 	schedule=models.ForeignKey(tblcustomersms,on_delete=models.CASCADE)
# 	alert_type=models.CharField(max_length=40)
# 	def __unicode__(self):
# 		return '%s %s'%(self.schedule,self.alert_type)


# class tblcustomersmsperiodicity_weekly(models.Model):

# 	schedule=models.ForeignKey(tblcustomersms,on_delete=models.CASCADE)
# 	day_of_week =models.CharField(max_length=40)

# 	def __unicode__(self):
# 		return '%s %s'%(self.schedule,self.day_of_week)


# class tblcustomersmsperiodicity_monthly(models.Model):
# 	schedule=models.ForeignKey(tblcustomersms,on_delete=models.CASCADE)
# 	date_of_delivery=models.DateField(default='2021-05-08')
# 	nick =models.CharField(max_length=40)
# 	def __unicode__(self):
# 		return '%s %s'%(self.schedule,self.date_of_delivery)


# class tblcustomersmspurchases(models.Model):
# 	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
# 	customer=models.ForeignKey(tblCUSTOMER,on_delete=models.CASCADE)
# 	recdate = models.DateField()
# 	volume = models.IntegerField()
# 	merchant = models.IntegerField()
# 	cost = models.IntegerField()
# 	code=models.CharField(max_length=40)
# 	status = models.CharField(max_length=6)

# 	def __unicode__(self):
# 		return '%s %s %s'%(self.customer,self.recdate,self.code)




