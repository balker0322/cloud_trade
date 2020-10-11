from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

from threading import Thread, Event
import time

from binance.client import Client
from binance.websockets import BinanceSocketManager
from app.config import BINANCE_CREDENTIALS


client = Client(BINANCE_CREDENTIALS['KEY'], BINANCE_CREDENTIALS['SECRET'])

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
# thread = None
# thread_lock = Lock()
thread = Thread()
thread_stop_event = Event()
conn_key = ""
count = 0

def emit_data(msg):
	global count
	if msg['e'] != 'error':
		btc_price = float(msg['c'])
		socket_.emit('my_response',
			{'data': str(count), 'count': btc_price}, namespace='/test')
		socket_.sleep(1)
		count += 1
		# if count == 60*60*12:
		# 	count = 0


@app.route('/')
def index():
	return render_template('index.html', async_mode=socket_.async_mode)


@socket_.on('connect', namespace='/test')
def test_connect():
	bsm = BinanceSocketManager(client)
	conn_key = bsm.start_symbol_ticker_socket("BTCUSDT", emit_data)
	bsm.start()
	# need visibility of the global thread object
	# global thread
	# print('Client connected')

	# #Start the random number generator thread only if the thread has not been started before.
	# if not thread.isAlive():
	#     print("Starting Thread")
	#     thread = socket_.start_background_task(emit_data)


@socket_.on('my_event', namespace='/test')
def test_message(message):
	# thread = socket_.start_background_task(emit_data)
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		 {'data': message['data'], 'count': session['receive_count']})


@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		 {'data': message['data'], 'count': session['receive_count']},
		 broadcast=True)


@socket_.on('disconnect_request', namespace='/test')
def disconnect_request():
	@copy_current_request_context
	def can_disconnect():
		disconnect()

	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my_response',
		 {'data': 'Disconnected!', 'count': session['receive_count']},
		 callback=can_disconnect)


