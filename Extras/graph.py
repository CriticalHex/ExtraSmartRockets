class Graph:
    class Node:
        def __init__(self, val) -> None:
            self.val = val
            self.lines: list[Graph.Line] = []

    class Line:
        def __init__(self, val, to) -> None:
            self.val = val
            self.to: Graph.Node = to

    def __init__(self) -> None:
        self.nodes: dict[str, Graph.Node] = {}

    def add_node(self, id: str, val: any):
        self.nodes[id] = Graph.Node(val)

    def add_line(self, start_node_id: str, stop_node_id: str, val: any):
        self.nodes[start_node_id].lines.append(
            Graph.Line(val, self.nodes[stop_node_id])
        )
