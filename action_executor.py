import boto3

ec2 = boto3.client("ec2")

def execute_action(node_id, action):
    if action == "RESTART_INSTANCE":
        print(f"⚙️ Restarting {node_id}")
        try:
            ec2.reboot_instances(InstanceIds=[node_id])
        except Exception as e:
            print(f"Restart failed: {e}")

    elif action == "SAFE_RECOVERY":
        print(f"🛡 SAFE_RECOVERY triggered for {node_id}")
        print("Simulating traffic draining and controlled restart...")

    else:
        print(f"✅ No action required for {node_id}")
