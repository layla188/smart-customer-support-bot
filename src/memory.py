from typing import List, Dict


class ConversationMemory:
    """
    Short-term conversation memory.

    Stores the conversation history so the assistant
    can remember previous turns during the current session.
    """

    def __init__(self):

        self.messages: List[Dict[str, str]] = []


    def add_message(
        self,
        role: str,
        content: str,
    ):

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )


    def add_user_message(self, content: str):

        self.add_message(
            role="user",
            content=content,
        )

    def add_assistant_message(self, content: str):

        self.add_message(
            role="assistant",
            content=content,
        )


    def get_history(self) -> List[Dict[str, str]]:

        return self.messages


    def clear(self):

        self.messages = []


    def __len__(self):

        return len(self.messages)

