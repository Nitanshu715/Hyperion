import boto3
import json
from datetime import datetime, timedelta, timezone
from graph_engine.graph_engine import HyperionGraph
from decision_engine import decide_action
from action_executor import execute_action
from prediction_engine import predict_future_cpu

graph = HyperionGraph()
ec2 = boto3.client("ec2")
cloudwatch = boto3.client("cloudwatch")


def ingest_ec2():
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]

            graph.add_node(
                instance_id,
                "INSTANCE",
                {
                    "name": instance_id,
                    "region": ec2.meta.region_name,
                    "owner": "aws",
                    "criticality": "MEDIUM",
                    "current_state": instance["State"]["Name"].upper()
                }
            )


def log_incident(node_id, cpu, action):
    record = {
        "time": str(datetime.now()),
        "node": node_id,
        "cpu": cpu,
        "action": action
    }

    try:
        with open("incident_log.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(record)

    with open("incident_log.json", "w") as f:
        json.dump(data, f, indent=2)


def update_cpu_and_decide():
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=10)

    for node_id in list(graph.nodes.keys()):
        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": node_id}],
            StartTime=start,
            EndTime=end,
            Period=300,
            Statistics=["Average"],
        )

        datapoints = response["Datapoints"]

        if datapoints:
            real_cpu = datapoints[-1]["Average"]

            # ---- SIMULATED TREND ENGINE ----
            try:
                with open("sim_counter.txt", "r") as f:
                    step = int(f.read().strip())
            except:
                step = 0

            cpu = real_cpu + (step * 15)

            with open("sim_counter.txt", "w") as f:
                f.write(str(step + 1))

            print(f"{node_id} CPU: {cpu:.2f}%")

            if cpu > 70:
                graph.update_node_state(node_id, "STRESSED")
                print(f"🚨 ANOMALY EVENT on {node_id}")
            else:
                graph.update_node_state(node_id, "HEALTHY")

            state = graph.nodes[node_id]["metadata"]["current_state"]
            action = decide_action(node_id, state, graph)
            print(f"🤖 Decision: {action}")

            execute_action(node_id, action)
            log_incident(node_id, cpu, action)


print("🔍 Discovering EC2...")
ingest_ec2()

graph.add_node(
    "payment-service",
    "SERVICE",
    {
        "name": "payment-service",
        "region": "ap-south-1",
        "owner": "app-team",
        "criticality": "HIGH",
        "current_state": "HEALTHY"
    }
)

graph.add_dependency("payment-service", list(graph.nodes.keys())[0])

print("📊 Checking CPU + making decisions...")
update_cpu_and_decide()

predicted = predict_future_cpu()

if predicted and predicted > 70:
    print("⚠️ Prediction: CPU likely to exceed threshold soon!")

print("\n🧠 Final System Snapshot:")
print(graph.snapshot())
