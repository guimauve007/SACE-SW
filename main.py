from flask import Flask, redirect, url_for, request, render_template
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO

app = Flask(__name__)

# Create a Flask-SocketIO instance
socketio = SocketIO(app)

# Create a MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect("127.0.0.1", 1883, 60)

client.subscribe("/led_state")

# Define a callback function for when an MQTT message is received
def on_message(client, userdata, message):
    # Emit a Socket.IO event with the message payload
    socketio.emit('led_state', message.payload.decode('utf-8'))
    print(message.payload.decode('utf-8'))

# Set the callback function
client.on_message = on_message

@socketio.on('button_pressed')
def handle_button_pressed():
    client.publish('/led_ctl', 'TOGGLE')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/cameras')
def cameras():
    return render_template('camera.html')

@app.route('/success/<name>')
def success(name):
    return '<script>alert("Message: %s"); window.location = "/";</script>' % name

@app.route('/message', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

if __name__ == '__main__':
    # Start the MQTT client
    client.loop_start()

    # Run the Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', debug=True)

