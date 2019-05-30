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

@app.route('/createplayer',methods=['POST'])
def createplayer():
    conn = sqlite3.connect('main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['code'],))
    #Check if something was wrong with the inputs
    if request.form['playername'] == '' or request.form['pass1'] == '' or request.form['code'] == '':
        conn.close()
        return '<script>window.location = "/newplayer?fail=invalid"</script>'
    elif curs.fetchone() != None:
        conn.close()
        return '<script>window.location = "/newplayer?fail=taken"</script>'
    elif request.form['pass1'] != 'obvigriefprotec': #Quality security right there
        conn.close()
        return '<script>window.location = "/newplayer?fail=wrong"</script>'
    #Create player
    curs.execute('INSERT INTO players (code,kills,alive,name) VALUES (?,0,1,?)',(request.form['code'],request.form['playername']))
    conn.commit()
    conn.close()
    return 'Player made!<br/><a href="/">Leaderboard</a>'

@app.route('/newkill')
def newkill():
    return render_template('newkill.html')

@app.route('/createkill',methods=['POST'])
def createkill():
    conn = sqlite3.connect('main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['killer'],))
    killer = curs.fetchone()
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['victim'],))
    victim = curs.fetchone()
    if killer == None or victim == None:
        conn.close()
        return '<script>window.location = "/newkill?fail=invalid"</script>'
    elif request.form['pass1'] != 'obvigriefprotec': #Quality security right there
        conn.close()
        return '<script>window.location = "/newkill?fail=wrong"</script>'
    elif killer[2] == 0 or victim[2] == 0:
        conn.close()
        return '<script>window.location = "/newkill?fail=dead"</script>'
    #Create kill
    curs.execute('UPDATE players SET kills = kills+1 WHERE code = ?',(request.form['killer'],))
    curs.execute('UPDATE players SET alive = 0 WHERE code = ?',(request.form['victim'],))
    conn.commit()
    conn.close()
    return 'Kill made!<br/><a href="/">Leaderboard</a>'

@app.route('/admin')
def adminpage():
    return render_template('admin.html')


