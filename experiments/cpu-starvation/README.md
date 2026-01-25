# Experiment: CPU Starvation & Vertical Scaling

**Hypothesis:** If the app is CPU throttled during a traffic spike, latency will increase. We can fix this by vertically scaling the Pod.

### Step 1: Deploy the "Weak" App
kubectl apply -f experiments/cpu-starvation/01-store-weak.yaml

### Step 2: Start the Attack
kubectl apply -f experiments/cpu-starvation/02-attack-cpu.yaml

### Step 3: Observe Throttling
1. Go to Grafana > Kubernetes / Compute Resources / Pod.
2. Select `resilience-store`.
3. Observe `CPU Usage` flattening against the `CPU Limit` (Red Line).
4. Observe the App Purchase Loop lagging.

### Step 4: Apply the Fix (Scale Up)
kubectl apply -f experiments/cpu-starvation/03-store-fixed.yaml

### Step 5: Validate
Observe `CPU Usage` graph. The Red Line (Limit) should jump up, leaving the Blue Line (Usage) room to breathe.