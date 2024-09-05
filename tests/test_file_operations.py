import pytest
import json
from unittest.mock import mock_open, patch
from src.file_operations import save, load
from src.Node import Node
from src.NodeData import NodeData

@pytest.fixture
def mock_scene():
    class MockScene:
        def __init__(self):
            self.items = []
            self.node_counter = 1

        def addItem(self, item):
            self.items.append(item)

    return MockScene()

def test_save(mock_scene):
    node_data = NodeData(type="Agent", name="TestAgent", uniq_id="test_id")
    node = Node(node_data)
    mock_scene.addItem(node)
    mock_scene.items = MagicMock(return_value=[node])

    mock_file = mock_open()
    with patch('builtins.open', mock_file):
        with patch('PySide6.QtWidgets.QFileDialog.getSaveFileName', return_value=('test.json', '')):
            save(mock_scene)

    mock_file().write.assert_called_once()
    written_data = json.loads(mock_file().write.call_args[0][0])
    assert len(written_data['nodes']) == 1
    assert written_data['nodes'][0]['type'] == "Agent"
    assert written_data['nodes'][0]['name'] == "TestAgent"
    assert written_data['node_counter'] == 1

def test_load(mock_scene):
    mock_data = {
        "nodes": [
            {"type": "Agent", "name": "TestAgent", "uniq_id": "test_id", "nexts": [], "prevs": []}
        ],
        "node_counter": 2
    }

    mock_file = mock_open(read_data=json.dumps(mock_data))
    with patch('builtins.open', mock_file):
        with patch('PySide6.QtWidgets.QFileDialog.getOpenFileName', return_value=('test.json', '')):
            load(mock_scene)

    assert len(mock_scene.items) == 1
    assert isinstance(mock_scene.items[0], Node)
    assert mock_scene.items[0].data.type == "Agent"
    assert mock_scene.items[0].data.name == "TestAgent"
    assert mock_scene.node_counter == 2
