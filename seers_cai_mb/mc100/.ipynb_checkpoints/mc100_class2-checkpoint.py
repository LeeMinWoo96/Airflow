#!/usr/bin/env python
# coding: utf-8

# ## mc100 class
# Version 0.1

# In[1]:


import os
import requests
from collections import OrderedDict
import json
# from utils import *

import time
import datetime
import socket
import urllib
import re


# In[2]:


class MC100:
    DOWNLOAD_PATH = '/home/nsc/seers/temp'
    URL_BASE = 'http://13.125.86.65:8080/mobiCARE/cardio'
    USER_ID = 'northstar01'
    USER_PW = 'northstar01'
    PW_ENCRYPTION = 0
    GMT_CODE = 'GMT+0900'
    DEVICE_KIND = 5
    COUNTRY_CODE = 'KR'
    COUNTRY_NAME = 'Korea'
    TIMEZONE = 'Asia/Seoul'
    
    auth_token = None
    ip_wan = None
    ip_lan = None
    request_user_id = None
    organization_id = None
    
    def __init__(self, path=None):
        self.list_measurement = []
        if path is not None:
            MC100.DOWNLOAD_PATH = path
        MC100.ip_lan = socket.gethostbyname(socket.gethostname())
        ip_check = urllib.request.urlopen('http://checkip.dyndns.org').read().decode('utf-8')
        MC100.ip_wan = re.search(re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),ip_check).group() 
#         print ('WAN ip : ' + MC100.ip_wan) 
#         print ('LAN ip : ' + MC100.ip_lan)
        self.login()
        
    def login(self):
        # Make Login message 
        
