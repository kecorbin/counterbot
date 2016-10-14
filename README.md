# CounterBot

CounterBot is a very simple utility which would poll a switch for CPU utilization, and report to a spark room
when that counter has incremented.

CPU utilization is given as an example, any other counter could be used as well.


## Configuration

The following environment variables need to be defined

```
export NXAPI_USER=admin
export NXAPI_PASSWORD=<changeme>
export SPARK_TOKEN=<your spark token>
export SPARK_ROOM=<roomId where msgs should be sent>

```

Additionally, the devices you would like to be monitored should be added to the hosts.yaml file


```
- switch1
- switch2
```

## Running
```
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python main.py

```
