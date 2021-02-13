import requests
import json
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox 
from Database import select, insert, creating_tables
from datetime import datetime

date=datetime.now().strftime("%Y-%m-%d")

def zapros():
    """apiKey='1e6f1af96e8d3bdb244c'
    url = "https://free.currconv.com/api/v7/convert?q={from_cur}_{to_cur}&compact=ultra&apiKey={apiKey}"
    d=dict(from_cur='USD',to_cur='UAH')
    d=dict(from_cur='USD',to_cur=to_cur)
    response = requests.request("GET", url.format(apiKey=apiKey,**d))"""

    url = "https://alpha-vantage.p.rapidapi.com/query"
    headers = {
    'x-rapidapi-key': "c196e03c3fmsh616ea3bcdef086dp14bc14jsnb23f8c69a501",
    'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
    }
    for from_cur in [x[0] for x in select('cur_id',table='Currency')]:
        querystring = {"function":"CURRENCY_EXCHANGE_RATE","to_currency":"USD","from_currency":None}
        querystring['from_currency']=from_cur
        response = requests.request("GET", url, headers=headers, params=querystring)
        rez=json.loads(response.text)
        values=rez["Realtime Currency Exchange Rate"]["1. From_Currency Code"], rez["Realtime Currency Exchange Rate"]["5. Exchange Rate"], date
        insert(*values)

def func():
    amount1=amount.get()
    value_from_cur = dict(cur_id=combo_from_cur.get(),date=date)
    value_to_cur = dict(cur_id=combo_to_cur.get(),date=date)
    # я помню о decimal потом вставлю
    rez=float(amount1)*(select('cur_to_USA', table='CurrencyRate', **value_from_cur)[0][0]/select('cur_to_USA', table='CurrencyRate', **value_to_cur)[0][0])
    lbl.configure(text=f"={rez:.2f}")

def update():
    if date not in [x[0] for x in select('date',table='CurrencyRate')]:
        zapros()
    else: 
        messagebox.showinfo('Message', 'Data have already refreshed!')  

creating_tables()

app=Tk()
app.title('Currency app')
app.geometry('500x450')

from_cur=StringVar()
to_cur=StringVar()
amount1=StringVar()


amount=Entry(app, width=15)
amount.grid(row=0, column=0,  sticky="w")


combo_from_cur = Combobox(app)
combo_to_cur = Combobox(app)  
combo_from_cur['values'] = combo_to_cur['values'] = tuple(select('cur_id', table='Currency'))
combo_from_cur.current(0)  # установите вариант по умолчанию  
combo_to_cur.current(1)
combo_from_cur.grid(column=1, row=0)  
combo_to_cur.grid(column=2, row=0) 

lbl = Label(app, text="=")
lbl.grid(column=3, row=0)


button=Button(app,text="Calculate", command=func)
button.grid(column=1, row=1)
button=Button(app,text="Refresh", command=update)
button.grid(column=2, row=1)
app.mainloop()
