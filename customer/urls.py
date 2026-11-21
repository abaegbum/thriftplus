from django.urls import path

from . import views

urlpatterns = [
##********************Create Wallet***************
	 path('customers/createwallet/', views.createwallet),
	 path('customers/editwallet/',views.editwallet),
	 path('customers/editwallet/wallet/',views.doedit),
	 path('customers/viewwallet/',views.viewwallet),
	 path('customers/customer_list/',views.customerslist),



###*****Customers' Area**************
	 path('customers/myprofileview/',views.viewwallet),  







# # ##******************** CUSTOMERS ***************************
 path('customeria/list/',views.cus_list),
  path('customer/list/lajax/',views.ajaxcus_list),
  path('customer/list/adminajaxlist/',views.adminlistajax),

  path('customer/list/lajax2/',views.ajaxcus_list2),

  path('customer/list/jaxlist/',views.mylistajax),


	   
###*****************************MISC************************

	
	]
