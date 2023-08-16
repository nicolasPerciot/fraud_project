import os
import sys
import pickle
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from common import conf
from model.node import node_bean
from controller.user_bean import user_bean
from controller.transaction_bean import transaction_bean as trans_bean


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Build user_bean and transaction_bean objects~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##


user_bean       = user_bean()
trans_bean      = trans_bean()

transactions    = []
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Build node object and features dict~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

with open(conf.model_all_path, 'rb') as file :
            
    dt_classifier = pickle.load(file)
    node = node_bean(dt_classifier,0, 0)
    
    file.close() 


def init_node() :
    global node
    with open(conf.model_all_path, 'rb') as file :
            
        dt_classifier = pickle.load(file)
        node = node_bean(dt_classifier,0, 0)
        
        file.close()




##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Common function~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Form name_account~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
def form_name_account(name:str) :
    name = name.replace('C', '1')
    name = name.replace('M', '2')
    return int(name)

def form_type_trans(trans_type) :
    trans_type.lstrip(' ')
    trans_type.rstrip(' ')
    trans_type.replace(' ', '_')    
    trans_type = trans_type.upper()
    return trans_type
    

def init_transactions(user, maj=0) :
    global transactions
    if len(transactions) == 0 or maj == 1:
        transactions = trans_bean.get_transactions(user)
        
        
def destruct_transactions() :
    global transactions
    transactions = []


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prediction Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prediction with all features~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
def predict_all(transaction_bean:trans_bean, mode:str='C') :
    
    transaction_bean.transaction.set_trans_type(transaction_bean.transaction.get_trans_type().upper())
    
    if trans_bean.is_form_type(transaction_bean.transaction.get_trans_type()) :
        
        with open(conf.model_all_path, 'rb') as file :
            
            classifier = pickle.load(file)
            
            
            data = [[transaction_bean.transaction.get_step(), float(conf.dict_type[transaction_bean.transaction.get_trans_type()]), transaction_bean.transaction.get_amount(), 
                     form_name_account(transaction_bean.account_orig.get_name()), transaction_bean.account_orig.get_old_balance(), transaction_bean.account_orig.get_new_balance(),
                     form_name_account(transaction_bean.account_orig.get_name()), transaction_bean.account_orig.get_old_balance(), transaction_bean.account_orig.get_new_balance()]]
            
            df = pd.DataFrame(data=data, columns=conf.form_data_all)
            
            is_fraud = classifier.predict(df)[0]
            
            trans_bean.transaction.set_is_fraud(is_fraud=is_fraud)
            file.close()
        return is_fraud
    else :
        return 'Wrong type format !!'
    
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prediction with 3 features~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
   
def predict_simple(transaction) :
    
    trans_type = transaction.get_trans_type().upper()
    
    if trans_bean.is_form_type(trans_type) :
        
        with open(conf.model_simple_path, 'rb') as file :
            
            classifier = pickle.load(file)
            data = [[transaction.get_step(), transaction.get_amount()]]
            
            dict_type = {
                'CASH_IN'       : [1,0,0,0,0], 
                'CASH_OUT'      : [0,1,0,0,0], 
                'DEBIT'         : [0,0,1,0,0], 
                'PAYMENT'       : [0,0,0,1,0], 
                'TRANSFER'      : [0,0,0,0,1]
            }
            
            for elem in dict_type[trans_type.upper()] :
                data[0].append(elem)
            df = pd.DataFrame(data=data, columns=conf.form_data_all[:1].append(conf.form_type))
            
            is_fraud = classifier.predict(df)[0]
            
            trans_bean.transaction.set_is_fraud(is_fraud=is_fraud)
                        
            return is_fraud    