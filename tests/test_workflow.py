import pytest
from src.WorkFlow import create_agent, create_task, topological_sort_tasks
from src.NodeData import NodeData

@pytest.fixture
def mock_llm():
    class MockLLM:
        def __init__(self):
            pass
        def bind(self, **kwargs):
            return self
    return MockLLM()

def test_create_agent(mock_llm):
    node_data = NodeData(type="Agent", name="TestAgent", role="Tester", goal="Test things")
    with patch('crewai.Agent') as MockAgent:
        agent = create_agent(node_data, mock_llm)
        MockAgent.assert_called_once_with(
            role="Tester",
            goal="Test things",
            backstory="",
            verbose=True,
            allow_delegation=False,
            llm=mock_llm,
            tools=[]
        )

def test_create_task(mock_llm):
    agent_node = NodeData(type="Agent", name="TestAgent")
    task_node = NodeData(type="Task", name="TestTask", description="Test description", agent="TestAgent")
    
    with patch('crewai.Agent') as MockAgent, patch('crewai.Task') as MockTask:
        agent = create_agent(agent_node, mock_llm)
        task = create_task(task_node, agent, {}, {})
        
        MockTask.assert_called_once_with(
            description="Test description",
            expected_output="",
            agent=agent,
            steps=[],
            dependencies=[]
        )

def test_topological_sort_tasks():
    task1 = NodeData(type="Task", uniq_id="1", nexts=["2"])
    task2 = NodeData(type="Task", uniq_id="2", prevs=["1"], nexts=["3"])
    task3 = NodeData(type="Task", uniq_id="3", prevs=["2"])
    sorted_tasks = topological_sort_tasks([task2, task3, task1])
    assert [task.uniq_id for task in sorted_tasks] == ["1", "2", "3"]
