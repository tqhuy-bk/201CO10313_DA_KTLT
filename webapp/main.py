# Store this code in 'app.py' file 
from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import re 


app = Flask(__name__, template_folder='template')

app.secret_key = '123456789'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'data'


mysql = MySQL(app) 

#homepage
@app.route('/')
def root():
    return render_template("index.html")

@app.route("/DataTiKi")
def DataTiKi():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM TiKi')
    account = cursor.fetchall()
    return render_template("data_tiki.html", account=account)

@app.route("/DataLazada")
def DataLazada():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Lazada')
    account = cursor.fetchall()
    return render_template("data_lazada.html", account=account)

@app.route("/DataShopee")
def DataShopee():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Shopee')
    account = cursor.fetchall()
    return render_template("data_shopee.html", account=account)

@app.route("/DataDienMay")
def DataDienMay():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM DienMayChoLon')
    account = cursor.fetchall()
    return render_template("data_dienmaycholon.html", account=account)

@app.route("/DataNguyenKim")
def DataNguyenKim():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM NguyenKim')
    account = cursor.fetchall()
    return render_template("data_nguyenkim.html", account=account)

@app.route("/Chart")
def Chart():
    return render_template("charts.html")

@app.route('/SimpleSearch', methods=['GET', 'POST'])
def SimpleSearch():
    if request.method == 'POST' and 'simplesearch' in request.form :
        simplesearch = request.form['simplesearch']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Tiki WHERE Category= %s ORDER BY Tiki.Price',(simplesearch,))
        account1 = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Lazada WHERE Category= %s ORDER BY Lazada.Price',(simplesearch,))
        account2 = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Shopee WHERE Category= %s ORDER BY Shopee.Price',(simplesearch,))
        account3 = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM NguyenKim WHERE Category= %s ORDER BY NguyenKim.Price',(simplesearch,))
        account4 = cursor.fetchall()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM DienMayChoLon WHERE Category= %s ORDER BY DienMayChoLon.Price',(simplesearch,))
        account5 = cursor.fetchall()
        return render_template("simple-results.html",account1=account1,account2=account2,account3=account3,account4=account4,account5=account5)

    return render_template("simple-search.html")
if __name__ == "__main__": 
    app.run(host ="localhost", port = int("5000")) 
