import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import conf
from model.account import account
from db.account_db import account_db
from model.transaction  import transaction
from db.transaction_db import transaction_db

class transaction_bean :
    

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Constructor to build all the objects~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def __init__(self, id:int=0, step:int=0, trans_type:str='', amount:float=0, is_fraud:bool=0,
                 id_account_orig:int=0, name_account_orig:str='', old_balance_orig:float=0, new_balance_orig:float=0,
                 id_account_dest:int=0, name_account_dest:str='', old_balance_dest:float=0, new_balance_dest:float=0) -> None :
        
        self.transaction        = transaction(id=id, step=step, trans_type=trans_type, amount=amount, is_fraud=is_fraud)  
        
        self.account_orig        = account(id=id_account_orig, account_name=name_account_orig, old_balance=old_balance_orig, new_balance=new_balance_orig)
        self.account_dest        = account(id=id_account_dest, account_name=name_account_dest, old_balance=old_balance_dest, new_balance=new_balance_dest)      
        
        self.account_db         = account_db()
        self.transaction_db     = transaction_db()
        
          
        
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Function to set objects~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Set the transaction object~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def set_transaction(self, id:int=0, step:int=0, trans_type:str='', amount:float=0, is_fraud:bool=0) :
        self.transaction.set_id(id=id)
        self.transaction.set_step(step=step)
        self.transaction.set_trans_type(trans_type=trans_type)
        self.transaction.set_amount(amount=amount)
        self.transaction.set_is_fraud(is_fraud=is_fraud)
        return self.transaction
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Set the origin account object~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def set_account_orig(self, id:int=0, account_name:int=0, old_balance:float=0, new_balance:float=0) :
        self.account_orig.set_id(id=id)
        self.account_orig.set_name(account_name=account_name)
        self.account_orig.set_old_balance(old_balance=old_balance)
        self.account_orig.set_new_balance(new_balance=new_balance)
        return self.account_orig
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Set the destination account object~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def set_account_dest(self, id:int=0, account_name:int=0, old_balance:float=0, new_balance:float=0) :
        self.account_dest.set_id(id=id)
        self.account_dest.set_name(account_name=account_name)
        self.account_dest.set_old_balance(old_balance=old_balance)
        self.account_dest.set_new_balance(new_balance=new_balance)
        return self.account_dest
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Common functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Check if type is in the list~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def is_form_type(self, type) :
        if type in conf.form_type[-5:] :
            return True
        else :
            return False
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Find the ID for the transaction~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_transaction_id(self) :
        this_id = self.transaction_db.get_transaction_id()
        if this_id != None :
            if len(this_id) != 0 :
                if this_id[0] != None :
                    return this_id[0] + 1
        return 0
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Find the ID for the account~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_account_id(self) :
        this_id = self.account_db.get_account_id()
        if this_id != None :
            if len(this_id) != 0 :
                if this_id[0] != None :
                    return this_id[0] + 1
        return 0
        

    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CRUD and Form of Transaction and Account~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Select all the transactions~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def select_all_transaction(self) :
        return self.transaction_db.select_all()          
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Select the transaction by ID~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_transaction(self, id:int) :
        trans           = self.transaction_db.get_transaction(id=id)
        
        account_orig    = self.account_db.get_account(account=account(id=trans[0]))
        account_dest    = self.account_db.get_account(account=account(id=trans[1]))
            
        trans_bean      = transaction_bean(id=trans[3], step=trans[4], trans_type=trans[5], amount=trans[6], is_fraud=trans[7],
                                        id_account_orig=account_orig[0], name_account_orig=account_orig[1], old_balance_orig=account_orig[2], new_balance_orig=account_orig[3],
                                        id_account_dest=account_dest[0], name_account_dest=account_dest[1], old_balance_dest=account_dest[2], new_balance_dest=account_dest[3])
        return trans_bean
    
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Select all the transactions by user~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def get_transactions(self, user) :
        
        list_transactions       = []
        tmp_list_transactions   = self.transaction_db.get_transactions(user.get_id())
        
        
        for trans in tmp_list_transactions :
            account_orig = self.account_db.get_account(account=account(id=trans[0]))
            account_dest = self.account_db.get_account(account=account(id=trans[1]))
            
            trans_bean = transaction_bean(id=trans[3], step=trans[4], trans_type=trans[5], amount=trans[6], is_fraud=trans[7],
                                          id_account_orig=account_orig[0], name_account_orig=account_orig[1], old_balance_orig=account_orig[2], new_balance_orig=account_orig[3],
                                          id_account_dest=account_dest[0], name_account_dest=account_dest[1], old_balance_dest=account_dest[2], new_balance_dest=account_dest[3])
            
            list_transactions.append(trans_bean)
            
        return list_transactions
        
    
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Create one transaction~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def create_transaction(self, user, transaction='', account_orig='', account_dest='') :
        
        transaction     = transaction   if transaction != ''    else self.transaction
        
        account_orig    = account_orig  if account_orig != ''   else self.account_orig
        account_dest    = account_dest  if account_dest != ''   else self.account_dest
        
        transaction.set_trans_type(trans_type=transaction.get_trans_type().upper())
        
        this_account_id         = self.get_account_id()
        account_orig.set_id(this_account_id)
        account_dest.set_id(this_account_id + 1)
        
        
        this_transaction_id     = self.get_transaction_id()
        transaction.set_id(this_transaction_id)
        
        self.transaction_db.create_transaction(transaction=transaction, account_orig=account_orig, account_dest=account_dest, user=user)        
        self.account_db.create_account(account=account_orig, is_orig=1)
        self.account_db.create_account(account=account_dest, is_orig=0)
            
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Update one transaction~~~~~~~~~~~~~~~~~~~~~~~~~~~~##  
    
    def update_transaction(self, user, transaction='', account_orig='', account_dest='') :
        
        transaction     = transaction   if transaction != ''    else self.transaction
        
        account_orig    = account_orig  if account_orig != ''   else self.account_orig
        account_dest    = account_dest  if account_dest != ''   else self.account_dest
        
        
        self.transaction_db.update_transaction(transaction=transaction, account_orig=account_orig, account_dest=account_dest, user=user)
        self.account_db.update_account(account=account_orig, is_orig=1)
        self.account_db.update_account(account=account_dest, is_orig=0)
        
        
    ##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Delete one transaction~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
    def delete_transaction(self, id:int) :
        
        self.get_transaction(id=id)
        
        self.transaction_db.delete_transaction(transaction=self.transaction)
        
        self.account_db.delete_account(account=self.account_orig, is_orig=1)
        self.account_db.delete_account(account=self.account_dest, is_orig=0)
        