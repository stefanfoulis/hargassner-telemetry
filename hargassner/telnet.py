import json
import telnetlib
import os
from hargassner import introspect_channel_config
from . import parse


def load_schema():
    dirname = os.path.dirname(__file__)
    schema = introspect_channel_config.decode(path=os.path.join(dirname, "../samples/SAMPLE.DAQ"))
    return schema


def connect(host):
    schema = load_schema()
    print("schema")
    print(json.dumps(schema, indent=2))
    telnet = telnetlib.Telnet(host=host, timeout=5)
    try:
        while True:
            line = telnet.read_until(b"\n")
            line_data = parse.parse(line=line.decode("ascii"), schema=schema)
            yield line_data
    except KeyboardInterrupt:
        print("closing....")
        telnet.close()
