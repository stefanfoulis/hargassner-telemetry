if __name__ == "__main__":
    from hargassner import from_telnet_to_tb
    import os
    heizkessel_host = os.environ["HEIZKESSEL_HOST"]
    mqtt_host = os.environ["MQTT_HOST"]
    mqtt_api_key = os.environ["MQTT_API_KEY"]
    submit_delay_s = int(os.environ.get("SUBMIT_DELAY_S", "60"))

    print(os.environ)

    print(f"reading from telnet at {heizkessel_host} and sending to {mqtt_host} with a delay of {submit_delay_s}s")

    from_telnet_to_tb.run(
        heizkessel_host=heizkessel_host,
        mqtt_host=mqtt_host,
        mqtt_api_key=mqtt_api_key,
        submit_delay_s=submit_delay_s
    )
