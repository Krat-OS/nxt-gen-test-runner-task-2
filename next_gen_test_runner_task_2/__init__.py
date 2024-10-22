from .controller.__main__ import Main


def run() -> None:
  """Run the main function of the Controller.

  For users who import the package.
  """
  return Main.main()


__all__ = ["run"]
