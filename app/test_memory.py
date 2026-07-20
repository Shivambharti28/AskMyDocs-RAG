from app.services.conversation.memory import ConversationMemory

memory = ConversationMemory()

memory.add_user_message("What is motivation?")
memory.add_assistant_message("Motivation is an internal process.")

memory.add_user_message("Explain it simply.")

print("\nConversation History\n")

for message in memory.get_history():

    print(f"{message['role'].upper()}: {message['content']}")
