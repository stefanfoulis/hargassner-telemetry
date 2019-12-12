from xml.dom import minidom
import json


def extract_daqprj_line(path):
    with open(path, "rb") as fobj:
        for line in fobj.readlines():
            line = line.decode("latin-1")
            if line.startswith("<DAQPRJ>"):
                return line


def decode(path):
    daqprj_text = extract_daqprj_line(path)
    if not daqprj_text:
        raise Exception(f"unable to extract <DAQPRJ> data from {path}")

    xml = minidom.parseString(daqprj_text)
    analog_channels_xml = xml.getElementsByTagName("ANALOG")[0].getElementsByTagName("CHANNEL")
    digital_channels_xml = xml.getElementsByTagName("DIGITAL")[0].getElementsByTagName("CHANNEL")
    channels = {}
    for xml_channel in analog_channels_xml:
        channel_id = int(xml_channel.attributes["id"].value)
        channels[channel_id] = {
            "id": channel_id,
            "name": xml_channel.attributes["name"].value,
            "unit": xml_channel.attributes["unit"].value,
            "type": "analog",
        }
    max_analog_channel_id = max(channels.keys())

    for xml_channel in digital_channels_xml:
        channel_id = int(xml_channel.attributes["id"].value)
        channel_id_with_offset = channel_id + max_analog_channel_id + 1
        channel = channels.setdefault(
            channel_id_with_offset,
            {
                "id":  channel_id,
                "type": "digital",
                "bits": {}
            },
          )
        bit = int(xml_channel.attributes["bit"].value)
        channel["bits"][bit] = {"name": xml_channel.attributes["name"].value}
    save(channels)
    return channels


def save(channels, path="channels.json"):
    with open(path, "w+") as fobj:
        fobj.write(json.dumps(channels, indent=2, sort_keys=True))

