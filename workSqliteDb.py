#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

from schemes.client import ClientScheme

from schemes.balance import BalanceScheme
import allure

class SqliteDb:

    def connectDB(self, path_db):
        try:
            connect = sqlite3.connect(path_db)
            return connect
        except sqlite3.Error:
            print ()
            assert False

    def close(self, connect):
        connect.close()

    def selectClientWherePositiveBalance(self, connect):
        try:
            cursor = connect.cursor()
            script = 'SELECT CLIENT_ID, CLIENT_NAME, BALANCE FROM CLIENTS ' \
                  'INNER JOIN BALANCES ON CLIENTS.CLIENT_ID = BALANCES.CLIENTS_CLIENT_ID ' \
                  'WHERE BALANCES.BALANCE>0 ORDER BY random() LIMIT 1;'
            cursor.execute(script)
            client = cursor.fetchall()
            print 'Запрос {0} вернул {1}'.format(script, client)
            allure.MASTER_HELPER.attach('Запрос {0}'.format(script), '{0}'.format(client))
            clientScheme = ClientScheme
            balanceScheme = BalanceScheme
            if(len(client) is not 0):
                (clientScheme.client_id, clientScheme.client_name, balanceScheme.balance) = client[0]
            balanceScheme.client_client_id = clientScheme.client_id
            return clientScheme, balanceScheme
        except sqlite3.Error:
            print 'Запрос {0} провалился'.format(script)
            assert False

    def selectLastInsertRowId(self, connect):
        try:
            cursor = connect.cursor()
            script = 'SELECT last_insert_rowid();'
            cursor.execute(script)
            last_insert_rowid = cursor.fetchall()
            print 'Запрос {0} вернул {1}'.format(script, last_insert_rowid)
            (id, ) = last_insert_rowid[0]
            return id
        except sqlite3.Error:
            print 'Запрос {0} провалился'.format(script)
            assert False

    def insertClient(self, connect, clientScheme):
        try:
            cursor = connect.cursor()
            script = 'INSERT INTO CLIENTS(CLIENT_ID, CLIENT_NAME) VALUES(NULL, \'{0}\');'.format(clientScheme.client_name)
            cursor.execute(script)
            connect.commit()
            print 'Запрос {0} вернул {1}'.format(script, cursor.fetchall())
            clientScheme.client_id = self.selectLastInsertRowId(connect)
        except sqlite3.Error:
            print 'Запрос {0} провалился'.format(script)
            assert False

    def insertBalance(self, connect, balanceScheme):
        try:
            cursor = connect.cursor()
            script = 'INSERT INTO BALANCES(CLIENTS_CLIENT_ID, BALANCE) VALUES(\'{0}\', \'{1}\');'.format(balanceScheme.client_client_id, balanceScheme.balance)
            cursor.execute(script)
            connect.commit()
            print 'Запрос {0} вернул {1}'.format(script, cursor.fetchall())
        except sqlite3.Error:
            print 'Запрос {0} провалился'.format(script)
            assert False

    def selectClientWithBalance(self, connect, clientId):
        try:
            cursor = connect.cursor()
            script = 'SELECT CLIENT_ID, CLIENT_NAME, BALANCE FROM CLIENTS ' \
                  'INNER JOIN BALANCES ON CLIENTS.CLIENT_ID = BALANCES.CLIENTS_CLIENT_ID ' \
                  'WHERE CLIENTS.CLIENT_ID={0};'.format(clientId)
            cursor.execute(script)
            client = cursor.fetchall()
            print 'Запрос {0} вернул {1}'.format(script, client)
            allure.MASTER_HELPER.attach('Запрос {0}'.format(script), '{0}'.format(client))
            clientScheme = ClientScheme
            balanceScheme = BalanceScheme
            if(len(client) != 0):
                (clientScheme.client_id, clientScheme.client_name, balanceScheme.balance) = client[0]
            balanceScheme.client_client_id = clientScheme.client_id
            return clientScheme, balanceScheme
        except sqlite3.Error:
            print 'Запрос {0} провалился'.format(script)
            assert False

    def insertService(self, connect, service_name, cost):
        try:
            cursor = connect.cursor()
            script = 'INSERT INTO SERVICES(SERVICE_ID, SERVICE_NAME, COST) VALUES(NULL, \'{0}\', \'{1}\');'.format(
                service_name, cost)
            cursor.execute(script)
            service = cursor.fetchall()
            print 'Запрос {0} вернул {1}'.format(script, service)
        except sqlite3.Error:
            print 'Запрос {0} провалился'.format(script)
            assert False

