import pytest
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture(autouse=True)
def run_around_tests(qapp):
    yield  # this is where the testing happens

@pytest.fixture
def mock_main_window(qapp):
    from src.MainWindow import MainWindow
    return MainWindow()