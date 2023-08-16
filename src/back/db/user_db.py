import os
import sys
import sqlite3
import mysql.connector

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import conf        

class user_db :
    
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
        
        
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read The Last Id For Create The User~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_user_id(self) :
        
        request = "SELECT user_id FROM {} ORDER BY user_id DESC".format(conf.user_table_name)        
        self.cursor.execute(request)
        return self.cursor.fetchone()
    
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CRUD User~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read One User~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_user(self, username) :
        request = "SELECT * FROM {} WHERE username = '{}'".format(conf.user_table_name,
                                                                   username)
        self.cursor.execute(request)
        return self.cursor.fetchone()
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Read All User~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def select_all(self) :
        request = "SELECT * FROM {}".format(conf.user_table_name)        
        self.cursor.execute(request)
        return self.cursor.fetchall()
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create One User~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def create_user(self, user) :
        request = "INSERT INTO {} (user_id, username, password) VALUES ('{}', '{}', '{}')".format(conf.user_table_name,
                                                                                                    user.get_id(),
                                                                                                    user.get_username(), 
                                                                                                    user.get_password())        
        self.cursor.execute(request)
        self.db.commit()
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Update One User~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def update_user(self, user) :
        request = "UPDATE {} SET username = '{}', password = '{}' WHERE user_id = '{}'".format(conf.user_table_name,
                                                                                                user.get_username(), 
                                                                                                user.get_password(),
                                                                                                user.get_id())
        self.cursor.execute(request)
        self.db.commit()
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delete One User~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def delete_user(self, user) :
        request = "DELETE FROM {} WHERE id = '{}'".format(conf.user_table_name, user.get_id())

        self.cursor.execute(request)
        self.db.commit()