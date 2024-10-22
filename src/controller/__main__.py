"""Main module for running the Controller."""

from typing import List

from .controller import Controller, ControllerError


class Main:
  """Main class for running the Controller."""

  @staticmethod
  def main() -> None:
    """Initialize and run the Controller.

    This function creates an instance of the Controller class and attempts to run it.
    If a ControllerError is raised during execution, it will be caught and re-raised
    as a RuntimeError.

    Raises:
      RuntimeError: If a ControllerError occurs during the execution of the controller.

    """
    try:
      controller: Controller = Controller()
      output: List[int] = controller.run()
      for value in output:
        print(value)
    except ControllerError as e:
      raise RuntimeError from e


if __name__ == "__main__":
  Main.main()
