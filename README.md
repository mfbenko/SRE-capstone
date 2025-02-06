# SRE Capstone Project Setup Guide

## Project Prerequisites

Before you begin, ensure that you have the following installed:

1. **Docker** (includes Docker Compose)  
   Follow the installation instructions for Docker, which also installs Docker Compose:  
   [Install Docker](https://docs.docker.com/get-docker/)

2. **MySQL**
   Follow the installation instructions for MySQL. For the purposes of this demonstration the root password has been set to "root". If you don't want to set your password to "root" please edit line 55 of src/extractor.py to whatever your root password is.
   [Install MySQL](https://dev.mysql.com/downloads/installer/)

3. **Python/dependecies**
Please read documents/project documentation.pdf and install Python and all dependecies using:
```bash
   pip
```

## Enviornment Setup Instructions

### 1. Clone the Repository
Clone this repository which includes the necessary `docker-compose.yaml` file:

```bash
git clone git@github.com:mfbenko/SRE-capstone.git
cd SRE-capstone
```

### 2. Start the containers
Run the following command to start Kafka and MongoDB services:
```bash
docker-compose up -d
```
This will start all needed services in docker.

### 3. Start the application using fastAPI
Type this command to start the python scripts
```bash
uvicorn src.main:app
```

### 4. Stopping the Services
When you're done, you can stop the services by shutting down the containers:
```bash
docker-compose down
```
This will stop the containers in docker.

