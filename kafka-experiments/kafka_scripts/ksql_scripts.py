import requests

from . import settings
from .http_response_check import check_errors

headers = {
    'Accept': 'application/vnd.ksql.v1+json',
    'Content-Type': 'application/vnd.ksql.v1+json'
}


def _execute_ksql_commands(command):
    url = f'{settings.KSQL_URL}/ksql'
    data = {'ksql': command}
    response = requests.post(url, headers=headers, json=data)
    check_errors(response)
    return response


def _check_stream_create_status(stream=None):
    assert stream
    url = f'{settings.KSQL_URL}/status/stream/{stream}/create'
    response = requests.get(url)
    assert response.json()['status'] == 'SUCCESS'


def _create_noise_stream():
    """
    Create the base stream from the noise topic.This
    is the base of all other topics/streams/table
    """
    command = (
        f"CREATE STREAM {settings.NOISE_STREAM}"
        f" WITH (kafka_topic='{settings.KAFKA_TOPIC}',"
        f" value_format='{settings.VALUE_FORMAT}');"
    )
    response = _execute_ksql_commands(command)
    print(f'KAFKA/KSQL:: {settings.NOISE_STREAM} STREAM CREATED')


def _create_location_based_steam():
    """
    Create the stream with location for elasticsearch
    """
    command = (
        f"CREATE STREAM ELASTIC_LOCATION_STREAM"
        f" AS SELECT SENSOR->SENSOR_NAME AS SENSOR_NAME,"
        f" THING->LOCATION AS LOCATION"
        f" FROM {settings.NOISE_STREAM}"
        f" PARTITION BY SENSOR_NAME;"
    )
    response = _execute_ksql_commands(command)

    print(f"KAFKA/KSQL:: STREAM LOCATION BASED CREATED")


def _create_sensor_name_keyed_stream():
    """
    Create the stream with key (sensor_name). The key part is required
    if we want to save the message to database.
    """
    command = (
        f"CREATE STREAM {settings.NOISE_STREAM_KEYED}"
        f" AS SELECT * FROM {settings.NOISE_STREAM}"
        f" PARTITION BY sensor_name;"
    )
    command1 = (
        f"CREATE STREAM {settings.NOISE_STREAM_KEYED}"
        f" AS SELECT SENSOR->SENSOR_NAME AS SENSOR_NAME,"
        f" RESULTS->LEVEL AS LEVEL,"
        f" RESULTS->BATTERY AS BATTERY,"
        f" RESULTS->POWER AS POWER,"
        f" RESULTS->OVERLOAD AS OVERLOAD,"
        f" THING->THING_NAME AS THING_NAME,"
        f" THING->LOCATION[0] AS LON,"
        f" THING->LOCATION[1] AS LAT"
        f" FROM {settings.NOISE_STREAM}"
        f" PARTITION BY SENSOR_NAME;"
    )
    response = _execute_ksql_commands(command1)

    print(f"KAFKA/KSQL:: STREAM {settings.NOISE_STREAM_KEYED} CREATED")


def _create_min_value_table():
    _check_stream_create_status(settings.NOISE_STREAM_KEYED)
    command = (
        f"CREATE TABLE {settings.MIN_VALUE_TABLE} AS"
        f" SELECT SENSOR_NAME, MIN(BATTERY) AS BATTERY FROM"
        f" NOISE_STREAM_KEYED GROUP BY sensor_name;"
    )
    response = _execute_ksql_commands(command)

    print(f"KAFKA/KSQL:: TABLE/TOPIC {settings.MIN_VALUE_TABLE} CREATED")


def _create_OPEN311_topic():
    _check_stream_create_status(settings.NOISE_STREAM)
    command = (
        f"CREATE STREAM {settings.ALERT_TOPIC} AS"
        f" SELECT * FROM {settings.NOISE_STREAM} WHERE"
        # f" SELECT * FROM {settings.NOISE_STREAM_KEYED} WHERE"
        # We can't create the functioning stream from keyed_stream so use original
        f" RESULTS->LEVEL > 7.0 AND RESULTS->OVERLOAD = True;"
    )
    response = _execute_ksql_commands(command)

    print (f'KAFKA/KSQL:: {settings.ALERT_TOPIC} CREATED')


def _create_loud_noise_stream():
    _check_stream_create_status(settings.NOISE_STREAM)
    command = (
        f"CREATE STREAM {settings.LOUD_NOISE_TOPIC}"
        f" AS SELECT SENSOR_NAME AS SENSOR_NAME,"
        f" LEVEL, BATTERY, LOCATION[0] AS LON,"
        f" LOCATION[1] AS LAT from {settings.NOISE_STREAM}"
        f" WHERE level > 4.0 PARTITION BY sensor_name;"
    )
    command1 = (
        f"CREATE STREAM {settings.LOUD_NOISE_TOPIC}"
        f" AS SELECT * from {settings.NOISE_STREAM_KEYED}"
        f" WHERE LEVEL > 4.0;"
    )
    response = _execute_ksql_commands(command1)

    print (f'KAFKA/KSQL:: {settings.LOUD_NOISE_TOPIC} STREAM CREATED')


def create_ksql_streams():
    _create_noise_stream()  # Registers a stream in ksql for noise topic.
    _create_sensor_name_keyed_stream() #  Registers a base keyed stream
    _create_loud_noise_stream()  # Registers and runs a stream for where level > theshold value also save to database.
    _create_min_value_table()
    _create_OPEN311_topic()  # Registers and runs stream where level > threshold value.
    _create_location_based_steam()



if __name__ == '__main__':
    create_ksql_streams()
