import calendar
import datetime
import json
import paho.mqtt.client as mqtt


mqtt_client = None


def report_data(measured_at, data, mqtt_host, mqtt_api_key, mqtt_user, mqtt_topic):
    global mqtt_client
    if not mqtt_client:
        mqtt_client = mqtt.Client()
        mqtt_client.username_pw_set(username=mqtt_user, password=mqtt_api_key)
        mqtt_client.connect(mqtt_host, 1883, 60)
        mqtt_client.loop_start()
    payload = restructure_for_mqtt(data, measured_at=measured_at)
    mqtt_client.publish(
        mqtt_topic, json.dumps(payload), 1
    )

def restructure_for_mqtt(data, measured_at=None):
    measured_at = datetime.datetime.utcnow() if measured_at is None else measured_at
    unixtime = calendar.timegm(measured_at.utctimetuple())
    return {"ts": unixtime, "data": data}


def write_to_log(line):
    today = datetime.date.today()
    with open("data-{today}.log".format(today=today), "a+") as fobj:
        fobj.write("{} {}".format(datetime.datetime.utcnow(), line.decode('ascii')))
