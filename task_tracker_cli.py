import sys
import json
import os
import datetime

def load_tasks():
    """Load tasks from the JSON file or create a new file if it doesn't exist.
    
    Reads the tasks.json file and parses its contents. Handles various edge cases:
    - Non-existent file
    - Empty file
    - Single task object instead of an array
    - String IDs that should be integers
    
    Returns:
        list: A list of task dictionaries, or an empty list if no tasks exist
    """
    if not os.path.exists("tasks.json"):
        return []
    
    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():
                return []
            data = json.loads(content)
            # Check if the file contains a list or a single dictionary
            if isinstance(data, dict):
                # If it's a dictionary, convert to a list with one item
                return [data] if "id" in data else []

            # Convert numeric string IDs to integers
            for task in data:
                if isinstance(task["id"], str) and task["id"].isdigit():
                    task["id"] = int(task["id"])
            
            return data
    except json.JSONDecodeError:
        print("Erro: O arquivo tasks.json está corrompido. Criando um novo arquivo.")
        return []

def save_tasks(tasks):
    """Save tasks to the JSON file.
    
    Writes the task list to tasks.json with proper formatting and UTF-8 encoding.
    
    Args:
        tasks: List of task dictionaries to save
    """
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)

def get_next_id(tasks):
    """Calculate the next available sequential ID for a new task.
    
    Finds the highest existing numeric ID and returns the next number in sequence.
    If no tasks exist, starts with ID 1.
    
    Args:
        tasks: List of existing task dictionaries
        
    Returns:
        int: The next available ID number
    """
    # If no tasks exist, start with ID 1
    if not tasks:
        return 1
    
    # Find the highest numeric ID
    max_id = 0
    for task in tasks:
        task_id = task["id"]
        # Check if ID is numeric
        if isinstance(task_id, int) or (isinstance(task_id, str) and task_id.isdigit()):
            current_id = int(task_id)
            if current_id > max_id:
                max_id = current_id
    
    # Return the next ID in sequence
    return max_id + 1