#         print('asdasdsadsadsadasds')
        URL_API_LOGIN = MC100.URL_BASE + '/Account/Login'
        HEADERS = {'Content-Type': 'application/json; charset=utf-8', 'SX-Client-IP': MC100.ip_wan}

        JSON_LOGIN = OrderedDict()
        JSON_LOGIN["id"] = MC100.USER_ID
        JSON_LOGIN["password"] = MC100.USER_PW
        JSON_LOGIN["encryption"] = MC100.PW_ENCRYPTION
        JSON_LOGIN["systemTime"] = int(time.time())
        JSON_LOGIN["requestDateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        JSON_LOGIN["gmtCode"] = MC100.GMT_CODE
        JSON_LOGIN["deviceKind"] = MC100.DEVICE_KIND
        JSON_LOGIN["countryCode"] = MC100.COUNTRY_CODE
        JSON_LOGIN["countryName"] = MC100.COUNTRY_NAME
        JSON_LOGIN["timezone"] = MC100.TIMEZONE
        TEXT_LOGIN = json.dumps(JSON_LOGIN)

        print('Login - POST request %s' % URL_API_LOGIN)
        res = requests.post(URL_API_LOGIN, data=TEXT_LOGIN, headers=HEADERS)
        res_code = res.status_code
        res_result = False
        response_dic = {}
        if res_code == 200:
            try:
                response_dic = json.loads(res.text)
                if 'error' in response_dic.keys():     
                    if response_dic["error"] == 0:
                        res_result = True
                        MC100.auth_token = response_dic["accessToken"]
                        MC100.organization_id = response_dic['userAccount']["organizationId"]
                        MC100.request_user_id = response_dic['userAccount']["userId"]
            except (ValueError, TypeError) as e:
                print ("post exception : ", e)
                print (res.text)
        elif res_code == 404:
            print ("send error - 404, Retry send cancel.")

#         print (res_result, res_code)
#         print ('organization_id', MC100.organization_id, 'token', MC100.auth_token)
        # print (res.text)
        return res_code
    
    def get_list_measure(self, status):
        if MC100.auth_token is None:
            return 0
        # Make SelectPatientMeasurementInfoByReviewer message 
        URL_API_LIST = MC100.URL_BASE + '/Measurement/SelectPatientMeasurementInfoByReviewer'
        HEADERS = {'Content-Type': 'application/json; charset=utf-8',
                   'SX-Auth-Token': MC100.auth_token,
                   'SX-Client-IP': MC100.ip_wan }

        JSON_LIST = OrderedDict()
        JSON_LIST["requestUserId"] = MC100.request_user_id
        JSON_LIST["organizationId"] = MC100.organization_id
        JSON_LIST["startDateTime"] = '2019-01-01 00:00:00'
        JSON_LIST["endDateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        JSON_LIST["systemTime"] = int(time.time())
        JSON_LIST["requestDateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        JSON_LIST["gmtCode"] = MC100.GMT_CODE
        JSON_LIST["deviceKind"] = MC100.DEVICE_KIND
        JSON_LIST["countryCode"] = MC100.COUNTRY_CODE
        JSON_LIST["countryName"] = MC100.COUNTRY_NAME
        JSON_LIST["timezone"] = MC100.TIMEZONE
        TEXT_LIST = json.dumps(JSON_LIST)

        print('get list measure - POST request %s' % URL_API_LIST)
        res = requests.post(URL_API_LIST, data=TEXT_LIST, headers=HEADERS)
        res_code = res.status_code
        res_result = False
        response_dic = {}
        self.list_measurement = []
        if res_code == 200:
            try:
                response_dic = json.loads(res.text)
                if 'error' in response_dic.keys():     
                    if response_dic["error"] == 0:
                        res_result = True
                        for measurement in response_dic["measurementInfoList"]:
                            if measurement['measurementStatus'] in status:
                                self.list_measurement.append(measurement)
                                
            except (ValueError, TypeError) as e:
                print ("post exception : ", e)
                print (res.text)
        elif res_code == 404:
            print ("send error - 404, Retry send cancel.")
        
#         print (res_result, res_code)
#         print ('count measurement', len(self.list_measurement))
        # print (res.text)
        return res_code
    
    def get_list_ecg(self, list_measurement):
        # Make SelectECGData  message 
        URL_API_ECG = MC100.URL_BASE + '/Measurement/SelectECGData'
        HEADERS = {'Content-Type': 'application/json; charset=utf-8',
                   'SX-Auth-Token': MC100.auth_token,
                   'SX-Client-IP': MC100.ip_wan }

        JSON_ECG = OrderedDict()
        JSON_ECG["requestUserId"] = MC100.request_user_id
        JSON_ECG["organizationId"] = MC100.organization_id
        JSON_ECG["measurementCode"] = ''

        JSON_ECG["systemTime"] = int(time.time())
        JSON_ECG["requestDateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        JSON_ECG["gmtCode"] = MC100.GMT_CODE
        JSON_ECG["deviceKind"] = MC100.DEVICE_KIND
        JSON_ECG["countryCode"] = MC100.COUNTRY_CODE
        JSON_ECG["countryName"] = MC100.COUNTRY_NAME
        JSON_ECG["timezone"] = MC100.TIMEZONE
        TEXT_ECG = json.dumps(JSON_ECG)
        
        for idx, measurement in enumerate(list_measurement):
            measurement_code = measurement['measurementCode']
            JSON_ECG["measurementCode"] = measurement_code
            TEXT_ECG = json.dumps(JSON_ECG)

#             print('get list ecg %s - POST request %s' % (measurement_code, URL_API_ECG))
            res = requests.post(URL_API_ECG, data=TEXT_ECG, headers=HEADERS)
            res_code = res.status_code
            res_result = False
            response_dic = {}
            if res_code == 200:
                try:
                    response_dic = json.loads(res.text)
                    if 'error' in response_dic.keys():     
                        if response_dic["error"] == 0:
                            res_result = True
                            measurement["ecgDataList"] = response_dic["ecgDataList"]
                except (ValueError, TypeError) as e:
                    print ("post exception : ", e)
                    print (res.text)
            elif res_code == 404:
                print ("send error - 404, Retry send cancel.")

#             print (res_result, res_code)
#             if measurement["ecgDataList"] is not None:
#                 print ('count ecg list', len(measurement["ecgDataList"]))
#             print (res.text)
#             print ('')
    
    def get_list_annotation(self, list_measurement):
        # Make SelectAnalysisOutputAnnotationFile  message 
        URL_API_ANNOTATION = MC100.URL_BASE + '/Analysis/SelectAnalysisOutputAnnotationFile'
        HEADERS = {'Content-Type': 'application/json; charset=utf-8',
                   'SX-Auth-Token': MC100.auth_token,
                   'SX-Client-IP': MC100.ip_wan }

        JSON_ANNOTATION = OrderedDict()
        JSON_ANNOTATION["requestUserId"] = MC100.request_user_id
        JSON_ANNOTATION["organizationId"] = MC100.organization_id
        JSON_ANNOTATION["measurementCode"] = ''

        JSON_ANNOTATION["systemTime"] = int(time.time())
        JSON_ANNOTATION["requestDateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        JSON_ANNOTATION["gmtCode"] = MC100.GMT_CODE
        JSON_ANNOTATION["deviceKind"] = MC100.DEVICE_KIND
        JSON_ANNOTATION["countryCode"] = MC100.COUNTRY_CODE
        JSON_ANNOTATION["countryName"] = MC100.COUNTRY_NAME
        JSON_ANNOTATION["timezone"] = MC100.TIMEZONE
        TEXT_ANNOTATION = json.dumps(JSON_ANNOTATION)
        
        for idx, measurement in enumerate(list_measurement):
            measurement_code = measurement['measurementCode']
            JSON_ANNOTATION["measurementCode"] = measurement_code
            TEXT_ANNOTATION = json.dumps(JSON_ANNOTATION)
#             print('get list annotation %s - POST request %s' % (measurement_code, URL_API_ANNOTATION))
            res = requests.post(URL_API_ANNOTATION, data=TEXT_ANNOTATION, headers=HEADERS)
            res_code = res.status_code
            res_result = False
            response_dic = {}
            if res_code == 200:
                try:
                    response_dic = json.loads(res.text)
                    if 'error' in response_dic.keys():     
                        if response_dic["error"] == 0:
                            res_result = True
                            measurement["analysisOutputFileList"] = response_dic["analysisOutputFileList"]
                except (ValueError, TypeError) as e:
                    print ("post exception : ", e)
                    print (res.text)
            elif res_code == 404:
                print ("send error - 404, Retry send cancel.")

#             print (res_result, res_code)
#             if measurement["analysisOutputFileList"] is not None:
#                 print ('count annotation list', len(measurement["analysisOutputFileList"]))
#             print (res.text)
#             print ('')
        
        
    def get_list(self, status):
        self.get_list_measure(status)
        self.get_list_ecg(self.list_measurement)
        self.get_list_annotation(self.list_measurement)
        return
    
    def download_ecg(self, list_measurement):
        # Make DownloadECGFile message 
        URL_API_DOWNLOAD_ECG = MC100.URL_BASE + '/Measurement/DownloadECGFile/{code}:{id}'
        HEADERS = {'Content-Type': 'application/json; charset=utf-8',
                   'SX-Auth-Token': MC100.auth_token,
                   'SX-Client-IP': MC100.ip_wan }
        for idx, measurement in enumerate(list_measurement):
            measurement_code = measurement['measurementCode']
            if measurement['ecgDataList'] is None :
                continue
            path = os.path.join(MC100.DOWNLOAD_PATH, measurement_code)
            measurement['storePath'] = path
            for idx, ecg in enumerate(measurement['ecgDataList']):
                ecg_id = ecg['ecgId']
                URL_API_DOWNLOAD_ECG = MC100.URL_BASE                     + '/Measurement/DownloadECGFile/{code}:{id}'.format(code=measurement_code, 
                                                                        id=str(ecg_id))
                ecg['ECGUrl'] = URL_API_DOWNLOAD_ECG
#                 print (measurement_code, ecg_id)
#                 print (URL_API_DOWNLOAD_ECG)

                res = requests.get(URL_API_DOWNLOAD_ECG, stream=True, headers=HEADERS)
                res_code = res.status_code
                res_result = False
                if res_code == 200:
                    # print (res.headers)
                    content_disposition = res.headers['Content-Disposition']
#                     print (content_disposition)
                    filename = re.findall('filename=.*"([^ ]*)"',content_disposition)[0]
                    ecg['filename'] = filename
#                     print('filename : ', filename)
                    if os.path.isdir(path) is not True:
                        try:
                            os.makedirs(path, exist_ok=True)
                        except OSError as ex:
                            raise
                    
                    with open(os.path.join(path, filename), 'wb') as f:
                        for chunk in res.iter_content(chunk_size=512):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
                elif res_code == 404:
                    print ("send error - 404, Retry send cancel.")

    
    def download_annotation(self, list_measurement):
        # Make DownloadAnaysisOutputFile message 
        URL_API_DOWNLOAD_ANNOTATION = MC100.URL_BASE + '/Analysis/DownloadAnalysisOutputFile/{code}:{id}'
        HEADERS = {'Content-Type': 'application/json; charset=utf-8',
                   'SX-Auth-Token': MC100.auth_token,
                   'SX-Client-IP': MC100.ip_wan }
        
        for idx, measurement in enumerate(list_measurement):
            measurement_code = measurement['measurementCode']
            if measurement['analysisOutputFileList'] is None :
                continue
            path = os.path.join(MC100.DOWNLOAD_PATH, measurement_code)
            measurement['storePath'] = path
            for idx, analysis in enumerate(measurement['analysisOutputFileList']):
                analysis_id = analysis['analysisOutputFileId']
                URL_API_DOWNLOAD_ANNOTATION = MC100.URL_BASE                     + '/Analysis/DownloadAnalysisOutputFile/{code}:{id}'.format(code=measurement_code,
                                                                                id=str(analysis_id))
                analysis['analysisUrl'] = URL_API_DOWNLOAD_ANNOTATION
#                 print (measurement_code, analysis_id)
#                 print (URL_API_DOWNLOAD_ANNOTATION)

                res = requests.get(URL_API_DOWNLOAD_ANNOTATION, stream=True, headers=HEADERS)
                res_code = res.status_code
                res_result = False
                if res_code == 200:
                    # print (res.headers)
                    content_disposition = res.headers['Content-Disposition']
#                     print (content_disposition)
                    filename = re.findall('filename=.*"([^ ]*)"',content_disposition)[0]
                    analysis['filename'] = filename
#                     print('filename : ', filename)
                    
                    if os.path.isdir(path) is not True:
                        try:
                            os.makedirs(path, exist_ok=True)
                        except OSError as ex:
                            raise
            
                    with open(os.path.join(path, filename), 'wb') as f:
                        for chunk in res.iter_content(chunk_size=512):
                            if chunk:  # filter out keep-alive new chunks
                                f.write(chunk)
                elif res_code == 404:
                    print ("send error - 404, Retry send cancel.")
    
    def get_review(self, list_measurement):
        # Make SelectAnalysisBeatClassify message 
        URL_API_ANALYSIS = MC100.URL_BASE + '/Analysis/SelectAnalysisBeatClassify'
        HEADERS = {'Content-Type': 'application/json; charset=utf-8',
                   'SX-Auth-Token': MC100.auth_token,
                   'SX-Client-IP': MC100.ip_wan }

        JSON_ANALYSIS = OrderedDict()
        JSON_ANALYSIS["requestUserId"] = MC100.request_user_id
        JSON_ANALYSIS["organizationId"] = MC100.organization_id
        JSON_ANALYSIS["measurementCode"] = ''
        JSON_ANALYSIS["includeNoise"] = True

        JSON_ANALYSIS["systemTime"] = int(time.time())
        JSON_ANALYSIS["requestDateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        JSON_ANALYSIS["gmtCode"] = MC100.GMT_CODE
        JSON_ANALYSIS["deviceKind"] = MC100.DEVICE_KIND
        JSON_ANALYSIS["countryCode"] = MC100.COUNTRY_CODE
        JSON_ANALYSIS["countryName"] = MC100.COUNTRY_NAME
        JSON_ANALYSIS["timezone"] = MC100.TIMEZONE
        TEXT_ANALYSIS = json.dumps(JSON_ANALYSIS)
              
        for idx, measurement in enumerate(list_measurement):
            measurement_code = measurement['measurementCode']
            JSON_ANALYSIS["measurementCode"] = measurement_code
            TEXT_ANALYSIS = json.dumps(JSON_ANALYSIS)
#             print('get review %s - POST request %s' % (measurement_code, URL_API_ANALYSIS))
            res = requests.post(URL_API_ANALYSIS, data=TEXT_ANALYSIS, headers=HEADERS)
            res_code = res.status_code
            res_result = False
            response_dic = {}
            if res_code == 200:
                try:
                    response_dic = json.loads(res.text)
                    if 'error' in response_dic.keys():     
                        if response_dic["error"] == 0:
                            res_result = True
                            measurement["analysisBeatClassifySimpleList"] = response_dic["analysisBeatClassifySimpleList"]
                except (ValueError, TypeError) as e:
                    print ("post exception : ", e)
                    print (res.text)
            elif res_code == 404:
                print ("send error - 404, Retry send cancel.")

#             print (res_result, res_code)
#             print ('')
    


# In[3]:


if __name__ == '__main__':
    """
    measurementStatus
    0x00 : NONE
    0x01 : RECODING_START
    0x02 : RECODING_END
    0x03 : UPLOAD_COMPLETE
    0x04 : ANALYZING
    0x05 : READY
    0x06 : REVIEWING
    0x07 : COMPLETED
    0x0A : REPORT RELEASE
    0x0F : ERROR
    """
    mc100_target = MC100()
    mc100_target.get_list([0x05, 0x06])
    mc100_target.download_ecg(mc100_target.list_measurement)
    mc100_target.download_annotation(mc100_target.list_measurement)
    
    mc100_complete = MC100()
    mc100_complete.get_list([0x07, 0x0A])
    mc100_complete.download_ecg(mc100_complete.list_measurement)
    mc100_complete.download_annotation(mc100_complete.list_measurement)

    print('--------- complete ---------------------------')
    print(mc100_complete.list_measurement)
    print('--------- target ---------------------------')
    print(mc100_target.list_measurement)
    
    
    mc100_target.get_review(mc100_target.list_measurement)
    if mc100_target.list_measurement[0]['analysisBeatClassifySimpleList'] is not None:
        for beat in mc100_target.list_measurement[0]['analysisBeatClassifySimpleList']:
            if beat['beatClass'] in ['V','F']:
                print(beat)


# In[ ]:




