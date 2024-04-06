# This script is designed to integrate ROS (Robot Operating System) logs with the Loki logging system.
# It demonstrates programmatic communication of log data between ROS and Loki using the ROSBridge WebSocket interface.
#
# Key Features:
# - Fetch logs from Loki based on a specified time range using the Loki API.
# - Subscribe to ROS topics using ROSBridge WebSocket connections.
# - Format incoming ROS messages and push them to Loki for centralized logging and analysis.
#
# Dependencies:
# - requests: To make HTTP requests to the Loki API.
# - websocket-client: For establishing WebSocket connections with ROSBridge for real-time message subscriptions.
#
# Usage:
# - Ensure that Loki and ROSBridge are running and accessible via the specified URLs.
# - Adjust `LOKI_API` and `ROSBRIDGE_URL` as necessary to point to your Loki and ROSBridge instances.
# - Run this script to start listening to ROS topics and forwarding messages to Loki.

import json
import time

import requests
import websocket


LOKI_API = "http://loki:3100/loki/api/v1"
ROSBRIDGE_URL = "ws://localhost:9090/"


# An example function to fetch logs from Loki based on a time range
def fetch_loki_logs(start_ts, end_ts):
    # Loki query endpoint
    loki_query_url = f"{LOKI_API}/query_range"
    
    # Adjust the query to match log format and labels
    query = {
        'query': '{job="ros_logging"}',
        'start': start_ts,
        'end': end_ts,
        'limit': 1000
    }

    response = requests.get(loki_query_url, params=query)
    if response.status_code == 200:
        return response.json()["data"]["result"]
    else:
        return None


# WebSocket event handlers

# Send incoming ROS messages to Loki
def on_message(ws, message):
    log_entry = json.loads(message)
    # Format the message as needed and send it to Loki via HTTP POST
    formatted_message = {"streams": [{"stream": {"ros_topic": log_entry["topic"]},
                                      "values": [[str(int(time.time()*1e9)), log_entry["msg"]]]}]}
    requests.post(f"{LOKI_API}/push", json=formatted_message)

# Handle WebSocket errors
def on_error(ws, error):
    print(error)

# Handle WebSocket connection closure
def on_close(ws):
    print("ROSBRidge WebSocket connection closed.")

# Subscribe to a ROS topic upon opening the WebSocket connection (e.g. "/rosout_agg")
def on_open(ws):
    # Subscribe to a ROS topic via ROSBridge
    subscribe_message = {
        "op": "subscribe",
        "topic": "/rosout_agg"}

    ws.send(json.dumps(subscribe_message))


if __name__ == "__main__":
    # Establish a WebSocket connection with ROSBridge
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ROSBRIDGE_URL,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Register the on_open event handler to subscribe to a ROS topic
    ws.on_open = on_open
    ws.run_forever()
