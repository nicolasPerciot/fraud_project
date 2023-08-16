import os
import sys
import sqlite3
import mysql.connector

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import conf        

class transaction_db :
    
    def __init__(self) :
        self.db = mysql.connector.connect(
            host      = conf.host,
            user      = conf.user,
            password  = conf.password,
            database  = conf.database
        )
        self.cursor = self.db.cursor(buffered=True)
        # self.db  = sqlite3.connect(conf.connect_db_sqlite)
        # self.cursor = self.db.cursor()
        
        
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read The Last Id For Create The Transaction~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
       
    def get_transaction_id(self) :
        
        request = "SELECT transaction_id FROM {} ORDER BY transaction_id DESC".format(conf.transaction_table_name)        
        self.cursor.execute(request)
        return self.cursor.fetchone()
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CRUD Transaction~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read One Transaction~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_transaction(self, id) :
        request = "SELECT * FROM {} WHERE transaction_id = '{}'".format(conf.transaction_table_name, id)
        self.cursor.execute(request)
        return self.cursor.fetchone()
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read All Transaction for one user ~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_transactions(self, user_id) :
        request = "SELECT * FROM {} WHERE user_id = '{}' ORDER BY transaction_id".format(conf.transaction_table_name, user_id)
        self.cursor.execute(request)
        return self.cursor.fetchall()
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read All Transaction ~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def select_all(self) :
        request = "SELECT * FROM {}".format(conf.transaction_table_name)        
        self.cursor.execute(request)
        return self.cursor.fetchall()
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create One Transaction ~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def create_transaction(self, transaction, user, account_orig, account_dest) :
        request = """INSERT INTO {} (account_id_orig, account_id_dest, user_id, transaction_id, step, type, amount, isFraud) 
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');""".format(conf.transaction_table_name, account_orig.get_id(), 
                                                                                    account_dest.get_id(), user.get_id(), transaction.get_id(),
                                                                                    transaction.get_step(), transaction.get_trans_type(),
                                                                                    transaction.get_amount(), transaction.get_is_fraud())        
        self.cursor.execute(request)
        self.db.commit()
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Update One Transaction ~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def update_transaction(self, transaction, user, account_orig, account_dest) :
        request = """UPDATE {} SET account_id_orig = '{}', account_id_dest = '{}', user_id = '{}', step = '{}', type = '{}', amount = '{}', 
                    isFraud = '{}' WHERE transaction_id = '{}'""".format(conf.transaction_table_name, account_orig.get_id(), 
                                                                            account_dest.get_id(), user.get_id(),
                                                                            transaction.get_step(), transaction.get_trans_type(),
                                                                            transaction.get_amount(), transaction.get_is_fraud(),
                                                                            transaction.get_id())
        self.cursor.execute(request)
        self.db.commit()
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delete One Transaction ~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def delete_transaction(self, transaction) :
        request = "DELETE FROM {} WHERE transaction_id = '{}'".format(conf.transaction_table_name, transaction.get_id())

        self.cursor.execute(request)
        self.db.commit()