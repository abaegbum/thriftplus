from django import forms
from staff.models import *
from IIIb.models import *



monthy = (('---','----'),('January','January'),('February','February'),('March','March'),('April', 'April'),
	('May','May'),('June','June'),('July','July'),('August', 'August'),('September','September'),
	('October','October'),('November', 'November'),('December','December'))


month = (('-','----'),(1,'January'),(2,'February'),(3,'March'),(4, 'April'),
	(5,'May'),(6,'June'),(7,'July'),(8, 'August'),(9,'September'),
	(10,'October'),(11, 'November'),(12,'December'))



class approveform(forms.Form):
	month = forms.ChoiceField(label = 'Month' , choices=month)


class mysavingsform(forms.Form):
	month = forms.ChoiceField(label = 'Month' , choices=monthy)




class setsave(forms.Form):
	month_from = forms.ChoiceField(choices=monthy)
	month_to = forms.ChoiceField(choices=monthy)



# class loanreqform(forms.Form):
# 	amount = forms.IntegerField(label = 'Amount')
# 	loans = forms.ChoiceField(label = "Loan Parkage",choices = [(c.description, c.description) for c in tblstandardloanIIIB.objects.filter(status='ACTIVE')])

