from typing import List, Dict


class ConversationMemory:

    def __init__(self):
        self._messages: List[Dict[str, str]] = []

    def add_user_message(self, message: str) -> None:
        self._messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str) -> None:
        self._messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def get_history(self) -> List[Dict[str, str]]:
        return self._messages.copy()

    def clear(self) -> None:
        self._messages.clear()

    def __len__(self):
        return len(self._messages)