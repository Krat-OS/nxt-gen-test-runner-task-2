"""Main module for the generator package."""

from .random_generator import RandomGenerator


class Main:
  """Main class for the generator package."""

  @staticmethod
  def main() -> None:
    """Run an interactive command-line interface.

    Continuously prompt the user for input commands and perform actions
    based on the command entered.

    Available commands:
    - "Hi": Prints "Hi".
    - "GetRandom": Prints a randomly generated value using the RandomGenerator class.
    - "Shutdown": Stops the loop and exits the program.
    - Any other command: Prints "Unknown command".

    The loop runs until the "Shutdown" command is entered.
    """
    is_running: bool = True
    while is_running:
      input_command: str = input()
      match input_command:
        case "Hi":
          print("Hi")
        case "GetRandom":
          print(RandomGenerator.generate())
        case "Shutdown":
          is_running = False
        case _:
          print("Unknown command")


if __name__ == "__main__":
  Main.main()
