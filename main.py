import os
import requests
import json
import yaml
import time

USERNAME = os.getenv("NXAPI_USER")
PASSWORD = os.getenv("NXAPI_PASSWORD")

with open('hosts.yaml', 'r') as cfg:
    HOSTS = yaml.safe_load(cfg)


def send_msg(msg):
    """
    Sends a message to a spark room
    :param msg:
    :return:
    """
    token = os.getenv("SPARK_TOKEN")
    room = os.getenv("SPARK_ROOM")
    headers = {"Authorization": "Bearer {}".format(token)}
    url = "https://api.ciscospark.com/v1/messages"
    payload = {"roomId": room,
               "text": msg}
    resp = requests.post(url, headers=headers, data=payload)
    print resp.text


def check_cpu(host, period='load_avg_5min'):
    """
    Returns average CPU utilization - defaults to 5 minute average

    :param host: string hostname or IP address
    :param period: string key of CPU value
    :return: float CPU utilization
    """
    url = 'http://{}/ins'.format(host)

    headers = {'content-type': 'application/json-rpc'}
    payload = [
        {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "show system resources",
                "version": 1
            },
            "id": 1
        }
    ]
    response = requests.post(url, data=json.dumps(payload), headers=headers, auth=(USERNAME, PASSWORD)).json()
    ret = response['result']['body'][period]

    return float(ret)

# Initialize a place to store some informatino
values = dict()

while True:
    for h in HOSTS:
        prev = values.get(h, 0)
        curr = check_cpu(h)
        if curr > prev:
            print send_msg("CPU usage is on the rise for node {}: Previous: {} Current: {}".format(h, prev, curr))
        values[h] = curr
    time.sleep(5)
