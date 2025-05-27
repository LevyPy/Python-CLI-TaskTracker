# Python-CLI-TaskTracker

## Overview
A lightweight task management CLI application built with pure Python (no external dependencies). This application allows users to manage tasks through a command-line interface with a focus on simplicity and reliability.

## Features
- **Task Management**: Create, read, update, and delete tasks
- **Status Tracking**: Mark tasks as 'todo', 'in-progress', or 'done'
- **Filtered Views**: View tasks by status
- **Robust Error Handling**: Graceful handling of invalid inputs and file operations

## Technical Implementation
- Pure Python implementation with no external dependencies
- Sequential numeric IDs for task identification
- JSON-based storage for task persistence
- Clean architecture with separation of concerns
- Comprehensive error handling

## Usage
Run the application with Python:
```
python task_tracker_cli.py <command> [arguments]
```

Available commands:
- `add <description>` - Add a new task
- `update <id> -d <description>` - Update task description
- `update <id> -s <status>` - Update task status
- `delete <id>` - Remove a task
- `list` - List all tasks
- `list-todo` - List pending tasks
- `list-in-progress` - List tasks in progress
- `list-done` - List completed tasks
- `help` - Show help information
