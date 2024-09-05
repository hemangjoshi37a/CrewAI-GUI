import pytest
from src.NodeData import NodeData

def test_node_data_creation():
    node = NodeData(type="Agent", name="TestAgent", role="Tester")
    assert node.type == "Agent"
    assert node.name == "TestAgent"
    assert node.role == "Tester"

def test_node_data_to_dict():
    node = NodeData(type="Task", name="TestTask", description="Test description")
    node_dict = node.to_dict()
    assert node_dict['type'] == "Task"
    assert node_dict['name'] == "TestTask"
    assert node_dict['description'] == "Test description"

def test_node_data_from_dict():
    data = {
        "type": "Step",
        "name": "TestStep",
        "tool": "TestTool",
        "arg": "TestArg"
    }
    node = NodeData.from_dict(data)
    assert node.type == "Step"
    assert node.name == "TestStep"
    assert node.tool == "TestTool"
    assert node.arg == "TestArg"

def test_node_data_default_values():
    node = NodeData()
    assert node.type == ""
    assert node.name == ""
    assert len(node.tools) == 0
    assert node.uniq_id == ""