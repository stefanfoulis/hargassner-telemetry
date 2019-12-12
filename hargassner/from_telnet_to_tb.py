from copy import deepcopy
import datetime

from . import telnet, submit
import json


def run(heizkessel_host, mqtt_host, mqtt_api_key, submit_delay_s=60):
    print(f"initiating telnet stream...")
    stream = telnet.connect(host=heizkessel_host)
    prev_data = {}
    last_submit = None
    print(f"consuming telnet stream...")
    for data in stream:
        print("read")
        changed = what_has_changed(prev_data, data)
        if changed:
            print(json.dumps(changed, indent=2, sort_keys=True))
        now = datetime.datetime.now()
        if last_submit is None or last_submit + datetime.timedelta(seconds=submit_delay_s) < now:
            submit.report_data(data, mqtt_host=mqtt_host, mqtt_api_key=mqtt_api_key)
            last_submit = now
            print("submit")
        else:
            print(f"skip (last submit: {last_submit}")
        # print(json.dumps(data, indent=2, sort_keys=True))
        prev_data = deepcopy(data)


def what_has_changed(new_data, prev_data):
    changed = {}
    for key, value in new_data.items():
        if value["value"] != prev_data[key]["value"]:
            changed[key] = {
                "old": prev_data[key]['value'],
                "new": value['value'],
                "ts": str(datetime.datetime.utcnow()),
            }
    return changed
