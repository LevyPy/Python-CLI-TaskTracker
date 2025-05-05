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


if __name__ == '__main__':
    main(sys.argv[1:])
