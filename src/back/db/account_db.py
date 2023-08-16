import os
import sys
import sqlite3
import mysql.connector

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import conf        

class account_db :
    
    def __init__(self) :
        self.db = mysql.connector.connect(
            host      = conf.host,
            user      = conf.user,
            password  = conf.password,
            database  = conf.database
        )
            
        self.cursor = self.db.cursor(buffered=True)
        # self.db         = sqlite3.connect(conf.connect_db_sqlite)
        # self.cursor     = self.db.cursor()
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Find If The Account Is Origin Or Destination~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def is_origin(self, account) :
        request = "SELECT * FROM {} WHERE account_id = '{}'".format(conf.account_orig_table_name,
                                                                   account.get_id())
        self.cursor.execute(request)
        
        return True if len(self.cursor.fetchall()) != 0 else False
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read The Last Id For Create The Account~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_account_id(self) :
        
        request = "SELECT account_id FROM {} ORDER BY account_id DESC".format(conf.account_table_name)        
        self.cursor.execute(request)
        return self.cursor.fetchone()  
    
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CRUD Account~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read One Account~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_account(self, account) :
        request = "SELECT * FROM {} WHERE account_id = '{}'".format(conf.account_table_name,
                                                                   account.get_id())
        self.cursor.execute(request)
        return self.cursor.fetchone()
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read All Account~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def select_all(self) :
        request = "SELECT * FROM {}".format(conf.account_table_name)        
        self.cursor.execute(request)
        return self.cursor.fetchall()
      
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create One Account~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def create_account(self, account, is_orig) :
        table_is_orig = conf.account_orig_table_name if is_orig else conf.account_dest_table_name
        
        request     = "INSERT INTO {} (account_id, account_name, old_balance, new_balance) VALUES ('{}', '{}', '{}', '{}')".format(conf.account_table_name,
                                                                                                                            account.get_id(),
                                                                                                                            account.get_name(), 
                                                                                                                            account.get_old_balance(),
                                                                                                                            account.get_new_balance())
        
        
        request_bis = "INSERT INTO {} (account_id) VALUES ('{}')".format(table_is_orig, account.get_id())
         
        self.cursor.execute(request)
        self.cursor.execute(request_bis)
        self.db.commit()
        
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Update One Account ~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def update_account(self, account, is_orig) :
        table_is_orig       = conf.account_orig_table_name if is_orig else conf.account_dest_table_name
        table_is_orig_old   = conf.account_orig_table_name if self.is_origin(account) else conf.account_dest_table_name
        
        request     = "UPDATE {} SET account_name = '{}', old_balance = '{}', new_balance = '{}' WHERE account_id = '{}'".format(conf.account_table_name,
                                                                                                                                account.get_name(),
                                                                                                                                account.get_old_balance(),
                                                                                                                                account.get_new_balance(),
                                                                                                                                account.get_id())
        
        if table_is_orig != table_is_orig_old :
            request_bis     = "DELETE FROM {} WHERE account_id = '{}'".format(table_is_orig_old, account.get_id())
            request_ter     = "INSERT INTO {} (account_id) VALUES ('{}')".format(table_is_orig, account.get_id())
            self.cursor.execute(request_bis)
            self.cursor.execute(request_ter)

        
        self.cursor.execute(request)
        self.db.commit()
        
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delete One Account~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def delete_account(self, account, is_orig) :
        table_is_orig = conf.account_orig_table_name if is_orig else conf.account_dest_table_name
        
        request     = "DELETE FROM {} WHERE account_id = '{}'".format(conf.account_table_name, account.get_id())
        request_bis = "DELETE FROM {} WHERE account_id = '{}'".format(table_is_orig, account.get_id())
        
        self.cursor.execute(request)
        self.cursor.execute(request_bis)
        self.db.commit()