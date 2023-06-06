from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

# gpt
from django.shortcuts import render
from django.utils import timezone
import threading
# from emergency_api.celery import app
# from celery import shared_task


# Create your views here.
import requests
import pandas as pd
from bs4 import BeautifulSoup
## 응급실 open api

#인증키
decoidng_key = 'oQNTMIPdTOg3f/loEXpq7uduydvqoo78gulfKKE4B83EAlaZ0yccwi61w2AOcYIWGxoncf7aB1vMSbvRczS/Lg=='
# 위치기반 응급실 불러오기
def get_api_xy(key, Lon, Lat):
    #API 이름 주소
    url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService'
    #query 넣어야 하는것
    params = {"serviceKey": key,
              'WGS84_LON' : str(Lon),
              'WGS84_LAT' : str(Lat),
              'numOfRows' : '100'}
    #API 상세기능 목록
    PATH = "getEgytLcinfoInqire"
    URL = f"{url}/{PATH}"
    response = requests.get(URL, params=params)
    try:
        app = BeautifulSoup(response.content, 'xml')
    except:
        app = "errorMUGxy"
    return app
def get_api_xy(key, Lon, Lat):
    url = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService'
    params = {
        "serviceKey": key,
        'WGS84_LON': str(Lon),
        'WGS84_LAT': str(Lat),
        'numOfRows': '100'
    }
    PATH = "getEgytLcinfoInqire"
    URL = f"{url}/{PATH}"
    response = requests.get(URL, params=params)
    try:
        app = BeautifulSoup(response.content, 'xml')
    except Exception as e:
        app = None
        print("An error occurred while parsing XML:", e)
    return app


class Emergency_Room_finder(APIView):
    def refresh_data(self):
        print("refreshin start",timezone.now())
        open_app = get_api_now(decoidng_key)
        api_data = []
        for item in open_app.findAll('item'):
            row = {}
            for tag in item.find_all():
                row[tag.name] = tag.text
            api_data.append(row)

        df_now = pd.DataFrame(api_data)
        Emergency_Room.objects.all().delete()
        for idx, row in df_now.iterrows():
            if pd.isna(row["hvs01"]): 
                row["hvs01"] = 0
            if pd.isna(row["hvec"]): 
                row["hvec"] = 0
            Emergency_Room.objects.create(
                hospital_name= row["dutyName"],
                phone=row["dutyTel3"],
                bed_number=row["hvs01"],
                bed_number_now=row["hvec"],
                distance_km=30)
        print("refreshin done",timezone.now())
        # Schedule the next refresh in 1 hour
        # print("refreshing done?", self.last_refreshed, "???")
        # threading.Timer(3600, self.refresh_data).start()
        # threading.Timer(40, self.refresh_data).start()
    # 기록 추출
    def get(self, request, lon, lat, format=None):
        # self.refresh_data()
        if len(Emergency_Room.objects.all()) == 0:
            self.refresh_data()
        open_api = get_api_xy(decoidng_key, lon, lat)
        if int(open_api.findAll('totalCount')[0].text) != 0:
            api_data = []
            for item in open_api.findAll('item'):
                row = {}
                for tag in item.find_all('dutyName'):
                    row[tag.name] = tag.text
                api_data.append(row)

            df_xy = pd.DataFrame(api_data)
            data = Emergency_Room.objects.filter(hospital_name__in = list(df_xy['dutyName']))
        data = Emergency_Room.objects.all()
        serializer = Emergency_RoomSerializer(data, many=True, context={"request": request})
        return Response(serializer.data)
    
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls the 'refresh_data' task every hour
#     print("refresh!")
#     sender.add_periodic_task(crontab(minute=39), Emergency_Room_finder.refresh_data.s())    
# df_xy = df_xy.rename(columns={
#     "dutyName": "hospital_name",
#     "dutyAddr": "address",
#     "hv1": "phone",
#     "HVS01": "bed_number",
#     "hvec": "bed_number_now"
# })
# # Add new columns to the DataFrame
# df_xy = df_xy.assign(distance=0, description="")
# # Remove columns from the DataFrame
# df_xy = df_xy.drop(columns=["extra_column"])
# Emergency_Room.objects.filter(hospital_name__in=list(df_xy['hospital_name'])).delete()
# Emergency_Room.objects.bulk_create(df_xy.to_dict('records'))