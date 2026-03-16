---
name: dev-optimizer
description: Enforces lean documentation, debug-ready logging, and testable methods during coding tasks.
---

# Development Guidelines

## 1. Documentation & Verbosity
* **Minimalist Docs**: Do not create separate documentation files unless explicitly requested. Avoid redundant comments that explain *what* the code does; only comment on *why* complex logic exists.
* **Code as Docs**: Prioritize self-documenting code with clear variable and function naming over external README updates.

## 2. Debugging & Observability
* **Structured Logging**: Add comprehensive logging to all new methods. Use consistent log levels (INFO, DEBUG, ERROR) to track state changes and execution flow.
* **Issue Reproduction**: If a bug is reported, add loggers first to find the core issue before attempting a fix.

## 3. Testable Architecture
* **Method Design**: Generate small, pure, and testable methods. Each method should ideally do one thing and have no side effects.
* **Test-First Workflow**: Write a failing test before implementing new logic. Confirm the test fails before writing code to make it pass.
* **No Mocks**: Prefer integration-style tests or state-based validation over heavy mocking where possible.

## 4. Operational Hooks
* **Git Hygiene**: Commit changes frequently with descriptive messages. Use Git history as the primary record of progress.
