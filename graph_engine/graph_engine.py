class HyperionGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, node_type, metadata):
        self.nodes[node_id] = {
            "type": node_type,
            "metadata": metadata
        }

    def add_edge(self, from_node, to_node, relation, weight=1.0):
        self.edges.append({
            "from": from_node,
            "to": to_node,
            "relation": relation,
            "weight": weight
        })

    def update_node_state(self, node_id, new_state):
        if node_id in self.nodes:
            self.nodes[node_id]["metadata"]["current_state"] = new_state

    def get_neighbors(self, node_id):
        return [
            edge for edge in self.edges
            if edge["from"] == node_id or edge["to"] == node_id
        ]

    def snapshot(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }

    def add_dependency(self, source, target):
        self.edges.append({
            "from": source,
            "to": target,
            "relation": "DEPENDS_ON",
            "weight": 1.0
        })
