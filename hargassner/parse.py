# from bitstring import BitString


def parse(line, schema):
    cells = line.split(" ")
    # date = cells.pop(0)
    # time = cells.pop(0)
    marker = cells.pop(0)
    assert marker == "pm"
    data = {}

    for pos, channel_schema in schema.items():
        value = cells[pos]
        data.update(handle_value(value, channel_schema))
    return data


def handle_value(value, channel_schema):
    if channel_schema["type"] == "analog":
        data = handle_analog_value(value, channel_schema)
    elif channel_schema["type"] == "digital":
        data = handle_digital_value(value, channel_schema)
    else:
        raise ValueError
    return data


def handle_analog_value(value, channel_schema):
    return {
        channel_schema["name"]: {
            "value": float(value),
            "unit": channel_schema["unit"],
        }
    }


def handle_digital_value(value, channel_schema):
    # print(f"handling digital {value}")
    # bits = BitString(bin=value)
    return {}
