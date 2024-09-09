# SACE-SW (guigui)
Web App based on Flask Framework to control SACE HW with MQTT protocol

<br/>


## Getting started
---

#### Install virtual env
```
pip install virtualenv 
```

#### Create Python virtual environment
```
virtualenv venv
```

#### Activate virtual environment (in admin mode)
***Windows:***
```
venv\Scripts\activate
```

#### Install dependencies
```
pip install -r requirements.txt
```

#### Install Mosquitto broker
https://mosquitto.org/download/

#### Edit Mosquitto config
in mosquitto.conf, set:
listener 1883
allow_anonymous true

**for developpment only

#### Start mosquitto broker
go to mosquitto folder (C:\Program Files\mosquitto)
start mosquitto:
```
.\mosquitto -v
```

