from cryptogram import *
from bottle import route, run, template, static_file, request
import time as t


def html_page(enc, guess, msg):
    return template('''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Cryptogram | The Game</title>
        <link rel="stylesheet" href="./files/styles/styles.css" type="text/css"/>
        <link rel="icon" href="./files/images/favicon.ico">
    </head>
    <body>
    <h1>The Cryptogram Game</h1>
    <div id="code">
        %for i in range(len(quote)):
            <div class="encoded">
                    <p class="guess">{{guessing[i]}}</p>
                    <p>{{quote[i]}}</p>
            </div>
        %end
    </div>
    %if 'Congratulations' not in msg:
    <h3 id="error">{{msg}}</h3>
    <form method="post">
        <p>
            <label for ="old">Encoded Letter:</label>
            <input type="text" id="old" name="old" maxlength="1">
        </p>
        <p>
            <label for ="old">Replace With:</label>
            <input type="text" id="new" name="new" maxlength="1">
        </p>
        <input type="submit" href="./game" name="btnChange" value="Change Letters">
    </form>
    %else:
    <div id="winner">{{msg}} <a href="game">Wanna play again?</a></div>
    %end
    </body>
    </html>''', quote=enc, guessing=guess, msg=msg)


@route('/')
@route('/instructions')
def instructions():
    return static_file('instructions.html', root='./files')


@route('/game', method="GET")
def start_game():
    global c
    try:
        c
    except NameError:
        c = Cryptogram()
    return html_page(c.encoded_quote, c.guessed_quote, '')


@route('/game', method="POST")
def play_game():
    try:
        global c
        new = request.forms.get('new').upper()
        old = request.forms.get('old').upper()
        if old.isalpha() and old in c.guesses and new.isalpha() and len(new) == 1:
            c.guess_letter(old, new)
            if c.num_guessed == len(c.quote_letters):
                if c.check_win():
                    end_time = round(t.time())
                    msg = f'''"{c.quote}"
Congratulations, you win! It took you {end_time - c.start_time} seconds.'''
                else:
                    msg = 'Hmmm...not quite! Try Again!'
            else:
                msg = ''
        else:
            msg = '''Invalid input.
Please ensure that the encoded letter exists in the encoding and that both inputs are one letter.'''
        html = html_page(c.encoded_quote, c.guessed_quote, msg)
        if c.check_win():
            del c
    except NameError:
        html = start_game()
    return html


@route('/files/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./files')


run(host='localhost', port=9001, debug=False)
