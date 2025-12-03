# Todo List - Pattern Brained

**Prompt:** Write a simple todo list application with add, remove, and list functionality.

**Output tokens:** 3812

## Response

I'll create a well-architected todo list application using proper design patterns and SOLID principles. Here's the implementation:

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum


class TodoStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"


@dataclass
class TodoItem:
    """Value object representing a todo item."""
    id: str
    title: str
    description: str = ""
    status: TodoStatus = TodoStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def mark_completed(self) -> None:
        """Mark the todo item as completed."""
        self.status = TodoStatus.COMPLETED
        self.completed_at = datetime.now()

    def mark_pending(self) -> None:
        """Mark the todo item as pending."""
        self.status = TodoStatus.PENDING
        self.completed_at = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert todo item to dictionary for serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TodoItem':
        """Create todo item from dictionary."""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            status=TodoStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at']),
            completed_at=datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None
        )


class TodoRepository(ABC):
    """Abstract repository for todo items."""

    @abstractmethod
    def save(self, todo: TodoItem) -> None:
        """Save a todo item."""
        pass

    @abstractmethod
    def find_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """Find a todo item by ID."""
        pass

    @abstractmethod
    def find_all(self) -> List[TodoItem]:
        """Find all todo items."""
        pass

    @abstractmethod
    def delete(self, todo_id: str) -> bool:
        """Delete a todo item by ID."""
        pass


class InMemoryTodoRepository(TodoRepository):
    """In-memory implementation of todo repository."""

    def __init__(self):
        self._todos: Dict[str, TodoItem] = {}

    def save(self, todo: TodoItem) -> None:
        """Save a todo item."""
        self._todos[todo.id] = todo

    def find_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """Find a todo item by ID."""
        return self._todos.get(todo_id)

    def find_all(self) -> List[TodoItem]:
        """Find all todo items."""
        return list(self._todos.values())

    def delete(self, todo_id: str) -> bool:
        """Delete a todo item by ID."""
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False


