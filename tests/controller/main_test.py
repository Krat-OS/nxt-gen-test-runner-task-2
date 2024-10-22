from typing import Any, List

import pytest

from next_gen_test_runner_task_2.controller.__main__ import Main
from next_gen_test_runner_task_2.controller.controller import Controller, ControllerError


def test_successful_execution(
  monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
  """Test successful execution of the controller."""

  test_values: List[int] = [42, 100, 200]

  def mock_init(self: Any) -> None:
    pass

  def mock_run(self: Any) -> List[int]:
    return test_values

  monkeypatch.setattr(Controller, "__init__", mock_init)
  monkeypatch.setattr(Controller, "run", mock_run)

  Main.main()
  captured: pytest.CaptureFixture[str] = capsys.readouterr()
  output_lines: List[str] = captured.out.splitlines()

  assert len(output_lines) == len(test_values) + 2
  for expected, actual in zip(test_values, output_lines[: len(test_values)]):
    assert str(expected) == actual

  assert output_lines[-2] == f"Median: {100}"
  assert output_lines[-1] == f"Average: {114}"


def test_controller_error_handling(monkeypatch: pytest.MonkeyPatch) -> None:
  """Test handling of ControllerError."""

  def mock_init(self: Any) -> None:
    pass

  def mock_run(self: Any) -> List[int]:
    msg: str = "Test error"
    raise ControllerError(msg)

  monkeypatch.setattr(Controller, "__init__", mock_init)
  monkeypatch.setattr(Controller, "run", mock_run)

  with pytest.raises(RuntimeError) as exc_info:
    Main.main()

  assert isinstance(exc_info.value.__cause__, ControllerError)


def test_empty_output(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
  """Test handling of empty output from controller."""

  def mock_init(self: Any) -> None:
    pass

  def mock_run(self: Any) -> List[int]:
    return []

  monkeypatch.setattr(Controller, "__init__", mock_init)
  monkeypatch.setattr(Controller, "run", mock_run)

  Main.main()
  captured: pytest.CaptureFixture[str] = capsys.readouterr()

  assert captured.out == ""


def test_large_output(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
  """Test handling of large output from controller."""

  test_values: List[int] = list(range(1000))

  def mock_init(self: Any) -> None:
    pass

  def mock_run(self: Any) -> List[int]:
    return test_values

  monkeypatch.setattr(Controller, "__init__", mock_init)
  monkeypatch.setattr(Controller, "run", mock_run)

  Main.main()
  captured: pytest.CaptureFixture[str] = capsys.readouterr()
  output_lines: List[str] = captured.out.splitlines()

  assert len(output_lines) == len(test_values) + 2
  for expected, actual in zip(test_values, output_lines[: len(test_values)]):
    assert str(expected) == actual

  assert output_lines[-2] == f"Median: {499.5}"
  assert output_lines[-1] == f"Average: {499.5}"


def test_negative_values(
  monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
  """Test handling of negative values in output."""

  test_values: List[int] = [-42, -100, -200]

  def mock_init(self: Any) -> None:
    pass

  def mock_run(self: Any) -> List[int]:
    return test_values

  monkeypatch.setattr(Controller, "__init__", mock_init)
  monkeypatch.setattr(Controller, "run", mock_run)

  Main.main()
  captured: pytest.CaptureFixture[str] = capsys.readouterr()
  output_lines: List[str] = captured.out.splitlines()

  assert len(output_lines) == len(test_values) + 2
  for expected, actual in zip(test_values, output_lines[: len(test_values)]):
    assert str(expected) == actual

  assert output_lines[-2] == f"Median: {-100}"
  assert output_lines[-1] == f"Average: {-114}"
