import pytest
from PySide6.QtWidgets import QApplication
from src.MainWindow import MainWindow
from src.CustomGraphicsView import CustomGraphicsView
from src.Node import Node
from src.NodeData import NodeData

@pytest.fixture
def app(qapp):
    return qapp

@pytest.fixture
def main_window(app):
    return MainWindow()

def test_add_node(main_window):
    view = main_window.view
    scene = view.scene()
    initial_item_count = len(scene.items())
    
    # Simulate adding a node
    view.add_node(view.mapToScene(100, 100))
    
    assert len(scene.items()) == initial_item_count + 1
    assert isinstance(scene.items()[-1], Node)

def test_remove_node(main_window):
    view = main_window.view
    scene = view.scene()
    
    # Add a node
    view.add_node(view.mapToScene(100, 100))
    initial_item_count = len(scene.items())
    
    # Remove the node
    node = scene.items()[-1]
    view.right_clicked_item = node
    view.remove_node()
    
    assert len(scene.items()) == initial_item_count - 1

def test_save_and_load(main_window, tmp_path):
    view = main_window.view
    scene = view.scene()
    
    # Add a node
    view.add_node(view.mapToScene(100, 100))
    initial_item_count = len(scene.items())
    
    # Save the scene
    save_file = tmp_path / "test_save.json"
    with patch('PySide6.QtWidgets.QFileDialog.getSaveFileName', return_value=(str(save_file), '')):
        main_window.save()
    
    # Clear the scene
    scene.clear()
    assert len(scene.items()) == 0
    
    # Load the saved scene
    with patch('PySide6.QtWidgets.QFileDialog.getOpenFileName', return_value=(str(save_file), '')):
        main_window.load()
    
    assert len(scene.items()) == initial_item_count
    assert isinstance(scene.items()[0], Node)
