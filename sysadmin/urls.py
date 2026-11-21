

from django.urls import path

from . import views

urlpatterns = [






     path('sysadmin/setup/password/', views.setuppas),
     path('sysadmin/setup/password/pop/', views.passpop),     
     path('sysadmin/setup/password/change/', views.changpasspop),

     
     path('sysadmin/setup/locations/', views.location),

     path('sysadmin/popup/location/', views.delloc),
     path('sysadmin/delete/location/<int:vid>/', views.dellocyes),

     

####****************PRODUCTS*********************###########
     path('sysadmin/setup/products/', views.myproduct),
     
####*****************CARDING*********************###########
    path('sysadmin/setup/carding/', views.carding),
    path('sysadmin/setup/carding/pop/', views.freshpop),
    path('sysadmin/setup/carding/pop/save/', views.savefreshpop),


        path('sysadmin/setup/carding/pop/re/', views.repop),
    path('sysadmin/setup/carding/pop/savere/', views.saverepop),


	 ]