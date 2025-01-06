# SRE Capstone Project Setup Guide

## Project Prerequisites

Before you begin, ensure that you have the following installed:

1. **Docker** (includes Docker Compose)  
   Follow the installation instructions for Docker, which also installs Docker Compose:  
   [Install Docker](https://docs.docker.com/get-docker/)


## Enviornment Setup Instructions

### 1. Clone the Repository
Clone this repository which includes the necessary `docker-compose.yml` file:

```bash
git clone git@github.com:mfbenko/SRE-capstone.git
cd git@github.com:mfbenko/SRE-capstone.git
```

### 2. Start Kafka and MongoDB Using Docker Compose
Run the following command to start Kafka and MongoDB services:
```bash
docker-compose up -d
```
This will start Kafka and MongoDB containers in detached mode.

### 3. Verify the Services Are Running
To verify that the services are up and running, use the following command:
```bash
docker-compose ps
```
This will list the containers and their current status.

### 4. Stopping the Services
When you're done, you can stop the services with the following command:
```bash
docker-compose down
```
This will stop and remove all containers.

