from graph_engine import HyperionGraph

graph = HyperionGraph()

# Nodes
graph.add_node(
    "payment-service",
    "SERVICE",
    {
        "name": "payment",
        "region": "ap-south-1",
        "owner": "fin-team",
        "criticality": "HIGH",
        "current_state": "HEALTHY"
    }
)

graph.add_node(
    "db-primary",
    "DATABASE",
    {
        "name": "payments-db",
        "region": "ap-south-1",
        "owner": "fin-team",
        "criticality": "HIGH",
        "current_state": "HEALTHY"
    }
)

# Edge
graph.add_edge(
    "payment-service",
    "db-primary",
    "DEPENDS_ON"
)

# Inject anomaly
graph.update_node_state("payment-service", "ANOMALOUS")

print(graph.snapshot())
