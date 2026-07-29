# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A basic Python calculator project with both a functional interface (`add()`, `subtract()`, etc.) and an object-oriented interface (`Calculator` class with method chaining).

## Commands

- **Run the app**: `python main.py`
- **Run all tests**: `python -m pytest`
- **Run a single test file**: `python -m pytest test_calculator.py -v`
- **Run a specific test**: `python -m pytest test_calculator.py::TestFunctional::test_add -v`

## Project Structure

| File | Purpose |
|---|---|
| `calculator.py` | Core module — pure functions (`add`, `subtract`, etc.) and `Calculator` class |
| `main.py` | Entry point demonstrating usage of the module |
| `test_calculator.py` | Pytest test suite |
| `requirements.txt` | Dependencies (pytest) |

## Architecture

- **Functional core** → `calculator.py` exports stateless math functions
- **Object wrapper** → `Calculator` class wraps those functions with a mutable `_result` state and supports method chaining (each method returns `self`)
- **Type hints** → All public functions are fully typed with `Number = Union[int, float]`
- **Testing** → Tests are grouped into `TestFunctional` (pure functions) and `TestCalculator` (class behavior), including edge cases like division by zero
