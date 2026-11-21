

from django.urls import path

from . import views

urlpatterns = [


	path('partner/repair/',views.repair),

	



	path('partner/restart/',views.restart),
	path('partner/rrr/',views.rrr),

	 path('partners/partner/',views.welcome),

	 path('partner/business/reg/',views.registration),

	 path('partner/business/branch/',views.branch),
	 path('partner/business/address/',views.address),

	 path('partner/business/ceo/',views.ceo),
	path('partner/business/ceodetails/',views.regceo),


	 path('partner/business/app/',views.app),
	 path('partner/business/app/<int:bid>/',views.app3),
	 path('partner/business/app/update/',views.app_update),


	 path('partner/business/subscription/',views.subscription),
	 path('partner/business/extension/',views.extension),
	 path('partner/business/extension/checkout/',views.chckoutext),

	 path('partner/business/renew/',views.renew),
	 path('partner/business/package/',views.package),

	 # path('partner/business/package/trial/',views.trial),

	 path('partner/business/packages/paid/',views.paid),

	 # path('partner/business/app/success/',views.app_update_success),


	 path('partner/business/manageall/',views.manageall),

	 path('partner/business/manage/status/',views.manageajax),


	 path('partner/business/manage/datepop/',views.datepop),


    # ##******************** VAS **************************** 
    path('partner/vas/', views.vas),
    path('partner/vas/process/', views.vasprocess),

	 ]