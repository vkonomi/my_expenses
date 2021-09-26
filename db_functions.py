import sqlite3
from sys import stderr

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    #print("conn.row_factory: {}". format(type(conn.row_factory)), file=stderr)
    return conn

def get_categories():
    conn = get_db_connection()
    categories = conn.execute("""SELECT * FROM categories""").fetchall()
    conn.close()
    print("categories: {}". format(categories), file=stderr)
    return categories

def get_categories_per_type(ctg_type):
    conn = get_db_connection()
    categories = conn.execute("""SELECT * FROM categories where ctg_type = '{0}'""".format(ctg_type)).fetchall()
    conn.close()
    print("categories: {}". format(categories), file=stderr)
    return categories

def get_subcategories():
    conn = get_db_connection()
    categories = conn.execute("""SELECT * FROM subcategories""").fetchall()
    conn.close()
    return categories

def get_cur_ctg_code():
    conn = get_db_connection()
    cur_pr_id = conn.execute('SELECT COALESCE(MAX(pr_id), 1) AS max_id FROM categories').fetchall()[0]['max_id']
    conn.close()
    return cur_pr_id

def get_accounts():
    conn = get_db_connection()
    accounts = conn.execute('SELECT * FROM accounts').fetchall()
    conn.close()
    return accounts

def get_subctgs_for_ctg(ctg):
    conn = get_db_connection()
    subctgs = conn.execute("SELECT subctg_id, subctg_desc FROM subcategories WHERE (assoc_ctg = {})".format(ctg)).fetchall()
    conn.close()
    return subctgs

def get_income_subcategories_all():
    conn = get_db_connection()
    subctgs = conn.execute("""SELECT subctg_id, subctg_desc FROM subcategories
                             JOIN CATEGORIES ON ctg_id = assoc_ctg
                             WHERE ctg_type = 'I'""").fetchall()
    conn.close()
    return subctgs

def get_items_per_sctg(subctg):
    conn = get_db_connection()
    items = conn.execute("SELECT it_id, it_desc FROM items WHERE (IT_ASSOC_SCTG = {})".format(subctg)).fetchall()
    conn.close()
    return items

def get_income_items():
    conn = get_db_connection()
    income_types = conn.execute("""SELECT CTG_ID, SUBCTG_ID, IT_ID, IT_DESC
                            FROM CATEGORIES CTG
                            JOIN SUBCATEGORIES SCTG ON CTG.CTG_ID = SCTG.ASSOC_CTG
                            JOIN ITEMS IT ON SCTG.subctg_id = IT.IT_ASSOC_SCTG
                            WHERE CTG_TYPE = 'I'""").fetchall()
    conn.close()
    return income_types

def get_item_associations(item_code):
    conn = get_db_connection()
    income_types = conn.execute("""SELECT CTG_ID, SUBCTG_ID, IT_ID, IT_DESC
                            FROM CATEGORIES CTG
                            JOIN SUBCATEGORIES SCTG ON CTG.CTG_ID = SCTG.ASSOC_CTG
                            JOIN ITEMS IT ON SCTG.subctg_id = IT.IT_ASSOC_SCTG
                            WHERE CTG_TYPE = 'I'
                            AND IT_ID = {}""".format(item_code)).fetchall()[0]
    conn.close()
    return income_types

def get_pending_items(userid=' '):
    conn = get_db_connection()
    pending_items = conn.execute("""SELECT main_ctg  
                                        ,sub_ctg   
                                        ,item_code 
                                        ,item_value
                                   FROM tr_pending trp
                                   JOIN items i
                                        on trp.item_code = i.it_id
                                   WHERE (trp.userid = '{}')""".format(userid)).fetchall()
    conn.close()
    return pending_items

def sum_of_pending_items(userid=' '):
    conn = get_db_connection()
    sum_pending_items = conn.execute("""SELECT SUM(trp.item_value) as items_value FROM tr_pending trp
                                        WHERE (trp.userid = '{}')""".format(userid)).fetchall()
    conn.close()
    return sum_pending_items

def get_max_tr_id():
    conn = get_db_connection()
    cur_tr_id = conn.execute("""SELECT COALESCE(MAX(trans_id), 1) AS max_id FROM transactions""").fetchall()
    conn.close()
    return cur_tr_id

def get_last_transactions():
    conn = get_db_connection()
    cur_tr_id = conn.execute("""SELECT trans_id,
                                       trans_descr,
                                       case trans_type
                                            when 'I' then 'Income'
                                            when 'E' then 'Expense'
                                        end as trans_type
                                , round(trans_total_value,2) as trans_total_value, trans_exec_date FROM transactions
                                order by trans_exec_date desc""").fetchall()
    conn.close()
    return cur_tr_id

