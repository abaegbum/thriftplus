from django.urls import path




from . import views

# from IIIB.views import *

urlpatterns = [


	#********************How it works************
	 path('threeb/home/', views.howitworks),


# 		####*******cooperatorst*******************
	path('threeb/staff_list/',views.stafflist),



# 	 ####*******set ups*****************
	 path('threeb/af/settings/',views.application_form),

	 path('threeb/loans/settings/',views.loan_setup),

	 path('threeb/maxloans/settings/',views.loan_limit),
	 path('threeb/maxloans/pop/',views.max_loan_pop),

	 path('threeb/maxloans/change/',views.max_loan_edit),
	 path('threeb/savings/settings/',views.savings_setup),





	 # 	 ####*******Manage set ups*****************
	 path('threeb/manage/settings/',views.manage_setup),



	 ##########opening balance
	 path('threeb/openingbalances/settings/',views.opening),
	  path('threeb/upload/settings/',views.uppld),



		####*******My wallet*******************
	 path('threeb/staff/mywallet/',views.history),
	 path('threeb/staff/statement/',views.statement),

	 path('threeb/staff/withdraw/',views.withdraw),
	 path('threeb/staff/withdrawajax/withdraw/',views.withdrawajax),
	 path('threeb/withdraw/ajax/pop/',views.withdrawpop),
	 path('threeb/mywallet/accno/',views.acctno),



# #************************my savings wallet schemes***********************
	 path('threeb/savings/wallet_packages/',views.wallet),
	 path('threeb/savings/eligibility/',views.eliibility),
	 path('threeb/savings/wallet_packages/create/',views.create_wallet_pack),


	 path('threeb/savings/save_packages/',views.safepack),
	 path('threeb/savings/deposit/packages/',views.save_pack),

	 path('threeb/savescheme/edit/pop/',views.editsavepop),
	 path('threeb/savescheme/edited/',views.editsave),
 
	 path('threeb/savings/deposit/view_transactions/',views.savelog),
	 path('threeb/staff/deposit/log/',views.deplogs),

	 path('threeb/savings/upload/',views.walletupload),


# #*********************MY loan******************************
	path('threeb/staff/request_loan/',views.reqloan),
	path('threeb/staff/request_loan/loan_packages/',views.getstandardloan),
     path('threeb/staff/request_loan/individual/',views.loandetails),
	path('threeb/staff/request_loan/performance/',views.loanperformance),
	path('threeb/staff/request_loan/history/',views.loanhistory),

	path('threeb/staff/loan/edit/pop/',views.editloanpop),
	path('threeb/staff/loan/edit/del/',views.delloan),



#*********************MY commodities******************************
	path('threeb/staff/request_commodities/',views.reqcomm),
     # path('threeb/staff/request_loan/loan_packages/',views.getloanpacks),
    path('threeb/staff/request_loan/individual/',views.loandetails),
	path('threeb/staff/request_loan/performance/',views.loanperformance),
	path('threeb/staff/request_loan/history/',views.loanhistory),

	path('threeb/staff/loan/edit/pop/',views.editloanpop),
	path('threeb/staff/loan/edit/del/',views.delloan),




#   	##***************Prorations***********
	 path('threeb/proration/',views.proration),
     path('threeb/loans/scenarios/',views.loanscene),
     path('threeb/proration/all/',views.proratepop),
     path('threeb/proration/details/',views.proratedetailspop),
     # path('threeb/proration/details/<int:vid>/',views.proratedetailspop),
    	path('threeb/staff/savings/prorate/yes/',views.prorateallrequests),


  	##***************Aprovals***********
	 path('threeb/approvals/',views.loan_approvals),
	path('threeb/loans/approval/ajax/',views.myloanpreviews),
	

	path('threeb/loanspp/decline/pop/',views.declinepop),
	path('threeb/loanspp/decline/',views.yesdeclineloan),


	path('threeb/requestdetails/',views.requestdetails),
	path('threeb/approvals/pop/',views.apprvepop),


  	##***************DISBURALS**********
	 path('threeb/requests/disburse/',views.loan_disburse),

	path('threeb/setsource/ajax/',views.setsource_ajax),
	path('threeb/setsave/ajax/',views.setsave_ajax),

	path('threeb/savescheme/pop/',views.withpopajax),
	
	 path('threeb/loans/payout/ajax/',views.disburse_ajax),
     path('threeb/requests/disburse/pop/',views.disbursepop),

 	 # path('threeb/staff/disburse/yes/',views.disburseallloan),



		####*******my deductions******************
	 path('threeb/staff/allmydeductions/',views.dedopts),
	 path('threeb/staff/allmydeduction/dedajax/',views.ajaxded),



		####*******H-R*******************
	 path('threeb/staff/myh-r/',views.hr),
	 path('threeb/staff/myh-r/ajax/',views.reportajaxx),

	 path('threeb/staff/mydeductions/',views.deductions),
	 path('threeb/staff/mydeductions/ajax/',views.deajax),
	path('threeb/loans/trail/deductions/',views.trailded),

	path('threeb/staff/myadditions/',views.deductions),

	path('threeb/staff/mynets/',views.deductions),


     

#************************my cash deposit*************
	 path('threeb/savings/deposit/',views.cash_deposit),
	 path('threeb/savings/deposit/monthajax/',views.destination_acc),
	 path('threeb/savings/depoajax/',views.checkdep),
	 path('threeb/savings/deposit/save/',views.save_deposit),





     # path('threeb/staff/request_loan/decline/yes/',views.yesdecline),

    #  path('threeb/loans/approval/ajax/',views.loanscene45),
     
    # path('threeb/savings/prorate/wallet/',views.prooneoffpop),
# 	 path('threeb/savings/prorate/wallet/yes/',views.prorateoneoff),

     # path('threeb/staff/request_loan/apply/',views.apply),
	# path('threeb/staff/repay_loan/',views.repay),


# path('threeb/loans/approve/all/',views.approveoptions),

#  path('threeb/savings/settings/',views.savings_setup),


# 	 # path('threeb/loans/settings/limit/',views.loan_limit),


#   	path('threeb/items/settings/',views.loan_setup),
#    	path('threeb/log/settings/',views.loan_setup),

# 	 path('threeb/admin/home/',views.adminwelcome),

# 	 #*********************membership***************
	 # path('threeb/registeration/',views.newregistration),
# 	 path('threeb/registeration/mass/',views.massReg),

# 	 path('threeb/vas/utils/',views.massReg),

# 	 path('threeb/staff/home/',views.staffwelcome),






#   	##***************LR***********
#      path('threeb/loans/lr/',views.lr),

#      path('threeb/loans/salary/',views.loandem),
#     path('threeb/loans/proorating/allloan/',views.loanprooptions),

# 	 path('threeb/staff/loan/proration/allyes/',views.proallloan),

#      path('threeb/loans/purchases/',views.lr),
#      path('threeb/loans/log/',views.proration),
#     path('threeb/loans/decline/',views.declineoptions),
#     path('threeb/staff/request_loan/decline/yes/',views.yesdecline),


# #******************MISC****************************
#      path('threeb/staff/changepass/',views.changepass),
#      # path('threeb/staff/profile/',views.my_Profile),

#      path('threeb/loans/repayment/',views.optionx),
#      path('threeb/staff/repay_loan/repay/',views.yesrepayloan),





	]
