from django.urls import path
from .views import *


urlpatterns =[

    path('details', CustomerDetailsViewSet.as_view({
        'get': 'get_client_details'
    }), name='freshdesk-get-client-details'),

]