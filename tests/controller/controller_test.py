import sys

from pathlib import Path
from typing import Any, List, Optional, Tuple

import pytest

from next_gen_test_runner_task_2.controller.controller import Controller, ControllerError

pytest.mark.tryfirst = True
pytest.mark.serial = True


class MockPopen:
  """Mock class for subprocess.Popen."""

  def __init__(
    self,
    args: List[str],
    stdin: Any,
    stdout: Any,
    text: bool,
    bufsize: int,
  ) -> None:
    """Initialize mock Popen instance."""
    self.args = args
    self.stdin = MockFile()
    self.stdout = MockFile()
    self._poll_value: Optional[int] = None

  def poll(self) -> Optional[int]:
    """Mock poll method."""
    return self._poll_value

  def set_poll_value(self, value: Optional[int]) -> None:
    """Set the poll return value."""
    self._poll_value = value


class MockFile:
  """Mock class for file-like objects."""

  def __init__(self) -> None:
    """Initialize mock file."""
    self.written: List[str] = []
    self.responses: List[str] = ["Hi\n"]
    self.random_responses: List[str] = ["42\n"] * 100
    self.response_index: int = 0
    self.random_index: int = 0
    self.is_random_mode: bool = False

  def write(self, text: str) -> None:
    """Mock write method."""
    self.written.append(text)
    if text == "GetRandom\n":
      self.is_random_mode = True
    elif text == "Hi\n":
      self.is_random_mode = False

  def flush(self) -> None:
    """Mock flush method."""

  def readline(self) -> str:
    """Mock readline method."""
    if self.is_random_mode:
      response = self.random_responses[self.random_index % len(self.random_responses)]
      self.random_index += 1
      return response + "\n"

    response = self.responses[self.response_index % len(self.responses)]
    self.response_index += 1
    return response + "\n"


@pytest.fixture(autouse=True)
def setup_controller(monkeypatch: pytest.MonkeyPatch) -> Controller:
  """Fixture that runs before each test, providing a fresh controller instance.
  The autouse=True parameter makes it run automatically before each test.
  """

  monkeypatch.setattr("subprocess.Popen", MockPopen)
  return Controller()


def test_controller_initialization(setup_controller: Controller) -> None:
  """Test controller initialization."""

  assert isinstance(setup_controller.child, MockPopen)


def test_check_child_process_success(setup_controller: Controller) -> None:
  """Test successful child process check."""

  setup_controller.check_child_process()
  assert "Hi\n" in setup_controller.child.stdin.written


def test_check_child_process_terminated(setup_controller: Controller) -> None:
  """Test terminated child process detection."""

  setup_controller.child._poll_value = 1

  with pytest.raises(ControllerError) as exc_info:
    setup_controller.check_child_process()
  assert "not running" in str(exc_info.value)


def test_check_child_process_unexpected_response(
  setup_controller: Controller,
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  """Test handling of unexpected response from child process."""

  def mock_readline() -> str:
    return "Unexpected\n"

  monkeypatch.setattr(setup_controller.child.stdout, "readline", mock_readline)

  with pytest.raises(ControllerError) as exc_info:
    setup_controller.check_child_process()
  assert "Unexpected response" in str(exc_info.value)


def test_process_responses_success(setup_controller: Controller) -> None:
  """Test successful processing of responses."""

  responses: List[str] = ["42", "-17", "100"]
  result: List[int] = setup_controller.process_responses(responses)
  assert result == [42, -17, 100]


def test_process_responses_invalid_input(setup_controller: Controller) -> None:
  """Test processing of invalid responses."""

  responses: List[str] = ["42", "not_a_number", "100"]

  with pytest.raises(ControllerError) as exc_info:
    setup_controller.process_responses(responses)
  assert "Invalid response" in str(exc_info.value)


def test_fetch_random_numbers(setup_controller: Controller) -> None:
  """Test fetching random numbers."""

  count: int = 5
  responses: List[str] = setup_controller.fetch_random_numbers(count)

  assert len(responses) == count
  assert all(isinstance(response, str) for response in responses)
  assert len(setup_controller.child.stdin.written) == count


def test_run_with_communication_error(
  setup_controller: Controller,
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  """Test run with communication error."""

  def mock_write(text: str) -> None:
    msg = "Mock communication error"
    raise OSError(msg)

  monkeypatch.setattr(setup_controller.child.stdin, "write", mock_write)

  with pytest.raises(ControllerError) as exc_info:
    setup_controller.check_child_process()
  assert "Error communicating" in str(exc_info.value)


def test_python_executable_path(setup_controller: Controller) -> None:
  """Test that the Python executable path is correct."""

  assert isinstance(setup_controller.child, MockPopen)
  expected_path: str = str(Path(sys.executable))
  actual_args: List[str] = setup_controller.child.args
  assert expected_path == actual_args[0]


def test_subprocess_arguments(setup_controller: Controller) -> None:
  """Test that subprocess is created with correct arguments."""

  python_path: str = str(Path(sys.executable))
  expected_args: Tuple[str, ...] = (python_path, "-m", "next_gen_test_runner_task_2.generator")

  assert isinstance(setup_controller.child, MockPopen)
  actual_args: List[str] = setup_controller.child.args
  assert all(exp == act for exp, act in zip(expected_args, actual_args))


def test_run_method_with_correct_responses(
  setup_controller: Controller, monkeypatch: pytest.MonkeyPatch
) -> None:
  """Test the complete run method of the Controller class with correct responses."""

  def mock_readline() -> str:
    if setup_controller.child.stdin.written[-1] == "Hi\n":
      return "Hi\n"
    return "42\n"

  monkeypatch.setattr(setup_controller.child.stdout, "readline", mock_readline)

  result: List[int] = setup_controller.run()
  assert len(result) == 100
  assert all(isinstance(number, int) for number in result)
  assert all(number == 42 for number in result)
