from flask import Flask, request, url_for, render_template
import sqlite3
import hashlib
import time
app = Flask(__name__)
open('main.db')

@app.route('/')
def main():
    conn = sqlite3.connect('main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players')
    players = curs.fetchall()
    return render_template('index.html',players=players)
    conn.close()

@app.route('/newplayer')
def newplayer():
    return render_template('newplayer.html')

@app.route('/createuser',methods=['POST'])
def createplayer():
    conn = sqlite3.connect('main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM users WHERE username = ?;',(request.form['username'],))
    #Check if something was wrong with the inputs
    if request.form['username'] == '' or request.form['pass1'] == '':
        conn.close()
        return '<script>window.location = "/newuser?fail=empty"</script>'
    elif curs.fetchone() != None:
        conn.close()
        return '<script>window.location = "/newuser?fail=taken"</script>'
    elif request.form['pass1'] != request.form['pass2']:
        conn.close()
        return '<script>window.location = "/newuser?fail=diff"</script>'
    elif len(request.form['pass1']) < 7:
        conn.close()
        return '<script>window.location = "/newuser?fail=short"</script>'
    #Create user
    curs.execute('INSERT INTO users (username,password) VALUES (?,?)',(request.form['username'],hashlib.md5(request.form['pass1']).hexdigest()))
    conn.commit()
    conn.close()
    return 'User made!<br/><a href="/login">Login</a>'



