


from django.db import models

from staff.models import *

from customer.models import *




#####*************Ajo Savings*****###################

class tblIaMERCHANT(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	staff=models.ForeignKey(tblSTAFF,on_delete=models.CASCADE)
	status=	 models.BooleanField(default=False)
	code=models.CharField(max_length=40)
	thrift1a = models.BooleanField(default=False)
	direc_credit = models.BooleanField(default=False)
	direct_withdraw = models.BooleanField(default=False)

	esusu1a= models.BooleanField(default=False)
	esusu1aloan= models.BooleanField(default=False)

	savings1a= models.BooleanField(default=False)
	loans1acash=models.BooleanField(default=False) #cash loans
	loans1aitems=models.BooleanField(default=False) #items loans

	fixeddepo1a=models.BooleanField(default=False) #fixed deposit
	targetsave1a=models.BooleanField(default=False) #target savings


	def __unicode__(self):
		return '%s %s %s'%(self.staff,self.status,self.code)


#customers who subscribe to 1a services
class tblIaCUSTOMER(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE) #who registered me
	customer=models.ForeignKey(tblCUSTOMER,on_delete=models.CASCADE)

	esusu1a= models.BooleanField(default=False)
	esusu1aloan= models.BooleanField(default=False)


	savings1a= models.BooleanField(default=False)
	loans1acash= models.BooleanField(default=False)
	loans1aitems=models.BooleanField(default=False) #items loans


	fixeddepo1a=models.BooleanField(default=False) #fixed deposit
	targetsave1a=models.BooleanField(default=False) #target savings
	active_loan=models.BooleanField(default=False) #if you got loan


	UX= models.BooleanField(default=False)
	status=models.BooleanField(default=False)
	online=models.BooleanField(default=False)
	code=models.CharField(max_length=40)
	sms=models.BooleanField(default=False)
	get_email=models.BooleanField(default=False)
	withdr_status=models.BooleanField(default=False)



	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.status,self.code)



#where merchants are assigned to
class tblIalocations(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE)
	location=models.CharField(max_length=120)
	code=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.merchant,self.branch,self.location)



#Thrfit and loans record 
class tblIathrift(models.Model):
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	month=models.CharField(max_length=20)
	monthindex=models.IntegerField()
	thrift=models.CharField(max_length=40)
	service_charge=models.CharField(max_length=40)
	code=models.CharField(max_length=40)
	year=models.CharField(max_length=20)
	cycle=models.CharField(max_length=40,default='cycle 1')
	purpose=models.CharField(max_length=120)

	is_overdraft=models.BooleanField(default=False) #HAVE I GOTTEN ANY LOAN FROM THIS

	is_contributed=models.BooleanField(default=False) #do i HAVE NET SAVINGS?
	complete_status=models.BooleanField(default=False) #HAVE I FILLED ALL 31 BLKS
	is_closed=models.BooleanField(default=False)	#ARE YOU STILL ACCEPTING DEPOSITS?

	is_empty=models.BooleanField(default=False) #HAVE I WITHDRAWN ALL 30 BLOKS
	withdraw_status=models.BooleanField(default=False) #AM I BLOCKED FROM WITHDRAWALS?


	is_done=models.BooleanField(default=False) #IS MY LOAN REPAID?
	overdraft_date_start=models.DateField(null =True)
	overdraft_date_end=models.DateField(null = True)
	interest_on_loan=models.CharField(max_length=40,default='0')
	actual_loan=models.CharField(max_length=40,default='0')
	overdraft=models.CharField(max_length=40,default='0')


	def __unicode__(self):
		return '%s %s %s'%(self.cycle,self.month,self.code)



#C/Os account for 1a where customers pay into
class tblIafieldagent(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE) 
	status=models.CharField(max_length=30) #Unapproved, approved
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE) #who got the money
	wallet_type=models.CharField(max_length=30)#main or referal
	amount=models.CharField(max_length=40) #amount recieved
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE) #who's money was got
	programmm =models.CharField(max_length=30) #'X + Nj' or 'Nj'
	code=models.CharField(max_length=30) #thrift related code
	recdate=models.DateField() #date of receipt
	
	number =models.CharField(max_length=40)#number of contribution
	ttime= models.TimeField(default='12:00')#time the collection occured
	transac_id=models.CharField(max_length=40) #transaction code
	cycle=models.CharField(max_length=40,default='cycle 1')
	purpose=models.CharField(max_length=120)
	is_declined=models.BooleanField(default=False)#True or false


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.amount,self.code)




#business account for 1a for holding sales and approvals
class tblIamerchantBank(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	code=models.CharField(max_length=40) #originates from thrift
	amount = models.CharField(max_length=40) #amount collected
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE) #if sales, admin. if approval, merchant
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE) #who's money was collected
	transdate=models.DateField()  #date of transaction

	product=models.CharField(max_length=40,default='Savings')#savings or loan

	number =models.CharField(max_length=40) #number of contribution
	wallet_type=models.CharField(max_length=30) #main or referal
	status= models.CharField(max_length=30) #credit, debit
	transac_id = models.CharField(max_length=40) #transacttion id

	description=models.CharField(max_length=30,default='Credit') #credit, debit,loan repayment

	cycle=models.CharField(max_length=40)#cycle
	purpose=models.CharField(max_length=120)#purpose
	year=models.CharField(max_length=20)#year
	recdate=models.DateField()  #date of record
	ttime= models.TimeField(default='12:00')#time of sales(if admin) or recon
	approved_by=models.CharField(max_length=50) #who did the reconciliation or sales




	def __unicode__(self):
		return '%s %s'%(self.recdate,self.amount)


