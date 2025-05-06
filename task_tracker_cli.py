import datetime
import json
import os
import sys


def main(args):

    if not args or args[0] in ["-h", "--help", "help"]:
        # print_help() adicionar
        print('Help')
        return

    command = args[0]

    if command == "add" and len(args) > 1:
        add_task(" ".join(args[1:]))

    elif command == "list":
        list_tasks()

def load_tasks():
    """Load tasks from the JSON file or create a new file if it doesn't exist"""
    if not os.path.exists("tasks.json"):
        return []

    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            content = file.read()
            if not content.strip():
                return []
            data = json.loads(content)
            # Verifica se o arquivo contém uma lista ou um único dicionário
            if isinstance(data, dict):
                # Se for um dicionário, converte para uma lista com um item
                return [data] if "id" in data else []

            # Converter IDs numéricos em strings para inteiros
            for task in data:
                if isinstance(task["id"], str) and task["id"].isdigit():
                    task["id"] = int(task["id"])

            return data
    except json.JSONDecodeError:
        print("Erro: O arquivo tasks.json está corrompido. Criando um novo arquivo.")
        return []


def save_tasks(tasks):
    """Save tasks to the JSON file"""
    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)


def get_next_id(tasks):
    """Get the next available sequential ID"""
    # Se não houver tarefas, começar com ID 1
    if not tasks:
        return 1

    # Tentar encontrar o maior ID numérico
    max_id = 0
    for task in tasks:
        task_id = task["id"]
        # Verificar se o ID é numérico
        if isinstance(task_id, int) or (isinstance(task_id, str) and task_id.isdigit()):
            current_id = int(task_id)
            if current_id > max_id:
                max_id = current_id

    # Retornar o próximo ID na sequência
    return max_id + 1


def add_task(description):
    """Add a new task"""
    tasks = load_tasks()

    # Gerar ID sequencial
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
    print(f"Tarefa adicionada: {description} -> (ID: {next_id})")

def list_tasks(status_filter=None):
    """List tasks with optional status filter"""
    tasks = load_tasks()

    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return

    # Garantir que não há tarefas duplicadas na listagem
    unique_tasks = []
    seen_ids = set()

    for task in tasks:
        # Normalizar o ID para comparação
        task_id = task["id"]
        if isinstance(task_id, str) and task_id.isdigit():
            task_id = int(task_id)

        # Pular tarefas com IDs já vistos
        if task_id in seen_ids:
            continue

        seen_ids.add(task_id)
        unique_tasks.append(task)

    # Aplicar filtro de status, se fornecido
    filtered_tasks = unique_tasks
    if status_filter:
        filtered_tasks = [task for task in unique_tasks if task["status"] == status_filter]

    if not filtered_tasks:
        print(f"Nenhuma tarefa com status '{status_filter}' encontrada.")
        return

    print(f"\n{'ID':<5} | {'Descrição':<30} | {'Status':<12} | {'Criado em':<25} | {'Atualizado em':<25}")
    print("-" * 110)

    # Ordenar tarefas por ID para exibição
    filtered_tasks.sort(key=lambda x: x["id"] if isinstance(x["id"], int) else int(x["id"]) if isinstance(x["id"], str) and x["id"].isdigit() else float('inf'))

    for task in filtered_tasks:
        # Formatar o ID para exibição
        task_id = task["id"]
        if isinstance(task_id, str) and not task_id.isdigit():
            # Se for um UUID ou outro formato não numérico, exibir como está
            display_id = task_id
        else:
            # Se for numérico, exibir como número
            display_id = str(task_id)

        # Verificar se os campos de data existem e obter seus valores
        created_at = "N/A"
        if "createdAt" in task:
            created_at = task["createdAt"].split("T")[0] if "T" in task["createdAt"] else task["createdAt"]
        elif "createdAt1" in task:  # Lidar com campo inconsistente no arquivo JSON
            created_at = task["createdAt1"].split("T")[0] if "T" in task["createdAt1"] else task["createdAt1"]

        updated_at = "N/A"
        if "updatedAt" in task:
            updated_at = task["updatedAt"].split("T")[0] if "T" in task["updatedAt"] else task["updatedAt"]

        # Verificar se a descrição é uma lista ou uma string
        description = task["description"]
        if isinstance(description, list):
            description = ", ".join(description)

        print(f"{display_id:<5} | {description[:30]:<30} | {task['status']:<12} | {created_at:<25} | {updated_at:<25}")

if __name__ == '__main__':
    main(sys.argv[1:])
