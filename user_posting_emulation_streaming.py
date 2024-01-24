import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text


random.seed(100)


class AWSDBConnector:

    def __init__(self):
        '''
        Class connects to AWS RDS and returns connection engine.
        '''

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()

#  Define a function that uses the connection engine to extract posting, geo-location and user data from AWS DB and streams it to AWS Kinesis. 
def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

                #To send JSON messages you need to follow this structure
                invoke_url = "https://afm0un5nrb.execute-api.us-east-1.amazonaws.com/PDP-Mile-9-Task-2/stream/streaming-0e172e8c4bc3-pin/record"
                payload = json.dumps({
                    "StreamName": "streaming-0e172e8c4bc3-pin",
                    "Data": {
                        #Data should be send as pairs of column_name:value, with different columns separated by commas      
                        "index": pin_result["index"], "unique_id": pin_result["unique_id"], "title": pin_result["title"], "description": pin_result["description"], "poster_name": pin_result["poster_name"],
                        "follower_count": pin_result["follower_count"], "tag_list": pin_result["tag_list"], "is_image_or_video": pin_result["is_image_or_video"], "image_src": pin_result["image_src"], 
                        "downloaded": pin_result["downloaded"], "save_location": pin_result["save_location"], "category": pin_result["category"]
                        },
                        "PartitionKey": "PK-pin"
                        })
                headers = {'Content-Type': 'application/json'}
                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print(response.status_code)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

                #To send JSON messages you need to follow this structure
                invoke_url = "https://afm0un5nrb.execute-api.us-east-1.amazonaws.com/PDP-Mile-9-Task-2/stream/streaming-0e172e8c4bc3-geo/record"
                payload = json.dumps({
                    "StreamName": "streaming-0e172e8c4bc3-geo",
                    "Data": {
                        #Data should be send as pairs of column_name:value, with different columns separated by commas      
                        "index": geo_result["ind"], "timestamp": str(geo_result["timestamp"]), "latitude": geo_result["latitude"], "longitude": geo_result["longitude"], "country": geo_result["country"]
                        },
                        "PartitionKey": "PK-geo"
                        })
                headers = {'Content-Type': 'application/json'}
                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print(response.status_code)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)

                #To send JSON messages you need to follow this structure
                invoke_url = "https://afm0un5nrb.execute-api.us-east-1.amazonaws.com/PDP-Mile-9-Task-2/stream/streaming-0e172e8c4bc3-user/record"
                payload = json.dumps({
                    "StreamName": "streaming-0e172e8c4bc3-user",
                    "Data": {
                        #Data should be send as pairs of column_name:value, with different columns separated by commas      
                        "index": user_result["ind"], "first_name": user_result["first_name"], "last_name": user_result["last_name"], "age": user_result["age"], "date_joined": str(user_result["date_joined"])
                        },
                        "PartitionKey": "PK-user"
                        })
                headers = {'Content-Type': 'application/json'}
                response = requests.request("PUT", invoke_url, headers=headers, data=payload)
                print(response.status_code)
            
            print(pin_result)
            print(geo_result)
            print(user_result)


if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    
