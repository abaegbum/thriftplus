"""
URL configuration for thriftplus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home)
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home)
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls))
"""

from django.urls import path

from . import views
# from Ia.views import *

urlpatterns = [

########***********CUSTOMERS' DASHBOARD ******##########################
   path('thrift/mycustomer/',views.straighttocus), #direct
   
 path('mycustomers/dashboard/<int:vid>/',views.cusboard), #indirect







  # path('thrift/admin/program/poprepost/',views.progrepost),

  # path('thrift/repost/admin/',views.prorecon),



# # ##******************** CREDIT OFFICES ***************************
path('staff/merchant/',views.regfieldagent),
path('staff/merchant/mypost/',views.services_update), 
 path('staff/merchant/manage/',views.manageco),
 path('staff/merchant/manage/popup/',views.manpop),
 path('staff/merchant/manage/change/',views.savepop),
 path('staff/merchant/location/popup/',views.locpop),
 path('staff/merchant/location/delete/<int:vid>/',views.locdel),
  path('staff/merchant/mycos/',views.mycos),



# # ##******************** CUSTOMERS ***************************
 path('customeria/list/',views.cus_list),
  path('customer/list/lajax/',views.ajaxcus_list),
  path('customer/list/adminajaxlist/',views.adminlistajax),

  path('customer/list/lajax2/',views.ajaxcus_list2),

  path('customer/list/jaxlist/',views.mylistajax),



# # ##********************General THRIFTS ***************************
path('thrift/thriftreport/',views.thriftrep),



# ##********************RECONCILIATIONS ***************************
    path('thrift/approvals/',views.approval),




path('customeria/list/<int:dl>/',views.cusreturn),
path('customer/viewwallet/<int:vid>/',views.viewwalletpop),
path('thrift/deposit/ajaxaccount_dep/',views.ajaxxccount_dep),

 path('thrift/funding/depsource/',views.depsource),



##******************** RESET BACK OFFICE  ****************************
     path('reset/home/',views.homereset),
     path('reset/',views.reset), 


# ##******************** RECEIPTS (General) ***************************
path('receipts/general/',views.receipts),











########***********ACTIVATE ******##########################
path('customer/products/',views.products),
path('customer/saveproducts/save/',views.save_client_products),



########***********CARDS ******##########################
path('customer/savecard/',views.safecard),
path('customer/ajax/savecard/',views.safecardajax),
path('customer/savecard/save/',views.safecardsave),



########***********THRIFTS ******##########################
 path('customer/dialthrift/',views.dithrift),
 path('customer/findcard/thrift/',views.findcardthrift),
 path('customer/findthrift/',views.findthrift),
 path('customer/thrift/addthrift/',views.popputthrift),




########***********DEPOSITS ESUSU******##########################
  path('customer/deposit/',views.didep),
  path('customer/findcard/deposit/',views.findcarddeposit),
  path('customer/deposit/valmonth/',views.fillmonthdep),
  path('customer/deposit/comcycle/',views.fillcycledep),
  path('thrift/deposit/account_dep2/',views.account_dep2),
  path('thrift/funding/getsource/',views.source),

  path('cashin/admin/display/',views.depdisplay),

  path('thrift/requests/cashin/admin/',views.admin_cashin),

path('deposit/payidsplay/',views.paygensave),
path('gensavings/admin/cashin/',views.gen_savings_admin_cashin),


########***********WITHDRAWAL ESUSU******##########################
path('customer/popwithdraw/',views.popwithdraw),
path('customer/findcard/withdraw/',views.findcardwithdraw),
path('customer/withdraw/allmonth/',views.fillmonthwithdr),
path('customer/withdraw/withcycle/',views.fillcyclewit),
path('customer/withdraw/account_withdrawpop/',views.account_withdraw_pop),
path('thrift/cashout/display/',views.displaycashout),
path('thrift/cashout/admin/',views.cashoutrequest),

########***********WITHDRAWAL General Savings*****##########################
path('customer/cashout/display/',views.cashoutdispl),
path('customer/cashout/admin/',views.witcashout),



##############RECEIPTS ( CUSTOMER)***********#############
path('customer/viewreceipts/<int:vid>/',views.cusreceipt),


########***********ACCOUNT BALANCES******##########################
path('thrift/historypop/',views.historypop),
path('customer/findcard/balance/',views.findcardbalance),
path('customer/balances/actmonth/',views.fillmonthbal),
path('customer/balances/fillbalancetype/',views.fillmonthbalooooo),
path('customer/balances/balcycle/',views.fillbalcycle),
path('customer/account_historypop/',views.account_history_pop),


########***********E-CARD ******##########################
path('thrift/ecardpop/',views.ecardpop),
path('customer/findcard/statement/',views.findcardstatement),
path('customer/ecardpop/ecardmonth/',views.ecardmonth),
path('customer/ecard/statement/',views.fillecardcycle),
path('thrift/addthrift/account_statement_history/',views.account_statement_history),


########***********TAKE A LOAN ******##########################
path('customer/overdrafts/',views.popoverdrafts),
path('customer/overfdraf/dramonth/',views.draftmonth),
path('customer/overdraft/overcycle/',views.fillcycledraft),
path('customer/overdrafts/bum/',views.ovedraftbum),
path('thrift/overdrafts/display/',views.displayoverdraft),
path('thrift/overdrafts/admin/',views.approvemyloan),



path('customer/overfdraf/packages/',views.ploan),
path('customer/overfdraf/breakdown/',views.loanbreak),
path('customer/overdrafts/continuous/display/',views.displaycontinuousoverdraft),
path('customer/overfdraft/generalsavings/approveloan/',views.generalsaveapproveloan),

########***********REPAY LOAN ******##########################
path('customer/repayloan/<int:vid>/',views.reploanview),

  path('customer/repayloan/pickmonth/',views.fillmonthloanrep),
  path('customer/repayloan/loanrepcycle/',views.fillcyclerep),
  path('customer/repayloan/account_rep/',views.loan_account_repay),
  path('customer/repayloan/find_source/',views.loansource),
  path('customer/repayloan/repay/admin/',views.repayadmin), #direct depo

path('customer/overdraft/running/',views.genploan),

path('customer/pop/loanrepay/',views.ru),

path('customer/overdraft/repayloan/',views.loanepay), 

########*********** MY LOANS******##########################
path('customer/myloans/poploan/<int:vid>/',views.myloansview),
  path('customer/myloanloan/loantype/',views.loantype),


########***********RECYCLE ******##########################
  path('customer/recycle/',views.recycle),
  path('customer/recycle/rmonth/',views.rmonth),
  path('customer/recycle/rcycle/',views.rcycle),
  path('thrift/deposit/acc_dep/recy2/',views.recycle_account),
  path('mycustomers/delete/allrecycles/<int:code>/',views.delete_recycle),


########***********CLOSE ACCOUNT ******##########################
  path('customer/closeacc/',views.closeacc),
  path('customer/closeacc/cmonth/',views.closeaccmonth),
  path('customer/closeacc/cycle/',views.closecycle),
  path('thrift/closeaccount/details/',views.delete_details),
  path('thrift/closeaccount/savechange/<int:code>/',views.savechange),


########***********MANAGE POSTING******##########################
path('customer/manage/allpost/<int:vid>/',views.viewllposts),
path('customer/manpost/manmonth/',views.manmonth),
path('customer/manpost/mancycle/',views.mancycle),
path('customers/mpost/details/',views.mpost_account),
path('customers/mpost/refresh/',views.mpost_refresh),
path('customers/mpost/view/',views.mpost_view),

# path('customers/mpost/yesview/',views.mpost_yes),
# path('customers/mpost/noview/',views.mpost_no),


########***********DELETE WALLET******##########################
path('customer/delete/wallet/',views.delpodel),
path('customer/wlletdelete/yes/<int:vid>/',views.vidsts),





# ##********************THRIFTS ***************************
 path('thrift/addthrift/',views.addthrift),  
     path('thrift/addthrift/account_type/',views.account_type),
     path('thrift/addthrift/putthrift/',views.putthrift),
     path('thrift/viewthrift/',views.viewthrift),
     path('thrift/addthrift/account_view/',views.account_view),
     path('thrift/changethrift/',views.changethrift),
     path('thrift/addthrift/account_change/',views.account_change),
     path('thrift/edit/thrift/',views.edit_thrift_popup),


     path('thrift/rolloverthrift/',views.rolloverthrift),
     
     path('thrift/addthrift/account_history/',views.account_history),





# ##********************THRANSACTIONS ***************************
     path('thrift/payrequest/',views.payrequests),
     path('thrift/deposit/account_dep/',views.account_dep),


    path('thrift/safecount/getcount/',views.getcount),


     path('thrift/requests/cashin/cashier/',views.cashier_cashin), #indirect depo
     


     path('findthrift/',views.autocomplete),
     path('thrift/history/',views.history),

     path('thrift/mystatement/',views.statementtt),

     path('thrift/addmythrift/',views.addmythrift),
     
     path('thrift/unremmitted/',views.unremmitted),

     path('thrift/unremmitted/fa/',views.fa_unremmitted),





    ######LOANS FOR GENERAL SAVINGS ********************

###**************Loan settings******************************
path('loans/settings/home/',views.loanwelcome),
path('loans/settings/loan_set_up/',views.loan_setup),
path('loans/settings/loan_set_up/setgrace/',views.setgrace),
path('loans/settings/loan_set_up/setgrace/ajax/',views.ajaxsetgrace),
path('loans/settings/loan_set_up/setgrace/addgrace/',views.addgrace),
# path('loans/settings/loan_set_up/setgrace/pop/',views.gracepop),
# path('loans/settings/loan_set_up/setgrace/change/',views.changegrace),

path('loans/settings/loan_set_up/setgrace/packageslists/',views.loan_packages),

# path('loans/settings/repayplan/',views.repayplan),



# path('threeb/staff/request_loan/',views.reqloan),

# path('threeb/staff/request_loan/loan_packages/',views.getloanpacks),
# path('threeb/staff/request_loan/repay_packages/',views.getrepaypacks),

# path('threeb/staff/request_loan/individual/',views.loandetails),
# path('threeb/staff/request_loan/apply/',views.apply), 



## Lone Appprovals************
# path('threeb/loans/approve/',views.bookloan),
# path('threeb/loans/approve/log/',views.bookloanlog),

# path('threeb/loans/scenarios/',views.loanscene),

# path('threeb/loans/scena/loanlog/',views.apploanlog),

# path('threeb/loans/scenarios/log/',views.loanscenelog),

# path('threeb/loans/withdraw/',views.withdrawoptions),

# path('threeb/loans/declineoptions/',views.decoptions),

# path('threeb/staff/request_loan/approve/yes/',views.yesapprovaloan),

# path('threeb/staff/request_loan/declines/',views.yesdeclineloan),


# path('threeb/staff/repay_loan/repay/',views.yesrepayloan),
# path('threeb/staff/request_loan/performance/',views.loanperformance),

# path('threeb/staff/request_loan/history/',views.loanhistory),












# ##********************RECONCILIATIONS ESUSU***************************
path('thrift/requests/sales/breakdown/',views.salesdetails), #C/O
path('reconciliation/breakdown/esusu/',views.salesdetails___2), #STATUS

path('thrift/requests/sales/approvedbreakdown/',views.approvvedsalesdetails),
path('reconciliation/breakdown/approvedesusu/',views.salesdetails___3), #STATUS
path('thrift/requests/delete/cusomer/',views.customerdepcancel), #DECLINE 

path('thrift/approvalsmenu/delete/yes/',views.cancelesuyes), #DECLINE YESf
path('thrift/approvalsmenu/delete/no/',views.cancelapprono), #DECLINE NO


path('thrift/requests/recline/',views.reclineme), #RECLINE
path('thrift/recline/yes/',views.reclppro),     #RECLINE YES
path('thrift/recline/no/',views.cancelapprono), #RECLINE NO


path('thrift/reedit/',views.reedit), #bulk approval popoup
path('thrift/approvals/approvebulk/',views.approvebulkcash), #bulk approval

# ##********************RECONCILIATIONS SAVINGS***************************
path('reconciliation/view/breakdown/',views.gen_save_details),
path('reconciliation/view/breakdown2/',views.gen_save_details_2),
path('reconciliation/decline/option/',views.savecanopt),
path('reconciliation/decline/option/yes/',views.cancelgensaveyes),
path('reconciliation/decline/option/no/',views.cancelgensaveyno),



path('reconciliation/requests/recline/',views.reclinesave),
path('thrift/reconciliation/recline/yes/',views.reclgensaveppro),
path('thrift/reconciliation/recline/no/',views.cancelrec),



path('reconciliation/reconcile/all/',views.apreedit),
path('reconciliation/bulkreconcile/',views.bulkrecon),

    

path('thrift/remittals/',views.individual),
 path('thrift/seedit/',views.seedit),




path('thrift/requests/adminpayfund/withdraw/',views.withdrawoptions),


path('thrift/aprrovals/approvalsingletrans/',views.approveone),
    
path('thrift/report/',views.report),





    path('thrift/approvalsmenu/',views.approvalsmenu),


        path('thrift/approvalsmenu/approvefund/',views.approvecash),

    path('thrift/allapprovals/',views.allapproval),

    path('thrift/approvals/approvereport/',views.approvereport),

    path('thrift/approvalforindv/',views.approveind),
    path('thrift/approvalsmenu/approvefundforcustomer/',views.approveindividualcash),







# ##********************SAVINGS REPORTS ***************************

  path('thrift/reports/home/',views.repome),

# ##********************END OF DAY ***************************
  path('thrift/reports/sales/cashier/',views.cashierreport),


# ##******************** VAULTS ***************************
 path('thrift/reports/sales/merchant/',views.merchantreport),

  
# ##******************** PROFITS ***************************
  path('thrift/reports/sales/admn/',views.adminreport),

    path('thrift/reports/getdetailprofit/',views.getdetailprofit),
    path('thrift/reports/getdetailloans/',views.getdetailloans),

# ####customer edit *****************
path('customer/editname/',views.editcusnamepop),
path('customer/viewwallet/editname/',views.editcusname),

 
path('customer/editemail/',views.editcusemailpop),
path('customer/viewwallet/editemail/',views.editemail),


path('customer/editphone/',views.editcusphonelpop),
path('customer/viewwallet/editphone/',views.editphone),

  path('thrift/reports/getdatemereport/',views.getmereportajaxdate),

path('customer/editlocation/',views.editlocationpop),
path('customer/viewwallet/editlocation/',views.editlocation),


path('customer/editaddr/',views.editaddrpop),
path('customer/viewwallet/editaddr/',views.editaddr),


path('customer/editstatus/',views.editstapop),
path('customer/viewwallet/editstatus/',views.editsta),



  path('thrift/reports/getunremcash/',views.getunremcash),





###LOAN********************

     path('thrift/loan/home/',views.LOANHOME),



     #*************** activity log********************

     path('thrift/log/',views.log),
     
     path('thrift/log/autopostlog/',views.fillmerchantb),



     path('thrift/log/payouts/autopostlog/',views.fillmerchantb),

     

     path('thrift/log/approvals/',views.logapprove),
     path('thrift/log/approvals/autopostlog/',views.showtrans),




     



     

     


# #      #*************** WITHDRAWAL ********************
     path('thrift/cashout/',views.cashout),






###***************************Payout***************
      path('thrift/payouts/',views.payout),
       path('thrift/requests/adminpayfund/',views.adminpayfund),
      path('thrift/payoutreport/',views.payoutreport),

      path('thrift/requests/adminpayfund/cancel/nos/',views.cancelreq),
      path('thrift/payouts/adminwithdraw/yes/',views.withdrawfunds),


#####***********************withdrawals*********************************   



            #******merchants*******

      path('thrift/reports/getmyname/',views.getmerchantname),


      #*****Cashier**************
      path('thrift/reports/getcashid/',views.getcashid),
      path('thrift/reports/getcashname/',views.getcashname),
       path('thrift/reports/getcashreport/',views.getcashreportajax),

      #****Admin***************
      path('thrift/reports/getadminid/',views.getadminid),
      path('thrift/reports/getadminname/',views.getadminname),
      path('thrift/reports/getadminreport/',views.getadminreportajax),
    
###*****************************MISC************************
    path('thrift/misc/customers/',views.customerslist),
    # path('thrift/misc/namesearch/',views.namesearch),
    path('thrift/misc/switches/',views.switches),
    path('thrift/misc/getstaff/',views.getallstall),
    path('thrift/misc/getswitch/',views.getbutton),
    path('thrift/misc/showselect/',views.openoption),

path('daily_contribution/sms//',views.mysmss),
    
    ]
