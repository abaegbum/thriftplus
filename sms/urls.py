
from django.urls import path

# from . import views
from sms.views import *

urlpatterns = [

	#***********************Sms Subscription********************
	path('daily_contribution/sms/well/',well),
	path('daily_contribution/sms/funding_details/',fundingdetails),


	path('daily_contribution/sms/',sms_customer),

	path('daily_contribution/balance/',sms_purchase),
	path('thrift/sms/register/customer/',transactional),
	path('thrift/sms/sms_history/',sms_history),
	path('daily_contribution/history/',sms_history),
	path('daily_contribution/weeklysms/',weeklysms),
	path('daily_contribution/monthlysms/',monthlysms),

	path('daily_contribution/requests/buysms/',buysms),
	path('daily_contribution/pay/unit/',unit),
	path('daily_contribution/pay/sms/',pay4sms),



	########***********SMS ******##########################
path('customer/sms/',cussms),
path('customer/savesms/saveoptions/',save_smsoptions),
path('customer/savesms/save/',save_sms),

path('customer/smsactive/',cussmsactive),
path('customer/savesms/saveactive/',save_smsactive),

	]
