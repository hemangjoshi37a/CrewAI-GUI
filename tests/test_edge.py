import pytest
from PySide6.QtCore import QPointF
from src.Edge import Edge
from src.Node import Node
from src.NodeData import NodeData

@pytest.fixture
def mock_nodes(qapp):
    node1 = Node(NodeData(uniq_id="node1", type="Agent", name="TestAgent1"))
    node2 = Node(NodeData(uniq_id="node2", type="Agent", name="TestAgent2"))
    return node1, node2

def test_edge_creation(mock_nodes):
    source_node, dest_node = mock_nodes
    edge = Edge(source_node.output_port)
    assert edge.source_port == source_node.output_port
    assert edge.source_id == "node1"
    assert edge.destination_port is None
    assert edge.destination_id is None

def test_edge_set_destination(mock_nodes):
    source_node, dest_node = mock_nodes
    edge = Edge(source_node.output_port)
    edge.set_destination(dest_node.input_port)
    assert edge.destination_port == dest_node.input_port
    assert edge.destination_id == "node2"
    assert "node2" in source_node.data.nexts
    assert "node1" in dest_node.data.prevs

def test_edge_update_position(mock_nodes):
    source_node, dest_node = mock_nodes
    edge = Edge(source_node.output_port)
    edge.set_destination(dest_node.input_port)
    edge.update_position()
    assert edge.path() is not None

def test_edge_remove(mock_nodes):
    source_node, dest_node = mock_nodes
    edge = Edge(source_node.output_port)
    edge.set_destination(dest_node.input_port)
    edge.remove()
    assert edge not in source_node.output_port.edges
    assert edge not in dest_node.input_port.edges
    assert dest_node.data.uniq_id not in source_node.data.nexts
    assert source_node.data.uniq_id not in dest_node.data.prevs