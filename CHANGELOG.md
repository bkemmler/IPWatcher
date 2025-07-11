# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-07-11

### Added

- **Settings Page**: A new settings page has been added to the web interface, allowing users to configure the application's parameters, such as IP ranges, scan schedules, and more.
- **Health Check Endpoint**: A `/api/health` endpoint has been added to the API to allow for container orchestration tools to monitor the application's health.

### Changed

- **Dockerfile Optimization**: The Dockerfile has been optimized for smaller image size and better caching.
- **Version Update**: The application version has been updated to 3.0.0.

## [2.0.0] - 2025-07-09

This is a major release that includes a complete overhaul of the application, introducing a modern web interface, enhanced scanning capabilities, and a more robust backend.

### Added

- **Modern Web Interface**: The entire frontend has been rebuilt using **React** and **Bootstrap**, providing a responsive, interactive, and user-friendly experience.
- **Detailed Device Information**: The scanner now collects and displays detailed information for each device, including its **MAC address, device vendor, OS details**, and a list of **open ports**.
- **User-Defined Device Names**: Users can now assign custom, friendly names to discovered devices directly from the web interface.
- **Historical Data Tracking**: The application now records and stores the online/offline status history for each device, allowing for better network monitoring.
- **Manual Scan Trigger**: A "Manual Scan" button has been added to the web interface to allow users to trigger a network scan on demand.
- **CSV Export**: Users can now export the complete list of discovered devices and their details to a CSV file directly from the web interface.
- **Enhanced Nmap Scanning**: The scanning logic now uses more advanced Nmap features to perform OS detection and more reliable host discovery.
- **New API Endpoints**:
  - `GET /api/version`: Returns the current application version.
  - `POST /api/scan`: Triggers a new network scan.
  - `PUT /api/devices/{device_id}`: Allows updating a device's name.
- **Application Versioning**: The application now has a version (v2.0.0), which is displayed in the UI and accessible via the API.
- **Unit Tests**: A suite of unit tests for the backend API has been added using `pytest` to ensure reliability and correctness.
- **Multi-stage Dockerfile**: The Docker build process has been updated to a multi-stage build, which first compiles the React frontend and then copies the artifacts into the final Python image for a more efficient and secure container.

### Changed

- **Primary Device Identifier**: Devices are now tracked by their **MAC address** instead of their IP address. This provides more reliable tracking of devices across IP changes.
- **Backend Refactoring**: The backend database models, Pydantic schemas, and CRUD operations have been significantly refactored to support the new features and data structure.
- **Scanning Logic**: The previous `ping_sweep` and `deep_scan` functions have been consolidated into a single, more efficient `scan_network` function.

### Removed

- **Old Static Frontend**: The original, simple `index.html` and `script.js` files have been removed and replaced by the new React application.
