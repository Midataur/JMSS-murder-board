from flask import Flask, request, url_for, render_template

import sqlite3
import hashlib
import time
from flask_turbolinks import turbolinks

app = Flask(__name__)
open('./main.db')
turbolinks(app)

ADMIN_PASS = 'PLEASE_SET_THIS_WHEN_YOU_HOST'

#this is a decorator that handles all of the construction and teardown of sql connections
#it saves like 50 lines of code
#idk why i didn't think of this before
def sql_handler(function):
    def wrapper(*args,**kwargs):
        conn = sqlite3.connect('./main.db')
        cursor = conn.cursor()
        output = function(*args,curs=cursor,**kwargs)
        conn.commit()
        conn.close()
        return output
    wrapper.__name__ = function.__name__
    return wrapper
        

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
@sql_handler
def main(curs):
    curs.execute('SELECT * FROM players')
    players = curs.fetchall()
    if players == []:
        players = (('PLA0001',0,1,'Add players'),)
        return render_template('index.html',players=players,kill_rank=players)
    else:
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
@sql_handler
def createplayer(curs):
    global ADMIN_PASS
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['code'],))
    #Check if something was wrong with the inputs
    if request.form['playername'] == '' or request.form['pass1'] == '' or request.form['code'] == '':
        return render_template('newplayer.html',fail="invalid")
    elif curs.fetchone() != None:
        return render_template('newplayer.html',fail="taken")
    elif request.form['pass1'] != ADMIN_PASS: #Quality security right there
        return render_template('newplayer.html',fail="wrong")
    #Create player
    curs.execute('INSERT INTO players (code,kills,alive,name) VALUES (?,0,1,?)',(request.form['code'],request.form['playername']))
    return 'Player made!<br/><a href="/">Leaderboard</a>'

@app.route('/newkill')
@sql_handler
def newkill(curs):
    curs.execute('SELECT * FROM players;')
    living = curs.fetchall()
    return render_template('newkill.html',living=living,fail=None)

@app.route('/createkill',methods=['POST'])
@sql_handler
def createkill(curs):
    global ADMIN_PASS
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['killer'],))
    killer = curs.fetchone()
    curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['victim'],))
    victim = curs.fetchone()
    curs.execute('SELECT * FROM players;')
    living = curs.fetchall()
    curs.execute('SELECT * FROM kills WHERE victim = ? AND killer = ?;',(request.form['victim'],request.form['killer']))
    kill_exists = curs.fetchone()
    if killer == None or victim == None:
        return render_template('newkill.html',living=living,fail="invalid")
    elif request.form['pass1'] != ADMIN_PASS:
        return render_template('newkill.html',living=living,fail="wrong")
    elif kill_exists != None:
        return render_template('newkill.html',living=living,fail="exists")
    #Create kill
    curs.execute('UPDATE players SET kills = kills+1 WHERE code = ?',(request.form['killer'],))
    curs.execute('UPDATE players SET alive = 0 WHERE code = ?',(request.form['victim'],))
    curs.execute('INSERT INTO kills (victim,killer) VALUES (?,?)',(request.form['victim'],request.form['killer']))
    return 'Kill made!<br/><a href="/">Leaderboard</a>'

@app.route('/admin')
def adminpage():
    return render_template('admin.html')

@app.route('/reset',methods=['GET','POST'])
@sql_handler
def reset(curs):
    global ADMIN_PASS
    if request.method == 'GET':
        return render_template('reset.html',fail=None)
    else:
        if request.form['pass1'] == ADMIN_PASS:
            curs.execute('UPDATE players SET kills = 0, alive = 1')
            curs.execute('DELETE FROM kills')
            return 'Leader board reset!<br/><a href="/">Leaderboard</a>'
        else:
            return render_template('reset.html',fail='wrong')

@app.route('/delete',methods=['GET','POST'])
@sql_handler
def deleteplayer(curs):
    global ADMIN_PASS
    curs.execute('SELECT * FROM players;')
    living = curs.fetchall()
    if request.method == 'GET':
        return render_template('delete.html',living=living,fail=None)
    else:
        if request.form['pass1'] == ADMIN_PASS:
            curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['code'],))
            player = curs.fetchone()
            if player != None:
                curs.execute('DELETE FROM players WHERE code = ?',(request.form['code'],))
                return 'Player deleted!<br/><a href="/">Leaderboard</a>'
            return render_template('delete.html',living=living,fail='invalid')
        return render_template('delete.html',living=living,fail='wrong')

@app.route('/undokill',methods=['GET','POST'])
@sql_handler
def undokill(curs):
    global ADMIN_PASS
    curs.execute('SELECT * FROM players;')
    living = curs.fetchall()
    if request.method == 'GET':
        return render_template('undokill.html',living=living,fail=None)
    else:
        curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['killer'],))
        killer = curs.fetchone()
        curs.execute('SELECT * FROM players WHERE code = ?;',(request.form['victim'],))
        victim = curs.fetchone()
        curs.execute('SELECT * FROM kills WHERE victim = ? AND killer = ?;',(request.form['victim'],request.form['killer']))
        kill_exists = curs.fetchone()
        if killer == None or victim == None:
            return render_template('undokill.html',living=living,fail="invalid")
        elif request.form['pass1'] != ADMIN_PASS:
            return render_template('undokill.html',living=living,fail="wrong")
        elif kill_exists == None:
            return render_template('undokill.html',living=living,fail="exists")
        #Create kill
        curs.execute('UPDATE players SET kills = kills-1 WHERE code = ?',(request.form['killer'],))
        curs.execute('UPDATE players SET alive = 1 WHERE code = ?',(request.form['victim'],))
        curs.execute('DELETE FROM kills WHERE victim = ? AND killer = ?',(request.form['victim'],request.form['killer']))
        return 'Kill undone!<br/><a href="/">Leaderboard</a>'


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.run()