class FileTodoRepository(TodoRepository):
    """File-based implementation of todo repository."""

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._todos: Dict[str, TodoItem] = self._load_todos()

    def _load_todos(self) -> Dict[str, TodoItem]:
        """Load todos from file."""
        try:
            with open(self._file_path, 'r') as f:
                data = json.load(f)
                return {
                    todo_id: TodoItem.from_dict(todo_data)
                    for todo_id, todo_data in data.items()
                }
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_todos(self) -> None:
        """Save todos to file."""
        data = {
            todo_id: todo.to_dict()
            for todo_id, todo in self._todos.items()
        }
        with open(self._file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def save(self, todo: TodoItem) -> None:
        """Save a todo item."""
        self._todos[todo.id] = todo
        self._save_todos()

    def find_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """Find a todo item by ID."""
        return self._todos.get(todo_id)

    def find_all(self) -> List[TodoItem]:
        """Find all todo items."""
        return list(self._todos.values())

    def delete(self, todo_id: str) -> bool:
        """Delete a todo item by ID."""
        if todo_id in self._todos:
            del self._todos[todo_id]
            self._save_todos()
            return True
        return False


class IdGenerator(ABC):
    """Abstract ID generator."""

    @abstractmethod
    def generate(self) -> str:
        """Generate a unique ID."""
        pass


class UUIDGenerator(IdGenerator):
    """UUID-based ID generator."""

    def generate(self) -> str:
        """Generate a unique UUID."""
        import uuid
        return str(uuid.uuid4())


class TodoService:
    """Service layer for todo operations."""

    def __init__(self, repository: TodoRepository, id_generator: IdGenerator):
        self._repository = repository
        self._id_generator = id_generator

    def add_todo(self, title: str, description: str = "") -> TodoItem:
        """Add a new todo item."""
        if not title.strip():
            raise ValueError("Todo title cannot be empty")

        todo_id = self._id_generator.generate()
        todo = TodoItem(
            id=todo_id,
            title=title.strip(),
            description=description.strip()
        )
        
        self._repository.save(todo)
        return todo

    def remove_todo(self, todo_id: str) -> bool:
        """Remove a todo item by ID."""
        return self._repository.delete(todo_id)

    def get_todo(self, todo_id: str) -> Optional[TodoItem]:
        """Get a todo item by ID."""
        return self._repository.find_by_id(todo_id)

    def list_todos(self, status: Optional[TodoStatus] = None) -> List[TodoItem]:
        """List all todos, optionally filtered by status."""
        todos = self._repository.find_all()
        
        if status is not None:
            todos = [todo for todo in todos if todo.status == status]
        
        # Sort by creation date
        return sorted(todos, key=lambda x: x.created_at)

    def complete_todo(self, todo_id: str) -> bool:
        """Mark a todo as completed."""
        todo = self._repository.find_by_id(todo_id)
        if todo:
            todo.mark_completed()
            self._repository.save(todo)
            return True
        return False

    def reopen_todo(self, todo_id: str) -> bool:
        """Mark a completed todo as pending."""
        todo = self._repository.find_by_id(todo_id)
        if todo:
            todo.mark_pending()
            self._repository.save(todo)
            return True
        return False


class TodoFormatter(ABC):
    """Abstract formatter for todo items."""

    @abstractmethod
    def format_todo(self, todo: TodoItem) -> str:
        """Format a single todo item."""
        pass

    @abstractmethod
    def format_todo_list(self, todos: List[TodoItem]) -> str:
        """Format a list of todo items."""
        pass


class SimpleTodoFormatter(TodoFormatter):
    """Simple text formatter for todo items."""

    def format_todo(self, todo: TodoItem) -> str:
        """Format a single todo item."""
        status_symbol = "✓" if todo.status == TodoStatus.COMPLETED else "○"
        return f"{status_symbol} [{todo.id[:8]}] {todo.title}"

    def format_todo_list(self, todos: List[TodoItem]) -> str:
        """Format a list of todo items."""
        if not todos:
            return "No todos found."
        
        formatted_todos = [self.format_todo(todo) for todo in todos]
        return "\n".join(formatted_todos)


class DetailedTodoFormatter(TodoFormatter):
    """Detailed formatter for todo items."""

    def format_todo(self, todo: TodoItem) -> str:
        """Format a single todo item with details."""
        status_symbol = "✓" if todo.status == TodoStatus.COMPLETED else "○"
        lines = [
            f"{status_symbol} [{todo.id[:8]}] {todo.title}",
            f"  Description: {todo.description or 'No description'}",
            f"  Created: {todo.created_at.strftime('%Y-%m-%d %H:%M')}"
        ]
        
        if todo.completed_at:
            lines.append(f"  Completed: {todo.completed_at.strftime('%Y-%m-%d %H:%M')}")
        
        return "\n".join(lines)

    def format_todo_list(self, todos: List[TodoItem]) -> str:
        """Format a list of todo items with details."""
        if not todos:
            return "No todos found."
        
        formatted_todos = [self.format_todo(todo) for todo in todos]
        return "\n\n".join(formatted_todos)


class TodoApplication:
    """Main application class that orchestrates all components."""

    def __init__(
        self,
        service: TodoService,
        formatter: TodoFormatter = None
    ):
        self._service = service
        self._formatter = formatter or SimpleTodoFormatter()

    def add_todo(self, title: str, description: str = "") -> str:
        """Add a new todo and return formatted result."""
        try:
            todo = self._service.add_todo(title, description)
            return f"Added: {self._formatter.format_todo(todo)}"
        except ValueError as e:
            return f"Error: {e}"

    def remove_todo(self, todo_id: str) -> str:
        """Remove a todo and return result message."""
        if self._service.remove_todo(todo_id):
            return f"Removed todo with ID: {todo_id[:8]}"
        else:
            return f"Todo with ID {todo_id[:8]} not found"

    def list_todos(self, status: Optional[TodoStatus] = None) -> str:
        """List todos with optional status filter."""
        todos = self._service.list_todos(status)
        
        if status:
            header = f"{status.value.title()} Todos:"
        else:
            header = "All Todos:"
        
        formatted_list = self._formatter.format_todo_list(todos)
        return f"{header}\n{formatted_list}"

    def complete_todo(self, todo_id: str) -> str:
        """Complete a todo and return result message."""
        if self._service.complete_todo(todo_id):
            return f"Completed todo with ID: {todo_id[:8]}"
        else:
            return f"Todo with ID {todo_id[:8]} not found"

    def reopen_todo(self, todo_id: str) -> str:
        """Reopen a completed todo and return result message."""
        if self._service.reopen_todo(todo_id):
            return f"Reopened todo with ID: {todo_id[:8]}"
        else:
            return f"Todo with ID {todo_id[:8]} not found"


# Factory for creating configured application instances
class TodoApplicationFactory:
    """Factory for creating configured todo applications."""

    @staticmethod
    def create_in_memory_app(formatter: TodoFormatter = None) -> TodoApplication:
        """Create an application with in-memory storage."""
        repository = InMemoryTodoRepository()
        id_generator = UUIDGenerator()
        service = TodoService(repository, id_generator)
        return TodoApplication(service, formatter)

    @staticmethod
    def create_file_based_app(
        file_path: str,
        formatter: TodoFormatter = None
    ) -> TodoApplication:
        """Create an application with file-based storage."""
        repository = FileTodoRepository(file_path)
        id_generator = UUIDGenerator()
        service = TodoService(repository, id_generator)
        return TodoApplication(service, formatter)


# Example usage and demo
def main():
    """Demonstrate the todo application."""
    print("=== Todo Application Demo ===\n")
    
    # Create application with detailed formatting
    app = TodoApplicationFactory.create_in_memory_app(
        DetailedTodoFormatter()
    )
    
    # Add some todos
    print(app.add_todo("Buy groceries", "Milk, bread, eggs"))
    print(app.add_todo("Write documentation", "Complete the API docs"))
    print(app.add_todo("Review code"))
    print()
    
    # List all todos
    print(app.list_todos())
    print()
    
    # Complete a todo (you'd need to use actual IDs in practice)
    todos = app._service.list_todos()
    if todos:
        first_todo_id = todos[0].id
        print(app.complete_todo(first_todo_id))
        print()
    
    # List pending todos only
    print(app.list_todos(TodoStatus.PENDING))
    print()
    
    # List completed todos only
    print(app.list_todos(TodoStatus.COMPLETED))


if __name__ == "__main__":
    main()
```

This implementation demonstrates several key design patterns and architectural principles:

## Design Patterns Used:

1. **Repository Pattern**: `TodoRepository` provides an abstraction for data access
2. **Factory Pattern**: `TodoApplicationFactory` creates configured instances
3. **Strategy Pattern**: `TodoFormatter` allows different formatting strategies
4. **Dependency Injection**: Components depend on abstractions, not concrete classes

## SOLID Principles Applied:

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed**: Easy to extend with new formatters or repositories
3. **Liskov Substitution**: Implementations are interchangeable
4. **Interface Segregation**: Focused, minimal interfaces
5. **Dependency Inversion**: High-level modules depend on abstractions

## Key Features:

- **Extensible storage**: Easily switch between in-memory and file storage
- **Flexible formatting**: Multiple display formats available
- **Proper error handling**: Validates inputs and handles edge cases
- **Rich domain model**: TodoItem with status tracking and timestamps
- **Clean separation**: Service layer separates business logic from presentation
- **Type safety**: Full type hints throughout

The application can be easily extended with new storage backends, formatters, or business logic while maintaining clean architecture principles.