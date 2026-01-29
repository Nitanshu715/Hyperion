import json

def predict_future_cpu():
    try:
        with open("incident_log.json", "r") as f:
            data = json.load(f)
    except:
        print("No historical data yet.")
        return None

    if len(data) < 5:
        print("Not enough data for prediction.")
        return None

    cpus = [entry["cpu"] for entry in data]

    # Simple trend calculation (difference between last 3 readings)
    trend = (cpus[-1] - cpus[-3]) / 2

    predicted_cpu = cpus[-1] + trend

    print(f"🔮 Predicted next CPU value: {predicted_cpu:.2f}%")

    return predicted_cpu
