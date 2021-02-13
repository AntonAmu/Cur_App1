import sqlite3 as db
import json
import datetime

def unpack(file_name):
        if file_name == 'ListCurrency1.txt':
            with open(file_name,encoding='utf-8-sig') as file:
                rez=json.load(file)
                return ([rez['results'][x]['id'], rez['results'][x]['currencyName']] for x in rez['results'])
             

def conn():
    con=db.connect('data.db')
    cur=con.cursor()
    return con, cur


def creating_tables():
    con, cur =conn()
    cur.execute("Create Table if not exists Currency (cur_id primery key text, cur_name text)")
    cur.execute("Create Table if not exists CurrencyRate (cur_id text, cur_to_USA integer, date text)")
    cur.executemany("Insert into Currency(cur_id , cur_name) values (?, ?)", unpack('ListCurrency1.txt'))
    con.commit()
    con.close()



def delet_tables():
    con, cur =conn()
    cur.execute("Select name from sqlite_master where type='table' AND name NOT LIKE 'sqlite_%'")
    list_of_tables=cur.fetchall()
    for table in list_of_tables:
        cur.execute("Drop table {name}".format(name=table[0]))
    con.commit()
    con.close()


def select(*arg, table, **kwarg):
    if not kwarg:
        string="Select {x} from {table}".format(x=', '.join(arg), table=table)
    else:
        string="Select {x} from {table} where {condition}".format(x=', '.join(arg), table=table, condition=' and '.join([f"{key}= '{kwarg[key]}'" for key in kwarg]))
    con, cur =conn()
    cur.execute(string)
    rez=cur.fetchall()
    con.commit()
    con.close()
    return rez



def insert(*arg):
    cur_id, cur_to_USA, date= arg
    date=datetime.date.today()
    string=f"Insert into CurrencyRate(cur_id, cur_to_USA, date)\
    values ('{cur_id}', {cur_to_USA}, '{date}')"
    con, cur =conn()
    cur.execute(string)
    con.commit()
    con.close()

        
