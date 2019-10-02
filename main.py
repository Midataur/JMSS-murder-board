from flask import Flask, request, url_for, render_template

import sqlite3
import hashlib
import time
from flask_turbolinks import turbolinks

app = Flask(__name__)
open('./main.db')
turbolinks(app)

def default_sort(players):
    living,dead = [],[]
    for x in players:
        if x[2] == 1:
            living.append(x)
        else:
            dead.append(x)
    living.sort(key=lambda x: x[1])
    dead.sort(key=lambda x: x[1])
    return living[::-1]+dead[::-1]

def kills_sort(players):
    players = [list(x) for x in players]
    players.sort(key=lambda x: x[1])
    players = players[::-1]
    return players

@app.route('/')
def main():
    conn = sqlite3.connect('./main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players')
    players = curs.fetchall()
    if players == []:
        players = (('PLA0001',0,1,'Add players'),)
        conn.close()
        return render_template('index.html',players=players,kill_rank=players)
    else:
        conn.close()
        return render_template('index.html',players=default_sort(players),kill_rank=kills_sort(players))

@app.route('/newplayer')
def newplayer():
    return render_template('newplayer.html',fail=None)

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/code')
def code():
    return render_template('code.html')


@app.route('/createplayer',methods=['POST'])
def createplayer():
    conn = sqlite3.connect('./main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['code'],))
    #Check if something was wrong with the inputs
    if request.form['playername'] == '' or request.form['pass1'] == '' or request.form['code'] == '':
        conn.close()
        return render_template('newplayer.html',fail="invalid")
    elif curs.fetchone() != None:
        conn.close()
        return render_template('newplayer.html',fail="taken")
    elif request.form['pass1'] != 'obvigriefprotec': #Quality security right there
        conn.close()
        return render_template('newplayer.html',fail="wrong")
    #Create player
    curs.execute('INSERT INTO players (code,kills,alive,name) VALUES (?,0,1,?)',(request.form['code'],request.form['playername']))
    conn.commit()
    conn.close()
    return 'Player made!<br/><a href="/">Leaderboard</a>'

@app.route('/newkill')
def newkill():
    conn = sqlite3.connect('./main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players;')
    living = curs.fetchall()
    conn.close()
    return render_template('newkill.html',living=living,fail=None)

@app.route('/createkill',methods=['POST'])
def createkill():
    conn = sqlite3.connect('./main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['killer'],))
    killer = curs.fetchone()
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['victim'],))
    victim = curs.fetchone()
    curs.execute('SELECT * FROM players;')
    living = curs.fetchall()
    curs.execute('SELECT * FROM kills WHERE victim = ? AND killer = ?;',(request.form['victim'],request.form['killer']))
    kill_exists = curs.fetchone()
    if killer == None or victim == None:
        conn.close()
        return render_template('newkill.html',living=living,fail="invalid")
    elif request.form['pass1'] != 'obvigriefprotec':
        conn.close()
        return render_template('newkill.html',living=living,fail="wrong")
    elif kill_exists != None:
        conn.close()
        return render_template('newkill.html',living=living,fail="exists")
    #Create kill
    curs.execute('UPDATE players SET kills = kills+1 WHERE code = ?',(request.form['killer'],))
    curs.execute('UPDATE players SET alive = 0 WHERE code = ?',(request.form['victim'],))
    curs.execute('INSERT INTO kills (victim,killer) VALUES (?,?)',(request.form['victim'],request.form['killer']))
    conn.commit()
    conn.close()
    return 'Kill made!<br/><a href="/">Leaderboard</a>'

@app.route('/admin')
def adminpage():
    return render_template('admin.html')

@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method == 'GET':
        return render_template('reset.html',fail=None)
    else:
        if request.form['pass1'] == 'obvigriefprotec':
            conn = sqlite3.connect('./main.db')
            curs = conn.cursor()
            curs.execute('UPDATE players SET kills = 0, alive = 1')
            curs.execute('DELETE FROM kills')
            conn.commit()
            conn.close()
            return 'Leader board reset!<br/><a href="/">Leaderboard</a>'
        else:
            return render_template('reset.html',fail='wrong')

@app.route('/delete',methods=['GET','POST'])
def deleteplayer():
    conn = sqlite3.connect('./main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players;')
    living = curs.fetchall()
    if request.method == 'GET':
        conn.close()
        return render_template('delete.html',living=living,fail=None)
    else:
        if request.form['pass1'] == 'obvigriefprotec':
            curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['code'],))
            player = curs.fetchone()
            if player != None:
                curs.execute('DELETE FROM players WHERE code = ?',(request.form['code'],))
                conn.commit()
                conn.close()
                return 'Player deleted!<br/><a href="/">Leaderboard</a>'
            conn.close() 
            return render_template('delete.html',living=living,fail='invalid')
        conn.close()
        return render_template('delete.html',living=living,fail='wrong')

@app.route('/undokill',methods=['GET','POST'])
def undokill():
    conn = sqlite3.connect('./main.db')
    curs = conn.cursor()
    curs.execute('SELECT * FROM players;')
    living = curs.fetchall()
    if request.method == 'GET':
        conn.close()
        return render_template('undokill.html',living=living,fail=None)
    else:
        conn = sqlite3.connect('./main.db')
        curs = conn.cursor()
        curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['killer'],))
        killer = curs.fetchone()
        curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['victim'],))
        victim = curs.fetchone()
        curs.execute('SELECT * FROM kills WHERE victim = ? AND killer = ?;',(request.form['victim'],request.form['killer']))
        kill_exists = curs.fetchone()
        if killer == None or victim == None:
            conn.close()
            return render_template('undokill.html',living=living,fail="invalid")
        elif request.form['pass1'] != 'obvigriefprotec':
            conn.close()
            return render_template('undokill.html',living=living,fail="wrong")
        elif kill_exists == None:
            conn.close()
            return render_template('undokill.html',living=living,fail="exists")
        #Create kill
        curs.execute('UPDATE players SET kills = kills-1 WHERE code = ?',(request.form['killer'],))
        curs.execute('UPDATE players SET alive = 1 WHERE code = ?',(request.form['victim'],))
        curs.execute('DELETE FROM kills WHERE victim = ? AND killer = ?',(request.form['victim'],request.form['killer']))
        conn.commit()
        conn.close()
        return 'Kill undone!<br/><a href="/">Leaderboard</a>'











