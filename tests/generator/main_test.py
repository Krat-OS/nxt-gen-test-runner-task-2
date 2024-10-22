import pytest

from src.generator.__main__ import Main


def test_hi_command(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
  """Test the 'Hi' command functionality."""

  inputs = iter(["Hi", "Shutdown"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))

  Main.main()
  captured = capsys.readouterr()

  assert "Hi" in captured.out


def test_get_random_command(
  monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
  """Test the 'GetRandom' command functionality."""

  inputs = iter(["GetRandom", "Shutdown"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))
  monkeypatch.setattr("src.generator.random_generator.RandomGenerator.generate", lambda: 42)

  Main.main()
  captured = capsys.readouterr()

  assert "42" in captured.out


def test_shutdown_command(
  monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
  """Test the 'Shutdown' command functionality."""

  inputs = iter(["Shutdown"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))

  Main.main()
  captured = capsys.readouterr()

  assert captured.out == ""


def test_unknown_command(
  monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
  """Test handling of unknown commands."""

  inputs = iter(["InvalidCommand", "Shutdown"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))

  Main.main()
  captured = capsys.readouterr()

  assert "Unknown command" in captured.out


def test_multiple_commands_sequence(
  monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
  """Test a sequence of multiple commands."""

  inputs = iter(["Hi", "GetRandom", "InvalidCommand", "Shutdown"])
  monkeypatch.setattr("builtins.input", lambda: next(inputs))
  monkeypatch.setattr("src.generator.random_generator.RandomGenerator.generate", lambda: 42)

  Main.main()
  captured = capsys.readouterr()
  output_lines = captured.out.splitlines()

  assert output_lines[0] == "Hi"
  assert output_lines[1] == "42"
  assert output_lines[2] == "Unknown command"


def test_keyboard_interrupt_handling(monkeypatch: pytest.MonkeyPatch) -> None:
  """Test handling of KeyboardInterrupt."""

  def raise_keyboard_interrupt() -> None:
    raise KeyboardInterrupt

  monkeypatch.setattr("builtins.input", raise_keyboard_interrupt)

  with pytest.raises(KeyboardInterrupt):
    Main.main()
