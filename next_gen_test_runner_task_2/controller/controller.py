"""Controller module for managing the generator process."""

import subprocess
import sys

from pathlib import Path
from typing import List


class ControllerError(Exception):
  """Custom exception class for controller errors."""

  def __init__(self, message: str) -> None:
    """Initialize the exception with a custom message.

    Args:
      message (str): The message to display when the exception is raised.

    """
    super().__init__(message)


class Controller:
  """Controller class responsible for managing the generator subprocess."""

  def __init__(self) -> None:
    """Initialize the controller with a generator subprocess.

    Creates a new subprocess running the generator module directly using Python.
    """
    python_path: str = str(Path(sys.executable))

    self.child: subprocess.Popen = subprocess.Popen(  # noqa: S603
      [python_path, "-m", "next_gen_test_runner_task_2.generator"],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      text=True,
      bufsize=1,
    )

  def check_child_process(self) -> None:
    """Check if the generator subprocess is still running and responding.

    Raises:
        ControllerError: If the generator subprocess is not running, has terminated,
                    or returns an unexpected response.

    """
    if self.child.poll() is not None:
      msg: str = "Generator subprocess is not running/has terminated."
      raise ControllerError(msg)

    try:
      self.child.stdin.write("Hi\n")
      self.child.stdin.flush()

      response: str = self.child.stdout.readline().strip()

      if response != "Hi":
        msg: str = f"Unexpected response from generator subprocess: {response}"
        raise ControllerError(msg)

    except (OSError, ValueError) as e:
      msg: str = f"Error communicating with generator subprocess: {e}"
      raise ControllerError(msg) from e

  def run(self) -> List[int]:
    """Run the controller process.

    This method performs the following steps:
    1. Checks the status of the child process.
    2. Fetches a list of random numbers.
    3. Sends a shutdown command to the child process.
    4. Processes the fetched responses into a list of integers.
    5. Returns the sorted list of integers.

    Returns:
      List[int]: A sorted list of integers obtained from processing the responses.

    """
    self.check_child_process()

    count: int = 100

    responses: List[str] = self.fetch_random_numbers(count)

    self.child.stdin.write("Shutdown\n")

    numbers: List[int] = self.process_responses(responses)

    return sorted(numbers)

  def process_responses(self, responses: List[str]) -> List[int]:
    """Process a list of string responses and convert them to integers.

    Args:
      responses (List[str]): A list of strings, each expected to be an integer.

    Returns:
      List[int]: A list of integers converted from the input strings.

    Raises:
      ControllerError: If any of the strings in the input list cannot be converted to an integer.

    """
    numbers: List[int] = []
    for response in responses:
      try:
        number: int = int(response)
        numbers.append(number)
      except ValueError as e:
        msg: str = f"Invalid response received, not an integer: {response}"
        raise ControllerError(msg) from e
    return numbers

  def fetch_random_numbers(self, count: int) -> List[str]:
    """Fetch a specified number of random numbers from a child process.

    Args:
      count (int): The number of random numbers to fetch.

    Returns:
      List[str]: A list of random numbers as strings.

    """
    responses: List[str] = []

    for _ in range(count):
      self.child.stdin.write("GetRandom\n")
      self.child.stdin.flush()

      response: str = self.child.stdout.readline().strip()
      responses.append(response)

    return responses
