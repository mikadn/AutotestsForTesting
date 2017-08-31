#! /usr/bin/env python
# -*- coding: utf-8 -*-



from Globals import PORT
from Globals import SCHEME
from Globals import URL
import requests
import allure

class WorkWithApi:

    def postListClientServiceForClient(self, clientId):
        try:
            response = requests.post('{0}://{1}:{2}/client/services'.format(SCHEME, URL, PORT),
                                     headers= {'Content-Type':'application/json'},
                                     json= {'client_id':clientId})
            print response.status_code
            print response.text
            assert 200==response.status_code
            json = response.json()
            allure.MASTER_HELPER.attach('Запрос /client/services', ''.format(json))
            return json
        except requests.RequestException:
            print 'Запрос провалился'
            assert False

    def getListService(self):
        try:
            response = requests.get('{0}://{1}:{2}/services'.format(SCHEME, URL, PORT),
                                     headers= {'Content-Type':'application/json'})
            print response.status_code
            print response.text
            assert 200==response.status_code
            allure.MASTER_HELPER.attach('Запрос /client/services', ''.format(response.json()))
            return response.json()
        except requests.RequestException:
            print 'Запрос провалился'
            assert False

    def postAddServiceClient(self, clientId, serviceId):
        try:
            body = {'client_id': clientId, 'service_id': serviceId}
            print 'Тело запроса на добавление услуги {0}'.format(body)
            response = requests.post('{0}://{1}:{2}/client/add_service'.format(SCHEME, URL, PORT),
                                     headers={'Content-Type': 'application/json'},
                                     json=body)
            print response.status_code
            print response.text
            assert 202 == response.status_code
        except requests.RequestException:
            print 'Запрос провалился'
            assert False