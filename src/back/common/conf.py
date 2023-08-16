import os



##------------------------------------Connection DB------------------------------------##

##-----------------MySQL-----------------##

host                        = "localhost"
user                        = "admin"
password                    = "root"
database                    = "fraud_project"

connect_db_mysql            = "mysql://{}:{}@{}/{}".format(user, password, host, database)

##-----------------SQLite-----------------##

connect_db_sqlite           = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fraud_database.db')

##------------------------------------Name of the Tables------------------------------------##

user_table_name             = "users"
account_table_name          = "accounts"
account_orig_table_name     = "origin"
account_dest_table_name     = "dest"
transaction_table_name      = "transactions"


##------------------------------------Config Model------------------------------------##

##-----------------Path to the model-----------------##

model_path                  = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 'data')

model_all_path              = os.path.join(model_path, 'dt_smote.pkl')

model_simple_path           = os.path.join(model_path, 'dt_simple.pkl')

##-----------------Form of the data to do the prediction-----------------##

form_type                   = ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']

dict_type = {
                'CASH_IN'       : 0, 
                'CASH_OUT'      : 1, 
                'DEBIT'         : 2, 
                'PAYMENT'       : 3, 
                'TRANSFER'      : 4
            }

form_data_all               = ['step', 'type', 'amount', 'nameOrig', 'oldbalanceOrg', 'newbalanceOrig', 'nameDest', 'oldbalanceDest', 'newbalanceDest']


dict_predict = {
            0 : "Not Fraud !",
            1 : "FRAUD !!"
        }


parquet_path            = os.path.join(model_path, 'tableau_comparatifs.parquet')