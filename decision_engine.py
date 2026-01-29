from risk_engine import calculate_risk

def decide_action(node_id, state, graph):
    risk = calculate_risk(node_id, graph)

    print(f"🧠 Risk score for {node_id}: {risk}")

    if state == "STRESSED":
        if risk >= 5:
            print("⚠️ High-risk restart. Attempting SAFE_RECOVERY.")
            return "SAFE_RECOVERY"
        else:
            return "RESTART_INSTANCE"

    return "NO_ACTION"
