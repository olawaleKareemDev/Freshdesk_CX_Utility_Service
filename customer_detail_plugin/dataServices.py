import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime, timedelta
import os
from email_validator import validate_email, EmailNotValidError
import re
import sys
from sqlalchemy import create_engine
import psycopg2 




class DataExtraction:

    def __init__(self) -> None:
        pass
       


    def get_payload(self, email):

        try:
            print("in get payload")


            print(os.environ.get("REDSHIFT_DB_HOST"), os.environ.get("REDSHIFT_DB_PORT"))

            conn =psycopg2.connect(
                host=os.environ.get("REDSHIFT_DB_HOST"),
                user=os.environ.get("REDSHIFT_DB_USER"),
                password=os.environ.get("REDSHIFT_DB_PASSWORD"),
                database = os.environ.get("REDSHIFT_DB_NAME"),
                port=os.environ.get("REDSHIFT_DB_PORT")
            )


            

            print("connected successfully")

        except Exception as e:
            print(e)
            print('errors')

        pd.set_option('display.max_columns', None)
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        
        data = pd.read_sql_query(f'''
                        select
                        clt.email_address as email,
                        clt.firstname,
                        clt.middlename,
                        clt.lastname as surname,
                        clt.client_tier,
                        clt.mobile_number as phoneNo,
                        clt.date_of_birth as dateOfBirth,
                        acc.account_no as accountNumber,
                        acc.product_name as productName
                        from dwh_all_clients clt
                        left join dwh_all_accounts acc on acc.client_id = clt.client_id
                        where email like '%%{email}%%'
                        
                        ''', conn)
        
        return data


    def refine(self, email):
        
        data = self.get_payload(email)
                
        if len(data) == 0:
            try:
                first_half = email.split('.')[0]
                second_half = email.split('.')[1]
                second_half_first_letter = second_half[0]

                if second_half_first_letter.islower():

                    email = first_half +'.'+second_half.capitalize()
                    data = self.get_payload(email)
                    # print('data', data, email)

                if second_half_first_letter.isupper():
                    second_half = second_half[0].lower() + second_half[1:]
                    email = first_half + '.' + second_half
                    data = self.get_payload(email)
            except Exception as e:
                print(e)
                data = []
                return data

        return data


    def get_client_details(self, email):
        
        data = self.get_payload(email)
        
        if len(data) == 0:
            
            
            first_letter = email[0]
            rest_email = email[1:]
            
            if first_letter.islower():
                email = first_letter.upper()+rest_email
                data = self.refine(email)
                
                if len(data) == 0:
                    email = first_letter+rest_email
                    data = self.refine(email)
                                                    
                
            if first_letter.isupper():
                email = first_letter.lower()+rest_email
                data = self.refine(email)
                
                if len(data) == 0:
                    email = first_letter + rest_email
                    data = self.refine(email)
            
        return data

        
   



data_service = DataExtraction()