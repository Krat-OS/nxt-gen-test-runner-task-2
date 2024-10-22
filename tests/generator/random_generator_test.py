import sys

from typing import Set

import pytest

from src.generator.random_generator import RandomGenerator


def test_generate_returns_integer():
  """Test that generate() returns an integer."""

  result: int = RandomGenerator.generate()
  assert isinstance(result, int)


def test_generate_within_bounds():
  """Test that generate() returns a number within system bounds."""

  result: int = RandomGenerator.generate()
  assert result >= -sys.maxsize - 1
  assert result <= sys.maxsize


def test_generate_produces_different_values():
  """Test that generate() produces different values."""

  results: Set = set()
  for _ in range(100):
    results.add(RandomGenerator.generate())
  assert len(results) > 1


@pytest.mark.parametrize("execution_count", range(10))
def test_generate_respects_bounds_multiple_times(execution_count):
  """Test bounds are respected across multiple executions."""

  result: int = RandomGenerator.generate()
  assert -sys.maxsize - 1 <= result <= sys.maxsize


def test_generate_is_static_method():
  """Test that generate() is a static method and can be called without instance."""

  assert RandomGenerator.generate() is not None
