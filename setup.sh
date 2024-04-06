#!/bin/bash

# Check if the script is run as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root." 1>&2
   exit 1
fi

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Docker is not installed."
        return 1
    else
        echo "Docker is installed."
        return 0
    fi
}

# Function to check if Docker Compose is installed within Docker
check_docker_compose() {
    if ! docker compose version &> /dev/null; then
        echo "Docker Compose V2 is not available."
        return 1
    else
        echo "Docker Compose V2 is available."
        return 0
    fi
}

# Function to install Docker
install_docker() {
    echo "Would you like to install Docker? (y/n)"
    read -r response
    if [[ "$response" = "y" ]]; then
        wget -O get-docker.sh https://get.docker.com
        sh get-docker.sh
        rm -f get-docker.sh
        echo "Docker is installed successfully."
    else
        echo "Docker is not installed. Exiting script."
        exit 1
    fi
}

# Function to set the .ros/log directory path
set_ros_log_path() {
    read -p "Enter the full path of your .ros/log directory (or press enter to detect automatically): " ros_log_path

    if [ -z "$ros_log_path" ]; then
        # Attempt to automatically detect the .ros/log path
        ros_log_path=$(find /home -name ".ros" -type d 2>/dev/null | grep -m1 'log$')

        if [ -z "$ros_log_path" ]; then
            echo "Unable to automatically detect the path. Please run the script again and provide the path manually."
            exit 1
        fi
    fi

    # Confirm the detected or entered path with the user
    echo "Using .ros/log path: $ros_log_path"
    read -p "Is this correct? (y/n): " confirmation

    if [[ $confirmation != "y" ]]; then
        echo "Please run the script again and provide the correct path."
        exit 1
    fi

    # Write the path to a .env file
    echo "GLP_ROS_LOG_PATH=$ros_log_path" > ./src/.env

    echo "Configuration complete. The .ros/log path is set to $ros_log_path"
}

# Main logic
echo "Checking for Docker Engine..."
check_docker || install_docker
echo "Checking for Docker Compose V2..."
check_docker_compose || { echo "Docker Compose V2 was not found. Exiting script."; exit 1; }

# If the checks pass, ask for the .ros/log directory
echo "Setting up .ros/log directory path..."
set_ros_log_path

# If everything is set up, attempt deploying the stack
cd ./src/
echo "Proceeding to deploy the stack..."
docker compose up -d
