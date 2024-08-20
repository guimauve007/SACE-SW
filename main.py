from flask import Flask, redirect, url_for, request, render_template
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
import cv2

app = Flask(__name__)

# Create a Flask-SocketIO instance
socketio = SocketIO(app)

# Create a MQTT client
client = mqtt.Client()

# Connect to the MQTT broker
client.connect("192.168.10.101", 1883, 60)

client.subscribe("/led_state")

# Define a callback function for when an MQTT message is received
def on_message(client, userdata, message):
    # Emit a Socket.IO event with the message payload
    socketio.emit('led_state', message.payload.decode('utf-8'))
    # print(message.payload.decode('utf-8'))

# Set the callback function
client.on_message = on_message

def gen_frames():
    cap = cv2.VideoCapture('/dev/video0')  # Change 0 to your camera index if needed

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            socketio.emit('image', frame)

@socketio.on('button_pressed')
def handle_button_pressed():
    client.publish('/led_ctl', 'TOGGLE')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/cameras')
def cameras():
    return render_template('camera.html')


if __name__ == '__main__':
    # Start the MQTT client
    client.loop_start()

    # Start the camera frame generation in a background task
    socketio.start_background_task(target=gen_frames)

    # Run the Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', debug=False, allow_unsafe_werkzeug=True)

