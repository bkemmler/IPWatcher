# IP Watcher

IP Watcher is a simple web application that periodically scans your network for connected devices and displays them in a web interface. It is built with FastAPI and uses nmap for network scanning.

## Features

*   **Network Scanning**: Periodically scans specified IP ranges for connected devices.
*   **Web Interface**: A simple web interface to view the list of connected devices.
*   **API**: A RESTful API to retrieve device information and manage the application's configuration.
*   **MQTT Integration**: Publishes device information to an MQTT broker.
*   **Dockerized**: The application is fully containerized and can be run with Docker Compose.

## Getting Started

To get started with IP Watcher, you will need to have Docker and Docker Compose installed.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ip-watcher.git
    cd ip-watcher
    ```

2.  **Create a `config/config.yaml` file:**

    You can use the provided `config/config.yaml.example` as a template.

3.  **Run the application:**

    ```bash
    docker-compose up -d
    ```

The application will be available at `http://localhost:8000`.

## Configuration

The application is configured using the `config/config.yaml` file. The following options are available:

*   `ip_ranges`: A list of IP ranges to scan.
*   `deep_scan_schedule`: The schedule for deep scans (cron format).
*   `ping_sweep_interval`: The interval for ping sweeps (in seconds).
*   `mqtt`: MQTT broker configuration.

## API Endpoints

The following API endpoints are available:

*   `GET /api/devices`: Retrieve a list of devices.
*   `GET /api/config`: Retrieve the current application configuration.
*   `POST /api/config`: Update the application configuration.
