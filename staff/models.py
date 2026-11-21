from django.db import models


from business.models import *

from sysadmin.mixing import FileCleanupMixin


class tblSTAFF(FileCleanupMixin, models.Model):
	branch=models.ForeignKey(tblBRANCH,on_delete=models.CASCADE)
	surname=models.CharField(max_length=20)
	firstname=models.CharField(max_length=20)
	othername=models.CharField(max_length=20, null=True,blank=True)
	email=models.EmailField(max_length=200)
	phone=models.CharField(max_length=11)
	Address=models.CharField(max_length=200)
	photo=models.ImageField(upload_to='staff-pix/', null=True,blank=True)
	code=models.CharField(max_length=41)
	types=models.CharField(max_length=20)
	ceo=models.BooleanField(default=False)
	status= models.BooleanField(default=False)
	
	def __unicode__(self):
		return '%s %s %s'%(self.surname,self.firstname,self.othername)


tblSTAFF.setup_file_cleanup()



