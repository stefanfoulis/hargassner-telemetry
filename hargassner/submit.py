import calendar
import datetime
import json
import paho.mqtt.client as mqtt


tb_client = None


def report_data(data, mqtt_host, mqtt_api_key):
    global tb_client
    if not tb_client:
        tb_client = mqtt.Client()
        tb_client.username_pw_set(mqtt_api_key)
        tb_client.connect(mqtt_host, 1883, 60)
        tb_client.loop_start()
    payload = restructure_for_thingsboard(data)
    tb_client.publish(
        "v1/devices/me/telemetry", json.dumps(payload), 1
    )


def restructure_for_thingsboard(data, measured_at=None):
    measured_at = datetime.datetime.utcnow() if measured_at is None else measured_at
    unixtime = calendar.timegm(measured_at.utctimetuple()) * 1000

    # thingsboard does not know anything about units
    values = {f"{key} ({value['unit']})" if value["unit"] else f"{key}": value["value"] for key, value in data.items()}
    return {"ts": unixtime, "values": values}


def write_to_log(line):
    today = datetime.date.today()
    with open("data-{today}.log".format(today=today), "a+") as fobj:
        fobj.write("{} {}".format(datetime.datetime.utcnow(), line.decode('ascii')))
