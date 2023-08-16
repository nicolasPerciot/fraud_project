import os
import sys
import pandas as pd
from flask import Flask, render_template, request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from back import main as fct


app = Flask(__name__)




##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Login, register and logout Views~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Login View~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
   
@app.route('/')
def login():  # put application's code here
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login_post():  # put application's code here
    username          = request.form['username']
    password          = request.form['password']
    
    if fct.user_bean.connect(username=username, password=password) :
        return main()
    else :
        return render_template('login.html', error='Error username or password')
    
    
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Register View~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
    
@app.route('/subscribe')
def subscribe():  # put application's code here
    return render_template('subscribe.html')


@app.route('/subscribe', methods=['POST'])
def subscribe_post():  # put application's code here
    username          = request.form['username']
    password          = request.form['password']
    
    if not fct.user_bean.is_exist(username=username) :
        fct.user_bean.set_user(username=username, password=password)        
        fct.user_bean.create_user()
        return render_template('main.html', username=username)
    else :
        return render_template('subscribe.html', error='Error username already exist !')
    
    
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Logout View~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

@app.route('/logout')
def logout():  # put application's code here    
    fct.user_bean.destruct_user()
    return render_template('login.html')




##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prediction Views~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prediction with 3 features~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

@app.route('/predicate_simple')
def predicate_simple():
    if fct.user_bean.user.get_username() == '' :
        return login()
    else :
        return render_template('predicate_simple.html')


@app.route('/predicate_simple', methods=['POST'])
def predicate_simple_post() :
    
    step                = request.form['step']
    trans_type          = request.form['type']
    amount              = request.form['amount']
    
    predict = fct.predict_simple(fct.trans_bean.set_transaction(step=step, trans_type=trans_type, amount=amount))
    
    
    return render_template('result.html', predict=fct.conf.dict_predict[predict])


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prediction with all features~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

@app.route('/predicate_global')
def predicate_global() :
    if fct.user_bean.user.get_username() == '' :
        return login()
    else :
        return render_template('predicate_global.html')


@app.route('/predicate_global', methods=['POST'])
def predicate_global_post() :
    form_transaction(request=request)
    predict = fct.predict_all(fct.trans_bean)
    fct.trans_bean.transaction.set_is_fraud(predict)
    fct.trans_bean.create_transaction(user=fct.user_bean.user)    
    return render_template('result.html', predict=fct.conf.dict_predict[predict])

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Prediction with all features step by step~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

@app.route('/step_by_step')
def step_by_step() :
    if fct.user_bean.user.get_username() == '' :
        return login()
    else :
        fct.init_node()
        feature_name = fct.node.node_next()
        return render_template('step_by_step.html', feature_name=feature_name, feature=select_step(feature_name))

@app.route('/step_by_step', methods=['POST'])
def step_by_step_post() :
    
    feature_value                   = request.form['feature_value']
    feature_name                    = request.form['feature_name']
    
    if feature_name == 'type' :
        feature_value = fct.conf.dict_type[fct.form_type_trans(feature_value)]
    
    try :
        feature_value = float(feature_value)
    except :
        feature_value = float(fct.form_name_account(feature_value))
        
    result = fct.node.node_next(value=feature_value)
    
    if isinstance(result, bool) :
        return render_template('result.html', predict=fct.conf.dict_predict[result])
    else :
        
        return render_template('step_by_step.html', feature_name=result, feature=select_step(feature_name=result)) 




##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~User Views~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~User view with the history~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
  
@app.route('/main')
def main(maj=1):
    
    if fct.user_bean.user.get_username() == '' :
        fct.destruct_transactions()
        return login()
    else :
        fct.init_transactions(fct.user_bean.user, maj=maj)        
        return render_template('main.html', username=fct.user_bean.user.get_username(), transactions=fct.transactions)


##~~~~~~~~~~~~~~~~~~~~~~~~~~~~User view update/delete~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

@app.route('/update ', methods=['POST'])
def main_post():
    global trans
    id      = request.form['id']
    trans   = fct.trans_bean.get_transaction(id=id)
    try :
        if request.form['update'] :
            return render_template('update.html', trans_bean=trans, select=select_update(trans.transaction.get_trans_type()))
    except :
        if request.form['delete'] :
            trans.delete_transaction(id=trans.transaction.get_id())
            return main()



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~User view update~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

