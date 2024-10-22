"""Random number generator module."""

import random
import sys


class RandomGenerator:
  """Random number generator class."""

  def generate() -> int:
    """Generate a random integer within the range of the system's maximum size.

    Returns:
      int: A randomly generated integer between -sys.maxsize - 1 and sys.maxsize.

    """
    return random.randint(-sys.maxsize - 1, sys.maxsize)
