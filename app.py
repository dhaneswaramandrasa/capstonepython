from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

def scrap(url):
    #This is fuction for scrapping
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    #Find the key to get the information
    table = soup.find('table', attrs={'class':'table'})
    tr = table.find_all('tr')

    temp = [] #initiating a tuple

    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]
        #use the key to take information here
        #name_of_object = row.find_all(...)[0].text
        date = row.find_all('td')[0].text
        date = date.strip() #for removing the excess whitespace
    
        #get ask
        ask = row.find_all('td')[1].text
        ask = ask.strip() #for removing the excess whitespace
    
        #get bid
        bid = row.find_all('td')[2].text
        bid = bid.strip() #for removing the excess whitespace





        temp.append((date, ask, bid)) #append the needed information 
    
    temp = temp[::-1] #remove the header

    df = pd.DataFrame(temp, columns = ('date', 'ask', 'bid')) #creating the dataframe
    #data wranggling -  try to change the data type to right data type
    df['date'] = df['date'].str.replace('Januari','01')
    df['date'] = df['date'].str.replace('Februari','02')
    df['date'] = df['date'].str.replace('Maret','03')
    df['date'] = df['date'].str.replace('April','04')
    df['date'] = df['date'].str.replace('Mei','05')
    df['date'] = df['date'].str.replace('Juni','06')
    df['date'] = df['date'].str.replace('Juli','07')
    df['date'] = df['date'].str.replace('Agustus','08')
    df['date'] = df['date'].str.replace('September','09')
    df['date'] = df['date'].str.replace('Oktober','10')
    df['date'] = df['date'].str.replace('November','11')
    df['date'] = df['date'].str.replace('Desember','12') 
    df['date'] = df['date'].astype('datetime64')
    
    df.set_index('date',inplace = True)
    
    df['ask'] = df['ask'].str.replace(',','.')
    df['bid'] = df['bid'].str.replace(',','.')
    
    df['ask'] = df['ask'].astype('float64')
    df['bid'] = df['bid'].astype('float64')

   #end of data wranggling

    return df

@app.route("/")
def index():
    df = scrap('https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019') #insert url here

    #This part for rendering matplotlib
    fig = plt.figure(figsize=(5,2),dpi=300)
    df.plot()
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df, result=result)


if __name__ == "__main__": 
    app.run()