def add_task(description):
    """Create and save a new task with the given description.
    
    Creates a task with a sequential ID, sets initial status to 'todo',
    and records creation and update timestamps.
    
    Args:
        description: Text description of the task
    """
    tasks = load_tasks()
    
    # Generate sequential ID
    next_id = get_next_id(tasks)
    
    new_task = {
        "id": next_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.datetime.now().isoformat(),
        "updatedAt": datetime.datetime.now().isoformat()
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Tarefa adicionada: {description} (ID: {next_id})")

def update_task(task_id, description=None, status=None):
    """Update a task's description or status.
    
    Finds a task by ID and updates either its description, status, or both.
    Updates the 'updatedAt' timestamp to reflect the change.
    
    Args:
        task_id: ID of the task to update
        description: New description text (optional)
        status: New status value (optional, must be 'todo', 'in-progress', or 'done')
    """
    tasks = load_tasks()
    
    # Convert task_id to integer if it's a numeric string
    if isinstance(task_id, str) and task_id.isdigit():
        task_id = int(task_id)
    
    for task in tasks:
        # Convert task ID to integer if it's a numeric string
        current_id = task["id"]
        if isinstance(current_id, str) and current_id.isdigit():
            current_id = int(current_id)
        
        if current_id == task_id:
            if description:
                task["description"] = description
            if status:
                if status not in ["todo", "in-progress", "done"]:
                    print(f"Erro: Status inválido '{status}'. Use 'todo', 'in-progress' ou 'done'.")
                    return
                task["status"] = status
            
            task["updatedAt"] = datetime.datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Tarefa atualizada: {task['description']} (ID: {task_id})")
            return
    
    print(f"Erro: Tarefa com ID {task_id} não encontrada.")

def delete_task(task_id):
    """Remove a task from the task list.
    
    Finds a task by ID and removes it from storage.
    Handles numeric string IDs by converting them to integers for comparison.
    
    Args:
        task_id: ID of the task to delete
    """
    tasks = load_tasks()
    initial_count = len(tasks)
    
    # Convert task_id to integer if it's a numeric string
    if isinstance(task_id, str) and task_id.isdigit():
        task_id = int(task_id)
    
    # Filter tasks, considering numeric IDs
    filtered_tasks = []
    for task in tasks:
        current_id = task["id"]
        if isinstance(current_id, str) and current_id.isdigit():
            current_id = int(current_id)
        
        if current_id != task_id:
            filtered_tasks.append(task)
    
    if len(filtered_tasks) < initial_count:
        save_tasks(filtered_tasks)
        print(f"Tarefa com ID {task_id} foi removida.")
    else:
        print(f"Erro: Tarefa com ID {task_id} não encontrada.")

def list_tasks(status_filter=None):
    """Display a formatted list of tasks with optional status filtering.
    
    Loads tasks from storage, applies status filtering if specified,
    and displays them in a tabular format with ID, description, status,
    and timestamps.
    
    Args:
        status_filter: Optional filter to show only tasks with a specific status
    """
    tasks = load_tasks()
    
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return
    
    # Ensure no duplicate tasks in the listing
    unique_tasks = []
    seen_ids = set()
    
    for task in tasks:
        # Normalize ID for comparison
        task_id = task["id"]
        if isinstance(task_id, str) and task_id.isdigit():
            task_id = int(task_id)
        
        # Skip tasks with IDs already seen
        if task_id in seen_ids:
            continue
        
        seen_ids.add(task_id)
        unique_tasks.append(task)
    
    # Apply status filter if provided
    filtered_tasks = unique_tasks
    if status_filter:
        filtered_tasks = [task for task in unique_tasks if task["status"] == status_filter]
    
    if not filtered_tasks:
        print(f"Nenhuma tarefa com status '{status_filter}' encontrada.")
        return
    
    print(f"\n{'ID':<5} | {'Descrição':<30} | {'Status':<12} | {'Criado em':<25} | {'Atualizado em':<25}")
    print("-" * 110)
    
    # Sort tasks by ID for display
    filtered_tasks.sort(key=lambda x: int(x["id"]) if isinstance(x["id"], str) and x["id"].isdigit() else x["id"])
    
    for task in filtered_tasks:
        # Format ID for display
        display_id = str(task["id"])
        
        # Get date values if they exist
        created_at = "N/A"
        if "createdAt" in task:
            created_at = task["createdAt"].split("T")[0] if "T" in task["createdAt"] else task["createdAt"]
        elif "createdAt1" in task:  # Handle inconsistent field in JSON file
            created_at = task["createdAt1"].split("T")[0] if "T" in task["createdAt1"] else task["createdAt1"]
            
        updated_at = "N/A"
        if "updatedAt" in task:
            updated_at = task["updatedAt"].split("T")[0] if "T" in task["updatedAt"] else task["updatedAt"]
        
        # Ensure description is a string
        description = task["description"]
        if isinstance(description, list):
            description = ", ".join(description)
        
        print(f"{display_id:<5} | {description[:30]:<30} | {task['status']:<12} | {created_at:<25} | {updated_at:<25}")

def print_help():
    """Display usage instructions and available commands.
    
    Prints a formatted help message showing all available commands
    and their parameters.
    """
    print("\nTask Tracker CLI - Gerenciador de Tarefas")
    print("\nUso:")
    print("  python task_tracker_cli.py <comando> [argumentos]")
    print("\nComandos:")
    print("  add <descrição>                   - Adicionar uma nova tarefa")
    print("  update <id> -d <descrição>        - Atualizar a descrição de uma tarefa")
    print("  update <id> -s <status>           - Atualizar o status de uma tarefa (todo, in-progress, done)")
    print("  delete <id>                       - Remover uma tarefa")
    print("  list                              - Listar todas as tarefas")
    print("  list-todo                         - Listar tarefas pendentes")
    print("  list-in-progress                  - Listar tarefas em andamento")
    print("  list-done                         - Listar tarefas concluídas")
    print("  help                              - Mostrar esta ajuda")



def main(args):
    """Process command-line arguments and execute the appropriate function.
    
    Parses command-line arguments and routes to the correct function based on
    the command. Handles help requests, task creation, updates, deletion, and listing.
    
    Args:
        args: List of command-line arguments (excluding the script name)
    """
    if not args or args[0] in ["-h", "--help", "help"]:
        print_help()
        return
    
    command = args[0]
    
    if command == "add" and len(args) > 1:
        add_task(" ".join(args[1:]))
    
    elif command == "update" and len(args) > 3:
        task_id = args[1]
        flag = args[2]
        value = args[3]
        
        if flag == "-d":
            update_task(task_id, description=value)
        elif flag == "-s":
            update_task(task_id, status=value)
        else:
            print(f"Erro: Flag inválida '{flag}'. Use '-d' para descrição ou '-s' para status.")
    
    elif command == "update":
        print("Erro: Formato incorreto para o comando 'update'.")
        print("Uso correto: python task_tracker_cli.py update <id> -d <descrição> ou python task_tracker_cli.py update <id> -s <status>")
        print("Execute 'python task_tracker_cli.py list' para ver os IDs das tarefas disponíveis.")
    
    elif command == "delete" and len(args) > 1:
        delete_task(args[1])
    
    elif command == "list":
        list_tasks()
    
    elif command == "list-todo":
        list_tasks("todo")
    
    elif command == "list-in-progress":
        list_tasks("in-progress")
    
    elif command == "list-done":
        list_tasks("done")
    
    else:
        print("Erro: Comando inválido ou argumentos insuficientes.")
        print_help()

if __name__ == '__main__':
    main(sys.argv[1:])
