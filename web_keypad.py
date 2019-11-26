#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.

async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary when using a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()
import RPI.GPIO as GPiO
import time, sys, tty, os, serial
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

GPIO.setmode(GPIO.BOARD)

#pin numbers on the pi
input_PA=11
input_RESET=13
input_INT=15
input_SET=16
input_ABORT=
input_FIRE=

GPIO.setup(input_PA, GPIO.IN)
GPIO.setup(input_RESET, GPIO.IN)
GPIO.setup(input_INT, GPIO.IN)
GPIO.setup(input_SET, GPIO.IN)
GPIO.setup(input_ABORT, GPIO.IN)
GPIO.setup(input_FIRE, GPIO.IN)
sleep(1)


ser = serial.Serial('/dev/ttyAMA0', 9600) 
time.sleep(2)

keycode_values = {
    'b0': 0x30,
    'b1': 0x31,
    'b2': 0x32,
    'b3': 0x33,
    'b4': 0x34,
    'b5': 0x35,
    'b6': 0x36,
    'b7': 0x37,
    'b8': 0x38,
    'b9': 0x39,
    'chime': 0x3a,
    'omit': 0x3b,
    'cancel': 0x3c,
    'program': 0x3d,
    'confirm': 0x3e,
    'reset': 0x3f,
    'panic': 0xaa,
}


def readAccentaOutputs():
    state_PA = GPIO.input(input_PA)
    state_RESET = GPIO.input(input_RESET)
    state_INT = GPIO.input(input_INT)
    state_SET = GPIO.input(input_SET)
    state_ABORT = GPIO.input(input_ABORT)
    state_FIRE = GPIO.input(input_FIRE)

def sendSerial(keycode):

        
def background_thread():
    count = 0
    while True:
        time.sleep(0.05)
        readAccentaOutputs()
        count += 1





@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('keypad.html', **values)


@socketio.on('my event', namespace='/raspberrykeypad')
def message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('button pressed', namespace='/raspberrykeypad')
def button_pressed(buttonid):
	sendSerial(keycode_values[buttonid])
    emit('button pressed', buttonid, broadcast=True)

@socketio.on('connect', namespace='/raspberrykeypad')
def test_connect():
    emit('my response', {'data': 'Connecting', 'count': 0})


@socketio.on('disconnect', namespace='/raspberrykeypad')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
