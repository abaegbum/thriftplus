"""
URL configuration for thriftplus project.

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import include, path





from thriftplus.views import *


urlpatterns = [


    path("", index),
    path('admin/', admin.site.urls),
    path('login/user/', login),
    path('login/', index),

    path('dashboard/', dashboard),
    path('switch/', switchuser),
    path('changepass/', changepass),






    # ##******************** HOW IT WORKS ****************************
   path('howitworks/',howitworks),


    path('backoffice/password/reset/', passreset),

    # path('backoffice/password/reset/', passreset, name='password_reset'),

    # ##******************** SUBSCRIPTION ****************************
    path('subscription/', subscription),
    path('renews/', renews),
    path('renews/sub/', renewsub),

    path('extension/', extension),
    path('currentsubscription/', currentsubscription),
    path('subty/', subty),
    path('send/', sendp),
    path('sendit/', sendit),
    path('addextension/', edit_sub),
    path('change/', delsubappl),
    path('logout/', logoutuser),


# ##******************** INTEGRITY ****************************
  path('integrity/',integrity),
  path('integrity/report/',rrep),
  path('integrity/ajo/',ajointegrity),
  path('ledgerdetails/',repost),
  path('thrift/admin/vintegrity/',vintegrity),


    # path('home/', dashboard_client),
    # path('dashboard/name_search_ajax/', namesearch),
    # path('dashboard/search/details/', cusdetailS),


    path('customer/', include('customer.urls')),
    path('fts/', include('Ia.urls')),
    # path('vts/', include('Ib.urls')),
    # path('IIIa/', include('IIIa.urls')),
    # # path('IIIb/', include('IIIb.urls')),
    # # path('loans/', include('loans.urls')),
    path('sms/', include('sms.urls')),
    # path('savings/', include('savings.urls')),
    path('staff/', include('staff.urls')),
    # path('corperative/', include('corperative.urls')),
    path('partner/', include('partner.urls')),
    path('sysadmin/', include('sysadmin.urls')),
]
