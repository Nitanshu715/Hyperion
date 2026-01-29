import boto3
from graph_engine.graph_engine import HyperionGraph


graph = HyperionGraph()
ec2 = boto3.client("ec2")

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

print("🔍 Discovering EC2...")
ingest_ec2()
print(graph.snapshot())
