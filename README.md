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
Clone this repository which includes the necessary `deployment.yml` file:

```bash
git clone git@github.com:mfbenko/SRE-capstone.git
cd SRE-capstone
```

### 2. Start Kafka, MongoDB, Prometheus, and Grafana Kubernetes Deployment 
Run the following command to start Kafka and MongoDB services:
```bash
kubectl apply -f deployment.yaml
```
This will start all needed services in a kubernetes cluster.

### 3. Port forward the services
Services must be port forwarded so that they can run as a daemon and be reachable from the application
```bash
Start-Process -FilePath "kubectl" -ArgumentList "port-forward svc/kafka-service 9092:9092"
Start-Process -FilePath "kubectl" -ArgumentList "port-forward svc/zookeeper-service 2181:2181"
Start-Process -FilePath "kubectl" -ArgumentList "port-forward svc/mongo-service 27017:27017"
Start-Process -FilePath "kubectl" -ArgumentList "port-forward svc/prometheus-service 9090:9090"
Start-Process -FilePath "kubectl" -ArgumentList "port-forward svc/grafana-service 3000:3000"
```

### 4. Stopping the Services
When you're done, you can stop the services by deleting the deployment:
```bash
kubectl delete deployment my-web-dep
```
This will stop the pods in Kubernetes.

