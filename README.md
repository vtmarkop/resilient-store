🛡️ Resilient Store: Chaos Engineering Lab

A practical demonstration of Kubernetes Resilience using Chaos Mesh. This project simulates a real-world e-commerce scenario where a critical dependency (Redis Database) fails repeatedly, testing the application's ability to degrade gracefully instead of crashing.
🏗️ Architecture

The application consists of two microservices running on Kubernetes:

    Store API (store-app): A Python Flask application that handles "Buy" requests.

    Inventory DB (redis-db): A Redis database that stores the stock count.

The Failure Scenario: We use Chaos Mesh to inject a PodKill fault, assassinating the Redis database every 20 seconds to simulate a sudden infrastructure outage.
🧪 The Experiment
Component	State	Expected Behavior
Normal Operation	Redis is UP	API returns 200 OK. Stock decreases.
Chaos Event	Redis is DOWN	API catches the connection error.
Resilience Logic	Handling	API returns 503 Service Unavailable with a custom error message: "Store is temporarily offline." The app does not crash.
🚀 How to Run
1. Build the Image

Point your terminal to Minikube's Docker daemon and build the app:
Bash

eval $(minikube -p minikube docker-env)  # (Linux/Mac)
# Or for PowerShell:
# & minikube -p minikube docker-env --shell powershell | Invoke-Expression

docker build -t resilient-store:latest app/

2. Deploy Infrastructure
Bash

kubectl apply -f k8s/

3. Initialize Stock

Open a tunnel to access the API:
Bash

kubectl port-forward svc/store-service 8080:80

Then reset the inventory to 100:
Bash

curl -X POST http://localhost:8080/reset

4. Unleash the Chaos 💥

Apply the schedule to kill Redis every 20 seconds:
Bash

kubectl apply -f experiments/kill-redis.yaml

📂 Project Structure

    app/: Python Flask source code and Dockerfile.

    k8s/: Kubernetes manifests for Deployment and Services.

    experiments/: Chaos Mesh configuration files.