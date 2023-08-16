# Import libraries
import os
import sys

# Append directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import user and database modules
from model.user import user
from db.user_db import user_db

# Class for user
class user_bean :

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Constructor to build user object~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def __init__(self, username:str='', password:str='') :
        """Creates an instance of the class

        Args:
            username (str, optional): Username for the user. Defaults to ''.
            password (str, optional): Password for the user. Defaults to ''.
        """
        self.user       = user(username, password)
        self.user_db    = user_db()    
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Function to set objects~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Set the user object~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def set_user(self, id:int='', username:float=0, password:float=0) :
        """Sets the user details.

        Args:
            id (int, optional): User ID. Defaults to ''.
            username (float, optional): Username. Defaults to 0.
            password (float, optional): Password. Defaults to 0.
        
        Returns:
            object: Instance of the class itself
        """
        self.user.set_id(id=id)
        self.user.set_username(username=username)
        self.user.set_password(password=password)
        return self
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Common functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Check if the username / password is exact and build user object~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def connect(self, username, password) -> bool:
        """Checks if the username/password combination exists in the database

        Args:
            username (string): username
            password (string): password
        
        Returns:
            boolean: True if connection was successful, false otherwise
        """
        if self.is_exist(username) :
            if password == self.get_user().get_password() :
                return True
        self.destruct_user()
        return False
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Check if the user exist and build user object~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

    def is_exist(self, username)-> bool:
        """Checks if a user exists

        Args:
            username (string): username
        
        Returns:
            user | False: if user exists returns user object, False if user doesn't exist
        """
        return self.get_user(username=username)        
        
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Destruct the user object~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def destruct_user(self) :
        """Destroy user object
        """
        self.set_user(id=-1, username='', password='')
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Find the ID for the user~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_user_id(self) -> int:
        """Gets the user ID from the database
        
        Returns:
            int: ID corresponding to the user
        """
        this_id = self.user_db.get_user_id()
        if this_id != None :
            if len(this_id) != 0 :
                if this_id[0] != None :
                    return this_id[0] + 1
        return 0
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CRUD and Form of User~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Select all the users~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def select_all(self):
        """Gets all users from the database
        
        Returns:
            List: List containing all users in the database
        """
        return self.user_db.select_all()
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Select the user by username~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_user(self, username:str='') -> user :
        """
        Retrieves a user's information from the user_db.
        If no username is specified, the user's current info will be returned.
        Returns an instance of User on success; else False
        """
        try :
            username = username if username != '' else self.user.get_username()
            tmp_user = self.user_db.get_user(username=username)
            self.user.set_id(tmp_user[0])
            self.user.set_username(tmp_user[1])
            self.user.set_password(tmp_user[2])
            return self.user
        except :
            return False
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create one user~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
        
    def create_user(self, user:user='') -> user:
        """
        Creates a new user and stores it in user_db.
        If no user is specified the current user will be used.
        Returns an instance of User on success;
        """
        user = user if user != '' else self.user
            
        this_id = self.get_user_id()
        self.user.set_id(this_id)
        self.user_db.create_user(self.user)
            
        tmp_user = self.user_db.get_user(username=self.user.get_username())
        self.user.set_id(tmp_user[0])
        self.user.set_username(tmp_user[1])
        self.user.set_password(tmp_user[2])
        return self.user
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Update one user~~~~~~~~~~~~~~~~~~~~~~~~~~~~##   

    def update_user(self, user:user) :
        """
        Updates an existing user record in the user_db.
        """
        self.user_db.update_user(user)
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delete one user~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

    def delete_user(self, user:user) :
        """
        Deletes an existing user record from the user_db.
        """
        self.user_db.delete_user(user) 