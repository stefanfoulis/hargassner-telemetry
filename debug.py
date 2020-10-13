if __name__ == "__main__":
    from hargassner import from_telnet_to_tb
    import os
    heizkessel_host = os.environ["HEIZKESSEL_HOST"]
    mqtt_host = os.environ["MQTT_HOST"]
    mqtt_api_key = os.environ["MQTT_API_KEY"]
    mqtt_user = os.environ["MQTT_USER"]
    mqtt_topic = os.environ["MQTT_TOPIC"]
    # submit_min_delay_s = int(os.environ.get("SUBMIT_DELAY_S", "60"))
    # submit_max_delay_s = int(os.environ.get("SUBMIT_DELAY_S", "60"))

    print(os.environ)

    print(f"reading from telnet at {heizkessel_host} and sending to {mqtt_host} on topic {mqtt_topic}.")


    from_telnet_to_tb.run(
        heizkessel_host=heizkessel_host,
        mqtt_host=mqtt_host,
        mqtt_api_key=mqtt_api_key,
        mqtt_user=mqtt_user,
        mqtt_topic=mqtt_topic,
    )
