from django.urls import path

from . import views

urlpatterns = [

	path('staff/staff/guide/',views.tutorial),
	 path('staff/home/',views.welcome),
	 path('staff/staffdet/',views.newst),
	 path('staff/viewstaffdet/',views.viewdetail),
	 path('staff/registeration/mass/',views.massReg),
	 path('staff/roleplay/',views.roles),
	 path('staff/staff_list/',views.listofstatt),
	 path('staff/deactivate/',views.deactivate),
	 path('staff/activate/',views.activate),
	  path('staff/delete/',views.delete),
	   path('staff/reset/',views.reset),

	 path('staff/selectrole/',views.setroles),
	 path('staff/updaterole/<int:vid>/',views.updaterole),
	 




# # ##******************** CREDIT OFFICES ***************************
path('staff/merchant/',views.regfieldagent),
path('staff/merchant/mypost/',views.services_update), 
 path('staff/merchant/manage/',views.manageco),
 path('staff/merchant/manage/popup/',views.manpop),
 path('staff/merchant/manage/change/',views.savepop),
 path('staff/merchant/location/popup/',views.locpop),
 path('staff/merchant/location/delete/<int:vid>/',views.locdel),
  path('staff/merchant/mycos/',views.mycos),



	 ]