def insert_category(category_desc, category_type):
    conn = get_db_connection()
    conn.execute("INSERT INTO categories (ctg_desc, ctg_type) values ('{}', '{}')".format(category_desc, category_type))
    conn.commit()
    conn.close()

def insert_subcategory(assoc_pr_ctg, subcategory_desc):
    conn = get_db_connection()
    conn.execute("INSERT INTO subcategories (assoc_ctg, subctg_desc) values ('{}', '{}')".format(assoc_pr_ctg, subcategory_desc))
    conn.commit()
    conn.close()

def insert_item(IT_ASSOC_SCTG, it_desc):
    conn = get_db_connection()
    conn.execute("INSERT INTO items (IT_ASSOC_SCTG, it_desc) values ('{}', '{}')".format(IT_ASSOC_SCTG, it_desc))
    conn.commit()
    conn.close()

def insert_pending_item(userid, tr_ctg, tr_subctg, tr_item, tr_item_value):
    conn = get_db_connection()
    conn.execute("INSERT INTO tr_pending (userid, main_ctg, sub_ctg, item_code, item_value) values ('{}', '{}', '{}', '{}', '{}')".format(userid, tr_ctg, tr_subctg, tr_item, tr_item_value))
    conn.commit()
    conn.close()

def insert_transaction(new_tr_id, trans_type, trans_descr, trans_total_value, trans_account, trans_exec_date):
    conn = get_db_connection()
    conn.execute("""INSERT INTO transactions (trans_id, trans_type, trans_descr, trans_total_value, trans_account, trans_exec_date)
                    values ('{}', '{}', '{}', '{}', '{}', '{}')""".format(new_tr_id, trans_type, trans_descr, trans_total_value, trans_account, trans_exec_date))
    conn.commit()
    conn.close()

def insert_transaction_details(new_tr_id, main_ctg, sub_ctg, item_code, item_value):
    conn = get_db_connection()
    conn.execute("""INSERT INTO tr_details (tr_id, main_ctg, sub_ctg, item_code, item_value)
                    values ('{}', '{}', '{}', '{}', '{}')""".format(new_tr_id, main_ctg, sub_ctg, item_code, item_value))
    conn.commit()
    conn.close()

def del_pending(userid):
    conn = get_db_connection()
    conn.execute("""DELETE FROM tr_pending WHERE userid = '{}'""".format(userid))
    conn.commit()
    conn.close()

def get_month_to_date_expenses():
    conn = get_db_connection()
    month_to_date = conn.execute("""select round(sum(trans_total_value),2) as monthly_total from transactions
                    where strftime('%m', trans_exec_date) = strftime('%m', 'now')
                    and trans_type = 'E'
                    ;""").fetchall()
    conn.close()
    return month_to_date

def get_year_to_date_expenses():
    conn = get_db_connection()
    year_to_date = conn.execute("""select round(sum(trans_total_value),2) as yearly_total from transactions
                                where strftime('%Y', trans_exec_date) = strftime('%Y', 'now')
                                and trans_type = 'E'
                                ;""").fetchall()
    conn.close()
    return year_to_date


def get_yearly_totals():
    conn = get_db_connection()
    totals = conn.execute("""select case strftime('%m', trans_exec_date) 
                                when '01' then 'January'
                                when '02' then 'February'
                                when '03' then 'March'
                                when '04' then 'April'
                                when '05' then 'May'
                                when '06' then 'June'
                                when '07' then 'July'
                                when '08' then 'August'
                                when '09' then 'September'
                                when '10' then 'October'
                                when '11' then 'November'
                                when '12' then 'December'
                                end as month
                                ,round(te.total_expense,2) as Expenses  
                                ,round(ti.total_income,2) as Income
                            from transactions
                            join (select strftime('%m', trans_exec_date) as expense_month , sum(trans_total_value) as total_expense
                                from transactions where trans_type = 'E'
                                group by expense_month) as te
                            on strftime('%m', trans_exec_date)  = te.expense_month
                            join (select strftime('%m', trans_exec_date) as income_month , sum(trans_total_value) as total_income
                                from transactions where trans_type = 'I'
                                group by income_month) as ti
                            on strftime('%m', trans_exec_date)  = ti.income_month
                            group by strftime('%m', trans_exec_date)
                            ;""").fetchall()
    conn.close()
    return totals
