"""Main module for running the Controller."""

import statistics

from typing import List

from .controller import Controller, ControllerError


class Main:
  """Main class for running the Controller."""

  @staticmethod
  def main() -> None:
    """Initialize and run the Controller.

    This function creates an instance of the Controller class and attempts to run it.
    It also prints the output and calculates and displays basic statistics (median and mean).

    Raises:
      RuntimeError: If a ControllerError occurs during the execution of the controller.

    """
    try:
      controller: Controller = Controller()
      output: List[int] = controller.run()
      for value in output:
        print(value)

      if output:
        median = statistics.median(output)
        average = statistics.mean(output)
        print(f"Median: {median}")
        print(f"Average: {average}")
    except ControllerError as e:
      raise RuntimeError from e


if __name__ == "__main__":
  Main.main()
