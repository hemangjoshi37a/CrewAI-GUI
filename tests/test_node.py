import pytest
from PySide6.QtCore import QPointF
from src.Node import Node
from src.NodeData import NodeData

@pytest.fixture
def mock_node_data():
    return NodeData(type="Agent", name="TestAgent", uniq_id="test_id")

def test_node_creation(mock_node_data):
    node = Node(mock_node_data)
    assert node.data == mock_node_data
    assert node.rect.width() == mock_node_data.width
    assert node.rect.height() == mock_node_data.height

def test_node_resize():
    node_data = NodeData(width=100, height=100)
    node = Node(node_data)
    node.setWidth(150)
    node.setHeight(120)
    assert node.rect.width() == 150
    assert node.rect.height() == 120
    assert node.data.width == 150
    assert node.data.height == 120

def test_node_position():
    node_data = NodeData(pos_x=10, pos_y=20)
    node = Node(node_data)
    assert node.pos() == QPointF(10, 20)

def test_node_ports():
    node = Node(NodeData())
    assert node.input_port.port_type == "input"
    assert node.output_port.port_type == "output"
    assert node.input_port.pos() == QPointF(0, 25)
    assert node.output_port.pos() == QPointF(node.rect.width(), 25)