from django.http import HttpResponse
from .dataServices import DataExtraction
from datetime import date, timedelta, datetime
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from customer_detail_plugin  import dataServices 
from customer_detail_plugin import serializers

class CustomerDetailsViewSet(viewsets.ViewSet):
    # serializer_class = serializers.CustomerSerializer

    def get_client_details(self,request):

        print('in here details')

        email=request.GET.get('email')

        sql_injection_list = [
            '',"", "select", "select from", "';", "--'", 
            "'; select true; --", "select true;"
        ]

        if email in sql_injection_list or email==None:
            return {}
        
        else:
                    
            try:


                df = dataServices.data_service.get_client_details(email)
                data = df
                    
                accountNumbers = data.get("accountnumber")
                productNames = data.get("productname")
                accountTiers = data.get("client_tier")

                account_infos = { f"{i}":{"accountNumber":int(accountNumbers[i]), "productName":productNames[i], "accountTier": accountTiers[i]  } for i in range(len(data.get("accountnumber")))}

                return_data = {

                    "email": data.get("email")[0],
                    "firstName": data.get("firstname")[0],
                    "middleName": data.get("middlename")[0],
                    "surname": data.get("surname")[0],
                    "phoneNo": data.get("phoneno")[0],
                    "dateOfBirth": data.get("dateofbirth")[0],

                    "accountRecord":{
                        "accounts": {
                            "account": account_infos
                        }
                    }
                }

                return Response(status=status.HTTP_200_OK, data=return_data)

            except Exception as e:
                print(e)
                return Response(
                    status=status.HTTP_400_BAD_REQUEST, 
                    data={}
                )


