import db_functions as db
from sys import stderr

def insert_income(assoc_acc, item, income_amount, tr_date, income_comment):
    new_tr_id = db.get_max_tr_id()[0]['max_id'] # [0] is the first row, max_id is the column name
    new_tr_id +=1 
    income = db.get_item_associations(item)
    #for id in new_tr_id:
     #   print("ID: {}".format(id), file=stderr)

    print("To insert: {}, {}, {}, {}, {}".format(assoc_acc, item, income_amount, tr_date, income_comment), file=stderr)
    db.insert_transaction(new_tr_id, 'I', income_comment , income_amount, assoc_acc, tr_date)
    db.insert_transaction_details(new_tr_id, income['CTG_ID'], income['SUBCTG_ID'], income['IT_ID'], income_amount)

def insert_expense(userid, tr_assoc_acc, tr_date, tr_descr):
    new_tr_id = db.get_max_tr_id()[0]['max_id'] # [0] is the first row, max_id is the column name
    new_tr_id +=1 

    #for id in new_tr_id:
     #   print("ID: {}".format(id), file=stderr)

    print("To insert: {},{},{}".format(tr_assoc_acc, tr_date, tr_descr), file=stderr)
    db.insert_transaction(new_tr_id, 'E', tr_descr, db.sum_of_pending_items(userid)[0]['items_value'], tr_assoc_acc, tr_date)

    db_pen_item_list = db.get_pending_items(userid)
    for i in range(len(db_pen_item_list)):
        db.insert_transaction_details(new_tr_id, db_pen_item_list[i]['main_ctg'],
                 db_pen_item_list[i]['sub_ctg'],
                 db_pen_item_list[i]['item_code'], db_pen_item_list[i]['item_value'])

    db.del_pending(userid)
    #t_list = {db_pen_item_list[i]['item_key']: (db_pen_item_list[i]['item_name'], str(db_pen_item_list[i]['item_value'])) for i in range(len(db_pen_item_list))}
       

"""
insert_transaction(new_tr_id, trans_type, trans_descr, trans_total_value, trans_account, trans_exec_date)
insert_transaction_details(new_tr_id, main_ctg, sub_ctg, section, item_code, item_value)

item_key INTEGER NOT NULL,
    userid   char(10) NOT NULL,
    main_ctg char(02) not null,
    sub_ctg  char (02) not null,
    section  char(03) not null, 
    item_code integer not null,
    item_value float(7,2) DEFAULT 0 NOT NULL,
    tr_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
"""

