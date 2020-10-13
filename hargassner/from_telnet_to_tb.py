from copy import deepcopy
import datetime

from . import telnet, submit
import json


def run(heizkessel_host, mqtt_host, mqtt_api_key, mqtt_user, mqtt_topic):
    print(f"initiating telnet stream...")
    report_every = datetime.timedelta(seconds=5)
    report_changes_immediatly = True

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
        do_report_because_data_changed = report_changes_immediatly and changed
        do_report_because_time = last_submit is None or last_submit + report_every < now
        if not (do_report_because_data_changed or do_report_because_time):
            print(f"skip (last submit: {last_submit}")
            continue

        print("submit")
        submit.report_data(measured_at=now, data=data, mqtt_host=mqtt_host, mqtt_api_key=mqtt_api_key, mqtt_user=mqtt_user, mqtt_topic=mqtt_topic)
        last_submit = now
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
