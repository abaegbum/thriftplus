from django.db import models


from staff.models import *



from customer.models import *



class tblIIIbcoop(models.Model):  # cooperators' table
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    staff = models.ForeignKey(tblSTAFF, on_delete=models.CASCADE)
    thrift3b = models.BooleanField()
    can_get_loan = models.BooleanField(default=False)
    can_buy_commodity = models.BooleanField(default=False)    
    status = models.BooleanField()
    cooperators_code = models.CharField(max_length=40,default=0)

    def __str__(self):
        return f"{self.staff} | {self.cooperators_code} | {'Active' if self.status else 'Inactive'}"



class tblIIIbthrift(models.Model):  # cooperators' table
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    staff = models.ForeignKey(tblIIIbcoop, on_delete=models.CASCADE)
    can_get_loan = models.BooleanField(default=False)
    can_buy_commodity = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.staff} | {self.branch} "

class tblIIIbsavingsaccount(models.Model):  #  wallet and scheme
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    staff = models.ForeignKey(tblIIIbcoop, on_delete=models.CASCADE)  # whose got the money    
    month = models.CharField(max_length=30)  # main or referral
    year = models.CharField(max_length=30)
    status = models.CharField(max_length=30) #
    amount = models.IntegerField()  # amount porated
    transdate = models.DateField(default='2020-02-04')  # date of receipt
    account_type = models.CharField(max_length=20)  # Assets or liabilities
    account_code = models.CharField(max_length=30)  # asset_authorization_code
    transID = models.CharField(max_length=40, default=0) #transac _id

    

    def __str__(self):
        return f"{self.staff} | {self.amount} | {self.transdate}"


# # #where all application to opt in a savings scheme go 
class tblIIIIbassets_authorization(models.Model): #class tblIIIIbassets_authorization(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	staff=models.ForeignKey(tblIIIbcoop,on_delete=models.CASCADE)
	month= models.CharField(max_length=40)
	year= models.CharField(max_length=40)
	asset_authorization_code =models.CharField(max_length=40,default=0)
	transdate=models.DateField()  #date of transaction
	amount= models.CharField(max_length=40) 
	description=models.CharField(max_length=40) #dr , cr
	status=models.CharField(max_length=40)
	def __unicode__(self):
		return '%s %s %s'%(self.transdate,self.amount,self.status)



#All c/os field activities here
class tblIIIbprorations_schedule(models.Model): #bfieldagent(models.Model):
	status=models.CharField(max_length=30)
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	staff=models.ForeignKey(tblIIIbcoop,on_delete=models.CASCADE) #whose got the mone

	month=models.CharField(max_length=30)#main or referal
	year=models.CharField(max_length=30)
	amount=models.IntegerField() #amount recieved
	transdate=models.DateField() #date of recept
	transID=models.CharField(max_length=40,default=0)
	
	authorization_code=models.CharField(max_length=30) #transaction code
	account_type=models.CharField(max_length=20) #wallet or package
	scheme=models.CharField(max_length=50,null =False)#main or referal

	def __unicode__(self):
		return '%s %s %s'%(self.transdate,self.amount,self.code)


class tblIIIbprorations(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	staff=models.ForeignKey(tblIIIbcoop,on_delete=models.CASCADE) #whose got the mone
	month=models.CharField(max_length=30)#main or referal
	year=models.CharField(max_length=30)
	amount=models.IntegerField() #amount recieved
	transdate=models.DateField() #date of recept
	# description=models.CharField(max_length=30)
	status=models.CharField(max_length=30)
	def __str__(self):
		return f"{self.transdate} {self.amount} {self.status}"



class tblstandardloanIIIB(models.Model):
    staffrec = models.ForeignKey(tblIIIbcoop, on_delete=models.CASCADE)
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    tenure = models.IntegerField()  # loan duration in months
    rate = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 12.50 for 12.5%
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.rate}% - {self.description} ({self.tenure} months)"


class tblIIIIbliabilities_authorization(models.Model):
	branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
	staff = models.ForeignKey(tblIIIbcoop, on_delete=models.CASCADE)
	package = models.ForeignKey(tblstandardloanIIIB, on_delete=models.CASCADE)
	application_date = models.DateField()
	approval_date = models.DateField()
	disbursal_date = models.DateField()
	status = models.CharField(max_length=20)
	year= models.CharField(max_length=40)
	

	principal = models.IntegerField()
	thrift = models.DecimalField(max_digits=12, decimal_places=2)

	interest = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	total_repayment = models.DecimalField(max_digits=12, decimal_places=2)

	grace_period = models.IntegerField()# in days
	application_code = models.CharField(max_length=20)
	description=models.CharField(max_length=40)#Loan or Commodities

	def __str__(self):
		return f"{self.branch} | {self.package} | {self.principal}"







class tblIIIb_bankdetail(models.Model):
    staff = models.ForeignKey(tblIIIbcoop, on_delete=models.CASCADE)
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=20)
    account_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.bank_name} {self.account_number} {self.branch}"




# # #where all scheme withdrawal goes to 
class tblIIIIbscheme_withdrawal(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	staff=models.ForeignKey(tblIIIbcoop,on_delete=models.CASCADE)
	year= models.CharField(max_length=40)
	scheme_authorization_code =models.CharField(max_length=40)
	transdate=models.DateField()  #date of transaction
	amount = models.IntegerField()  # amount porated
	# amount= models.CharField(max_length=40) 
	description=models.CharField(max_length=40) #dr , cr
	status=models.CharField(max_length=40)
	def __unicode__(self):
		return '%s %s %s'%(self.transdate,self.staff,self.status)




class tblstandardsavingIIIB(models.Model): #for savings schemes/packaages
	staffrec=models.ForeignKey(tblIIIbcoop,on_delete=models.CASCADE)
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	from_month=models.CharField(max_length=20)
	to_month=models.CharField(max_length=20)
	description=models.CharField(max_length=20)
	active=models.BooleanField(default=False)


	def __unicode__(self):
		return '%s %s %s'%(self.rate,self.description,self.from_week)



class tblIIIbclientsubscription(models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	subscription=models.IntegerField() #who colected the money
	status=models.BooleanField(max_length=40) 

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.amount,self.status)


# # # registration money 
class tblIIIIbregistration(models.Model):
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    staff = models.ForeignKey(tblIIIbcoop, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transdate = models.DateField()  # date of transaction
    description = models.CharField(max_length=40)  # registration fee
    status = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.transdate} {self.amount} {self.status}"




# # # subscription fee 
class tblIIIIsubscriptionfee(models.Model):
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount}"



class tblmaxloanIIIB(models.Model):
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.branch} | {self.value}"

















	







class tblIIIbcommapplications(models.Model):
    branch = models.ForeignKey(tblBRANCH, on_delete=models.CASCADE)
    date = models.DateField()
    staffrec = models.ForeignKey(tblIIIbcoop, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    item = models.CharField(max_length=500)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.branch} | {self.item} | {self.price}"


class tblIIIbloantransaction(models.Model): 
    transaction_source = models.ForeignKey(tblIIIIbliabilities_authorization, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.CharField(max_length=30)  # main or referral
    year = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.amount} | {self.month} | {self.status}"
