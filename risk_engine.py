def calculate_risk(node_id, graph):
    node = graph.nodes[node_id]
    criticality = node["metadata"]["criticality"]

    # Find dependent services
    dependents = [
        edge["from"]
        for edge in graph.edges
        if edge["to"] == node_id
    ]

    service_risk = 0

    for dep in dependents:
        dep_crit = graph.nodes[dep]["metadata"]["criticality"]
        if dep_crit == "HIGH":
            service_risk += 3
        elif dep_crit == "MEDIUM":
            service_risk += 2
        else:
            service_risk += 1

    node_risk = 2 if criticality == "MEDIUM" else 1

    total_risk = node_risk + service_risk

    return total_risk
