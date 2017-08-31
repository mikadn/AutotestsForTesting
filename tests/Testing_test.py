#! /usr/bin/env python
# -*- coding: utf-8 -*-
import random
import string
import time

import allure

import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import Globals

from schemes.balance import BalanceScheme
from workSqliteDb import SqliteDb
from workWithRestApi import WorkWithApi




class Test_api:

    @allure.MASTER_HELPER.feature('Тестовое задание')
    @allure.MASTER_HELPER.story('Тестирование изменения баланса клиента при подключении услуги')
    def test_edit_balance_client(self):
        with allure.MASTER_HELPER.step('\nШаг 1 Подключение к БД'):
            sqliteDb = SqliteDb()
            connect = sqliteDb.connectDB(Globals.PATH_DB)

        with allure.MASTER_HELPER.step('Шаг 2 Получить клиента с положительным балансом'):
            clientScheme, balanceScheme = self.getClientWithPositiveBalance(connect)

        with allure.MASTER_HELPER.step('Шаг 3 Получить список подключённых клиенту услуг'):
            workWithApi = WorkWithApi()
            serviceClientJson = workWithApi.postListClientServiceForClient(clientScheme.client_id)
        with allure.MASTER_HELPER.step('Шаг 4 Получить список всех услуг'):
            serviceJson = workWithApi.getListService()
        with allure.MASTER_HELPER.step('Шаг 5 В списке всех доступных услуг найти неподключенную для данного клиента услугу'):
            service = self.findNotConnectServiceForClient(connect, serviceJson, serviceClientJson)
        with allure.MASTER_HELPER.step('Шаг 6 Подключить услугу клиенту'):
            workWithApi.postAddServiceClient(clientScheme.client_id, service['id'])
        with allure.MASTER_HELPER.step('Шаг 7 Выполнять ожидание до тех пор, пока не появится новая услуга в течении 1 минуты'):
            self.waitAddServiceClient(clientScheme.client_id, service)
        with allure.MASTER_HELPER.step('Шаг 8 Выбрать из БД баланс клиента'):
            sqliteDb = SqliteDb()
            clientSchemeNew, balanceSchemeNew = sqliteDb.selectClientWithBalance(connect, clientScheme.client_id)
        with allure.MASTER_HELPER.step('Шаг 9 Сравнить: {конечный баланс} = {начальный баланс} - {стоимость подключения услуги}'):
            assert balanceSchemeNew.balance == balanceScheme.balance - service['cost']
            sqliteDb.close(connect)

    def generateString(self, listSimbols, length):
        return ''.join(random.choice(listSimbols) for x in range(length))

    def getClientWithPositiveBalance(self, connect):
        sqliteDb = SqliteDb()
        clientScheme, balanceScheme = sqliteDb.selectClientWherePositiveBalance(connect)
        if clientScheme.client_id == None:
            clientScheme.client_name = self.generateString(string.ascii_letters, 16)
            sqliteDb.insertClient(connect, clientScheme)
            balanceScheme = BalanceScheme
            balanceScheme.client_client_id = clientScheme.client_id
            balanceScheme.balance = 5.00
            sqliteDb.insertBalance(connect, balanceScheme)
        return clientScheme, balanceScheme

    def findNotConnectServiceForClient(self, connect, serviceJson, serviceClientJson):
        if(len(serviceClientJson['items'])==0):
            return serviceJson['items'][0]
        find = False
        for service in serviceJson['items']:
            for serviceClient in serviceClientJson['items']:
                if int(service['id'])!=int(serviceClient['id']):
                    find = True
                else:
                    find = False
                    break
            if find == True:
                print 'У клиента нет услуги {0}'.format(service)
                return service
        sqliteDb = SqliteDb()
        sqliteDb.insertService(connect, self.generateString(string.ascii_letters, 16), self.generateString(string.digits, 1))

    def waitAddServiceClient(self, client_id, service):
        timeWait = 0
        workWithApi = WorkWithApi()
        while timeWait!=60:
            listServiceClient = workWithApi.postListClientServiceForClient(client_id)
            for serviceClient in listServiceClient['items']:
                if int(serviceClient['id'])==int(service['id']):
                    print 'Услуга добавилась'
                    return True
            time.sleep(5)
            timeWait=timeWait+5
        print 'Услуга не добавилась'
        return False








