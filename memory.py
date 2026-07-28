from collections import defaultdict

conversation_memory = defaultdict(list)


def add_message(chat_id, role, text):
    conversation_memory[chat_id].append({
        "role": role,
        "content": text
    })


def get_history(chat_id):
    return conversation_memory[chat_id]


def clear(chat_id):
    conversation_memory.pop(chat_id, None)