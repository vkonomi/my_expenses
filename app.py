from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import db_functions as db
import base_functions as d
import validation_functions as vf
from werkzeug.exceptions import abort
import pprint
import json
from collections import OrderedDict
import pandas as pd
from sys import stderr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ghbhjgfbhj5465454143215477999gfhjghjbghjsdf' 

@app.route('/', methods=('GET', 'POST')) #Flask view function, which converts the function’s return value into an HTTP response to be displayed by an HTTP client 
def index():
    if request.method == 'POST':
        if 'confirm_exp_trans' in request.form:

            tr_assoc_acc      = request.form.get('tr_assoc_acc', default=False)
            tr_date           = request.form.get('tr_date', default=False)
            tr_descr          = request.form.get('tr_descr', default=False)
            userid = 'Admin'
            d.insert_expense(userid,  tr_assoc_acc, tr_date, tr_descr)

        if 'confirm_inc_trans' in request.form:
            assoc_acc         = request.form.get('assoc_acc', default=False)
            income_item       = request.form.get('income_item', default=False) 
            income_amount     = request.form.get('income_amount', default=False)
            tr_date           = request.form.get('tr_date', default=False) 
            income_comment    = request.form.get('income_comment', default=False) 
            
            d.insert_income(assoc_acc, income_item, income_amount, tr_date, income_comment)

            flash("Income of {} Euros".format(income_amount))

    expense_categories = db.get_categories_per_type("E")
    print('expense_categories:(',len(expense_categories),') ', expense_categories, file=stderr)
    #income_items = db.get_income_items('I')
    accounts = db.get_accounts()
    income_subcategories = db.get_income_subcategories_all()
    print(type(income_subcategories), file=stderr)
    return render_template('index.html',  expense_categories=expense_categories, accounts=accounts, income_subcategories=income_subcategories) 


@app.route('/admin', methods=('GET', 'POST'))
def admin():

    if request.method == 'POST':
       #print("Hello", file=stderr)
       #print("\n".join("{}\t{}\t{}".format(i, k, v) for i in range(10) for k, v in request.form.getlist(i)), file=stderr)
       if 'create_category' in request.form:
        category_desc = request.form.get('addcategory2', default=False) #request.form.getlist
        category_type = request.form.get('addcategory3', default=False)
        if vf.validate_string(category_desc):
            print("To insert: {},{}".format(category_desc, category_type), file=stderr)
            db.insert_category(category_desc, category_type)
            flash("Category {} has been inserted".format(category_desc))

       elif 'create_subcategory' in request.form:
        subcategory_desc = request.form.get('addsubcategory2', default=False) #request.form.getlist
        assoc_pr_ctg = request.form.get('assoc_pr_ctg', default=False)

        #print("To insert: {},{},{}".format(subcategory, subcategory_desc, assoc_pr_ctg), file=stderr)

        if vf.validate_string(subcategory_desc, assoc_pr_ctg):
            print("To insert: {},{}".format(subcategory_desc, assoc_pr_ctg), file=stderr)
            db.insert_subcategory(assoc_pr_ctg, subcategory_desc)
            flash("Subcategory {} has been inserted".format(subcategory_desc))

       elif 'create_item' in request.form:
        item_desc = request.form.get('additem1', default=False) #request.form.getlist
        sctg_id = request.form.get('i_sub_subctg', default=False)

        #print("To insert: {},{},{}".format(subcategory, subcategory_desc, assoc_pr_ctg), file=stderr)
        print("To insert: {},{}".format(item_desc, sctg_id), file=stderr)
        if vf.validate_string(item_desc):
            print("To insert: {},{}".format(item_desc, sctg_id), file=stderr)
            db.insert_item(sctg_id, item_desc)
            flash("Item {} has been inserted".format(item_desc))

    categories = db.get_categories()
    #subcategories = db.get_subctgs_for_ctg(8)

    #print("\n".join("{}\t{}".format(k, v) for k, v in request.form.getlist(0)), file=stderr)
    #print("11 tuple: {}". format(type(request.form.getlist()), file=stderr))
    #print("cat_id: {}". format(categories[0]['pr_desc']), file=stderr)

    return render_template('admin.html', categories=categories)

@app.route('/reporting', methods=('GET', 'POST'))
def reporting():

    monthly_expenses = db.get_month_to_date_expenses()[0]['monthly_total']
    yearly_expenses =  db.get_year_to_date_expenses()[0]['yearly_total']
    all_monthly_totals = db.get_yearly_totals()

    return render_template('reporting.html', monthly_expenses=monthly_expenses,
                                            yearly_expenses=yearly_expenses,
                                            all_monthly_totals=all_monthly_totals) 

@app.route('/about', methods=('GET', 'POST'))
def about():
    return redirect(url_for('index'))


@app.route('/_get_subcategories', methods=['GET'])
def get_subcategories():
    if request.method == "GET":

        #print("Parse DATA", file=stderr)
        id = request.args.get('b', 1)
        print("Parse ID:", id, file=stderr)
        db_list = db.get_subctgs_for_ctg(id)
        t_list = {str(db_list[i]['subctg_id']): db_list[i]['subctg_desc'] for i in range(len(db_list))}
        print('T_list:',t_list, file=stderr)
        # When returning data it has to be jsonify'ed and a list of tuples (id, value) to populate select fields.
        # Example: [('1', 'One'), ('2', 'Two'), ('3', 'Three')]
        response = jsonify(t_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/_get_items', methods=['GET'])
def get_items():
    if request.method == "GET":

        #print("Parse DATA", file=stderr)
        id = request.args.get('b', 1)
        print("Parse ID:", id, file=stderr)
        db_list = db.get_items_per_sctg(id)
        t_list = {str(db_list[i]['it_id']): db_list[i]['it_desc'] for i in range(len(db_list))}
        #print('T_list:',t_list, file=stderr)

        response = jsonify(t_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/_handle_pending_expense', methods=['GET'])
def handle_pending_expense():
    if request.method == "GET":
        tr_ctg     = request.args.get('a', default=False)
        tr_subctg  = request.args.get('b', default=False)
        tr_item    = request.args.get('d', default=False)
        tr_item_value = request.args.get('e', default=False)

        userid = 'Admin'

        print("To insert: {}, {}, {}, {} ,{}".format(userid, tr_ctg, tr_subctg, tr_item, tr_item_value), file=stderr)
        db.insert_pending_item(userid, tr_ctg, tr_subctg, tr_item, tr_item_value)

        #db_pen_item_list = db.get_pending_items(userid)
        #t_list = {db_pen_item_list[i]['item_key']: (db_pen_item_list[i]['item_name'], str(db_pen_item_list[i]['item_value'])) for i in range(len(db_pen_item_list))}
        #print('Pending_list:(',len(t_list),') ', t_list, file=stderr)
      
        total_amount = db.sum_of_pending_items(userid)[0]['items_value']
        t_amount = {'total': total_amount}

        #print('len(db_pen_item_list):',len(db_pen_item_list), file=stderr)
 
        response = jsonify(t_amount)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/_show_last_transactions', methods=['GET'])
def show_last_transactions():
    if request.method == "GET":
        tr_type   = request.args.get('a', default=False)
        tr_range  = request.args.get('b', default=False)
      
        last_trans = db.get_last_transactions()
        #last_trans_df = pd.read_sql(db.get_last_transactions()).to_json(orient='records')

        print('last_trans:',{'data': [OrderedDict(trans) for trans in last_trans]},  file=stderr)

        return {'data': [OrderedDict(trans) for trans in last_trans]}

"""
        response = jsonify(last_trans)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
"""