#where all customers' savings, withdrwals and service charges are kept
class tblIasavings_trans(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE) #who colected the money
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE) #whose money is it
	transdate=models.DateField()  #date of transaction
	amount= models.CharField(max_length=40) #how much was collected
	wallet_type=models.CharField(max_length=40,default='Main') #main or referal

	product=models.CharField(max_length=40,default='Savings')#savings or loan

	number =models.CharField(max_length=40)#number of contribution  
	description=models.CharField(max_length=40) #dr , cr  
	status=models.CharField(max_length=40) #service charges, withdrawn,
	code=models.CharField(max_length=40) #originates from thrift
	cycle=models.CharField(max_length=40)#cycle
	purpose=models.CharField(max_length=120)#purpose
	year=models.CharField(max_length=20) #year
	avalability=models.CharField(max_length=50) #use availability to manipulate withdrwal (if u got loan)
	transac_id = models.CharField(max_length=40) #transacttion id from fieldtable
	ttime= models.TimeField(default='12:00') #ttime of reconciliation
	recdate=models.DateField() #record date from fieldtable

	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.wallet_type)




#customers' iCard detailss
class tblIacards(models.Model):
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	purpose=models.CharField(max_length=130)
	card_status= models.BooleanField(default=False)
	year=models.CharField(max_length=13,default=2025)
	def __unicode__(self):
		return '%s %s %s'%(self.customer,self.purpose,self.branch)




#third party withdrawal requests
class tblIapayoutrequest(models.Model):
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE)
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)

	recdate=models.DateField() #cashin date from merchant
	status= models.CharField(max_length=20)
	amount=models.CharField(max_length=50)

	wallet_type=models.CharField(max_length=40,default='Main') #changed

	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.wallet_type,self.customer)


#third party withdrawal requests granted
class tblIapayoutrecord(models.Model):
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE)
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)

	recdate=models.DateField() #cashin date from merchant
	status= models.CharField(max_length=20)
	amount=models.CharField(max_length=50)
	wallet_type=models.CharField(max_length=40,default='Main') #changed


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.wallet_type,self.customer)




#####*************General Savings*****###################


#C/Os accont for 1bb where customers pay into
class tblIbbfieldagent(models.Model):

	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	amount=models.CharField(max_length=40) #amount recieved
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE) #whose got the mone


	recdate=models.DateField() #date of recept
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)


	ttime= models.TimeField(default='12:00')
	status=models.CharField(max_length=30)
	year=models.CharField(max_length=20)

	transac_id=models.CharField(max_length=40) #transaction code
	wallet_type=models.CharField(max_length=30)#main or referal


	is_declined=models.BooleanField(default=False)


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.amount,self.transac_id)



class tblIbbsavings_trans(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	amount= models.CharField(max_length=40) #how much
	merchant=models.ForeignKey(tblIaMERCHANT,on_delete=models.CASCADE) #who colected the money

	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE) #whose money is it
	recdate=models.DateField() #recorddate
	transdate=models.DateField()  #date of transaction

	ttime= models.TimeField(default='12:00')
	status=models.CharField(max_length=40) #service charges, withdrawn,


	wallet_type=models.CharField(max_length=40,default='Main') #
	transac_id = models.CharField(max_length=40) #transacttion id


	description=models.CharField(max_length=40) #dr , cr
	avalability=models.CharField(max_length=50) #use availability to manipulate withdrwal (if u got loan)

	year=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.wallet_type)





###*Loans for general savings **************#

class tblIastandardloan(models.Model):
	staffrec=models.ForeignKey(tblSTAFF,on_delete=models.CASCADE)
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	duration=models.CharField(max_length=40)
	rate=models.CharField(max_length=20)
	description=models.CharField(max_length=20)
	status=models.BooleanField(default=False)

	def __unicode__(self):
		return '%s %s %s'%(self.rate,self.description,self.duration)



class tblIagrace(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	plan=models.CharField(max_length=20)
	grace=models.IntegerField()
	status=models.BooleanField(default=False)

	def __unicode__(self):
		return '%s %s'%(self.plan,self.branch)



class tblloandetails(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)
	start_date =models.DateField(max_length=20)
	end_date =models.DateField(max_length=20)
	staffrec=models.ForeignKey(tblSTAFF,on_delete=models.CASCADE)
	package=models.ForeignKey(tblIastandardloan,on_delete=models.CASCADE)
	status=models.CharField(max_length=20)
	code=models.CharField(max_length=20)
	volume=models.CharField(max_length=20)
	card=models.CharField(max_length=20)
	thrift=models.CharField(max_length=20)
	repayment=models.CharField(max_length=20)
	frequency=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.volume,self.package)



class tblloanrepay(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	loan=models.ForeignKey(tblloandetails,on_delete=models.CASCADE)
	customer=models.ForeignKey(tblIaCUSTOMER,on_delete=models.CASCADE)
	repaid=models.CharField(max_length=20)
	transac_id=models.CharField(max_length=20)
	pd_date =models.DateField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.loan,self.repaid)





class tblIatv(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	product=models.CharField(max_length=20) #Ajo, Savings, Ajo_loan,General_loan, fxd_depo,inv_bank
	ddate =models.DateField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.product,self.ddate)




