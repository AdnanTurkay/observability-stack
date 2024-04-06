# Web Interface to Interact with TIAGo Robot: Logging

This project is a log visualization solution for systems running the [Robot Operating System](http://ros.org) (ROS), specifically designed around the [TIAGo robot](https://wiki.ros.org/Robots/TIAGo).

It is a collection of tools that provide real-time monitoring and extended logging capabilities for ROS-based systems.

The stack is a distributed system consisting of three major open-source components:
- [Grafana](https://grafana.com/oss/grafana/) is a data visualization tool, used as the frontend of the stack.
- [Loki](https://grafana.com/oss/loki/) is a log aggregation system, used to store and query logs.
- [Promtail](https://grafana.com/docs/loki/latest/send-data/promtail/) is a log collection agent for Loki.

The stack is deployed using Docker Compose and is designed to work alongside ROS.

## Getting Started

The observability stack (Grafana, Loki, Promtail) is deployed through the provided setup script.

Existing configuration files allow for seamless deployment with minimal manual setup.

### Prerequisites

- For the Grafana dashboard to display any data, the stack requires real-time or recent logs from the ROS system to be available for visualization.

    - Ensure you have correctly setup ROS environment on your system. For more information, visit [ROS Wiki](http://wiki.ros.org/ROS/Tutorials).

- Docker Engine and Docker Compose V2 are required to deploy the stack.

    - The setup script will install them if they are not already installed on the system.

### (Optional) Alternative Log Transport
By default, logs are transported to Loki using the provided Promtail agent, which relies on the file system to read log files.

However, logs can also be provided to Loki programmatically (e.g. with a Python script) using the [Loki API](https://grafana.com/docs/loki/latest/api/).

If the use of alternative methods of logs transport is desired, a Python 3 environment is required to run the provided example scripts.

#### Example setup:
```sh
sudo apt-get install python3 python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Run the example script:
```sh
python3 ./src/rosbridge.py
```

### Installation Instructions
1. Clone the repository:
```sh
git clone https://github.com/AdnanTurkay/observability-stack.git
```

2. Navigate to the project folder:
```sh
cd observability-stack
```

3. Set up and deploy the stack:
```sh
sudo ./setup.sh
```

4. Enter the full path to the ROS log directory when prompted. For example (note the specific syntax):
```sh
/home/USER/.ros/log
```

The setup script will check necessary dependencies, install them if needed, and deploy the stack using Docker Compose.

### Usage

Access the Grafana dashboard at [http://127.0.0.1:3000](http://127.0.0.1:3000).

Login is disabled by default, and the home dashboard is pre-configured.

#### To manage the stack, navigate to the project folder and use the following commands:
- To bring down the stack:
```sh
cd ./src/
sudo docker compose down
```
- To bring up the stack:
```sh
cd ./src/
sudo docker compose up -d
```

#### Basic Functionality:
- Use the time range selector in the top right corner to adjust the time range of the displayed logs.

- "Log Timeline" panel can be used to filter logs based on a time range by clicking and dragging on the timeline.

- Navigate to "Log Details" dashboard for more detailed queries, either using the link on "Latest Logs" panel or the "Dashboards" section in the top left menu.

- Use the selectors and the search bar to filter logs based on log level, ROS node, message type, and log contents (search uses regular expressions).

- Navigate to back to "Log Dashboard", either using the link on "Output" panel or the "Dashboards" section in the top left menu.

- Click on the "Explore" button in the top left corner to query logs directly and for real-time monitoring.

- Click on the "Alerting" bell icon in the left sidebar to configure alerts.

## Third-Party Software And License Information

Please refer to the LICENSE file for the license of this project, and the licenses below for the third-party software.

This project uses the following open-source third-party software:

- **Grafana**: Data visualization tool. For more information, visit [Grafana website](https://grafana.com/grafana/).

    - Grafana is distributed under the AGPLv3 license. See [Grafana license](https://github.com/grafana/grafana/blob/main/LICENSE) for more details.

- **Loki**: Log aggregation system. For more information, visit [Loki website](https://grafana.com/oss/loki/).

    - Loki is distributed under the AGPLv3 license. See [Loki license](https://github.com/grafana/loki/blob/main/LICENSE) for more details.

- **Promtail**: Log collection agent for Loki. For more details, visit [Promtail documentation](https://grafana.com/docs/loki/latest/send-data/promtail/).

    - Promtail is distributed under the AGPLv3 license. Refer to [Promtail license](https://github.com/grafana/loki/blob/main/clients/LICENSE_APACHE2) for more details.

- **Docker**: Containerization platform. For more information, visit [Docker website](https://www.docker.com/).

    - Docker Engine and Docker Compose are distributed under the Apache License 2.0. Refer to [Docker Engine license](https://github.com/moby/moby/blob/master/LICENSE) and the [Docker Compose license](https://github.com/docker/compose/blob/main/LICENSE) for more details.