@app.route('/main', methods=['POST'])
def update_post():
    form_transaction_update(request=request, trans=trans)    
    fct.trans_bean.update_transaction(user=fct.user_bean.user)
    return main()



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~User view statistic~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

@app.route('/stat')
def statistic():  # put application's code here
    df_tableau_comparatif = pd.read_parquet(fct.conf.parquet_path)
    lignes = df_tableau_comparatif.itertuples(index=False)
    colonnes = list(df_tableau_comparatif.columns)
    return  render_template('statistic.html', colonnes=colonnes, lignes=lignes)


    
    
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Common functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Function to build the dropdown menu for the update view~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

def select_update(trans_type) :
    trans_type = trans_type.capitalize()
    trans_type = trans_type.replace('_', ' ')
    
    string = '''<div class="form-outline mb-4">
                    <label for="type">Select type:</label>
                    <select class="form-control" id="type" name="type">
                        <option>Cash in</option>
                        <option>Cash out</option>
                        <option>Debit</option>
                        <option>Payment</option>
                        <option>Transfer</option>
                    </select>
                </div>'''
    indice = string.find(trans_type)
    tmp = [string[:indice - 1], string[indice - 1:]]
    html = tmp[0] + ' selected' + tmp[1]
    
    return html

def select_step(feature_name) :
    if feature_name == 'type' :
            
        string = '''
                    <div class="form-outline mb-4">
                        <label for="feature_value">Select type:</label>
                        <select class="form-control" id="feature_value" name="feature_value">
                            <option>Cash in</option>
                            <option>Cash out</option>
                            <option>Debit</option>
                            <option>Payment</option>
                            <option>Transfer</option>
                        </select>
                    </div>
                '''
    else :
        string = '''
                    <div class="form-outline mb-4">
                        <label class="form-label" for="feature_value">{}</label>
                        <input type="text" id="feature_value" class="form-control" name="feature_value"/>
                    </div>
                '''.format(feature_name)
    
    return string
    
                



##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Function to build the object to use~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

def form_transaction(request) :
    
    step                = request.form['step']
    trans_type          = fct.form_type_trans(request.form['type'])
    amount              = request.form['amount']
    
    account_name_orig   = request.form['account_name_orig']
    old_balance_orig    = request.form['old_balance_orig']
    new_balance_orig    = request.form['new_balance_orig']
    
    account_name_dest   = request.form['account_name_dest']
    old_balance_dest    = request.form['old_balance_dest']
    new_balance_dest    = request.form['new_balance_dest']
    
    
    fct.trans_bean.set_transaction(step=step, trans_type=trans_type, amount=amount)
    
    fct.trans_bean.set_account_orig(account_name=account_name_orig, old_balance=old_balance_orig, new_balance=new_balance_orig)
    fct.trans_bean.set_account_dest(account_name=account_name_dest, old_balance=old_balance_dest, new_balance=new_balance_dest)
    
    
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~Function to build the object to use in update~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

def form_transaction_update(request, trans) :
    
    
    trans_id            = trans.transaction.get_id()
    step                = request.form['step']
    trans_type          = fct.form_type_trans(request.form['type'])
    amount              = request.form['amount']
    
    account_id_orig     = trans.account_orig.get_id()
    account_name_orig   = request.form['account_name_orig']
    old_balance_orig    = request.form['old_balance_orig']
    new_balance_orig    = request.form['new_balance_orig']

    account_id_dest     = trans.account_dest.get_id()
    account_name_dest   = request.form['account_name_dest']
    old_balance_dest    = request.form['old_balance_dest']
    new_balance_dest    = request.form['new_balance_dest']
    
    
    fct.trans_bean.set_transaction(id=trans_id, step=step, trans_type=trans_type, amount=amount)
    
    fct.trans_bean.set_account_orig(id=account_id_orig, account_name=account_name_orig, old_balance=old_balance_orig, new_balance=new_balance_orig)
    fct.trans_bean.set_account_dest(id=account_id_dest, account_name=account_name_dest, old_balance=old_balance_dest, new_balance=new_balance_dest)
    


if __name__ == '__main__':
    app.run(debug=True)
