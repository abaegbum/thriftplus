from django.db import models

from staff.models import *
from sysadmin.mixing import FileCleanupMixin




class tblCUSTOMER(FileCleanupMixin, models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)

	surname=models.CharField(max_length=20)
	firstname=models.CharField(max_length=120)
	othername=models.CharField(max_length=20)
	location=models.CharField(max_length=120)
	wallet=models.CharField(max_length=40)
	phone=models.CharField(max_length=40)
	Address=models.CharField(max_length=200)
	photo=models.ImageField(upload_to='customer_photo', null=True,blank=True,default='customer_photo/user.png')
	email=models.EmailField()

	ttime= models.TimeField(default='12:00')
	created_by=models.ForeignKey(tblSTAFF,on_delete=models.CASCADE)
	created_date=models.DateField(default='2022-01-07')

	status=models.BooleanField(default=False)

	dc=models.BooleanField(default=False)  #daily contr
	ivb=models.BooleanField(default=False)  #investment Banking
	ts=models.BooleanField(default=False)   #target savings
	cc=models.BooleanField(default=False)  	#corperate C
	cs=models.BooleanField(default=False)   #cooperative society
	code=models.CharField(max_length=40)
	def __unicode__(self):
		return '%s %s %s'%(self.surname,self.firstname,self.othername)


tblCUSTOMER.setup_file_cleanup()
