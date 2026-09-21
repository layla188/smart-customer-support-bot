import traceback

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from src.llm import create_llm
from src.memory import ConversationMemory
from src.tools import TOOLS


SYSTEM_PROMPT = """
You are LumaAssist, the customer-support assistant for LumaCart.

LumaCart is a fictional e-commerce company based in Cairo, Egypt.

Your job is to help customers with:

- Products
- Shipping
- Returns
- Payments
- Order support
- Order calculations
- Currency conversion

Follow these rules carefully:

1. Use the search_knowledge_base tool for questions about
   LumaCart products, shipping, returns, payments, support,
   company policies, and other knowledge-base information.

2. Use calculate_order_total when the user asks you to
   calculate an order total, discount, or shipping cost.

3. Use get_exchange_rate when the user asks for a live
   currency conversion or exchange rate.

4. Do not invent company policies, product information,
   order details, prices, delivery dates, refunds, or
   replacement decisions.

5. If required information is missing, ask the user for it.

6. For order-related questions, never invent an order status
   or order information.

7. If the knowledge base does not contain the required
   information, clearly say that additional assistance
   is required.

8. Use previous conversation context when answering
   follow-up questions.

9. Be polite, professional, and concise.

10. After using a tool, explain the result clearly to the user.
"""


class LumaAssistAgent:

    def __init__(self):
        self.llm = create_llm()
        self.llm_with_tools = self.llm.bind_tools(TOOLS)

        self.memory = ConversationMemory()

        self.tool_map = {
            tool.__name__: tool
            for tool in TOOLS
        }

        # Safety limit to prevent infinite tool-calling loops
        self.max_iterations = 5

    def build_messages(self, user_input: str):
        """
        Build the messages sent to the LLM.

        Includes:
        - System instructions
        - Previous conversation
        - Current user message
        """

        messages = [
            SystemMessage(
                content=SYSTEM_PROMPT
            )
        ]

        # Add previous conversation history
        for message in self.memory.get_history():

            if message["role"] == "user":
                messages.append(
                    HumanMessage(
                        content=message["content"]
                    )
                )

            elif message["role"] == "assistant":
                messages.append(
                    AIMessage(
                        content=message["content"]
                    )
                )

        # Add the current user message
        messages.append(
            HumanMessage(
                content=user_input
            )
        )

        return messages

    def execute_tool(
        self,
        tool_name: str,
        tool_args: dict,
    ) -> str:

        tool = self.tool_map.get(tool_name)

        # Unknown tool
        if tool is None:
            return (
                f"Error: unknown tool '{tool_name}'."
            )

        try:
            # Execute the Python function
            result = tool(**tool_args)

            return str(result)

        except Exception as e:
            print("\n========== TOOL ERROR ==========")
            traceback.print_exc()
            print("================================\n")

            return (
                f"Tool '{tool_name}' failed:\n"
                f"{type(e).__name__}: {str(e)}"
            )

    def chat(self, user_input: str) -> str:
        """
        Process one user message.

        The agent can:
        1. Send the question to the LLM
        2. Detect tool calls
        3. Execute requested tools
        4. Send tool results back to the LLM
        5. Return the final answer
        """

        # Remove unnecessary spaces
        user_input = user_input.strip()

        if not user_input:
            return "Please enter a question."

        # Build initial conversation
        messages = self.build_messages(
            user_input
        )

        # ====================================================
        # Tool Calling Loop
        # ====================================================

        for iteration in range(
            self.max_iterations
        ):

            try:
                # Ask the LLM what to do
                response = self.llm_with_tools.invoke(
                    messages
                )

            except Exception as e:
                print("\n========== LLM ERROR ==========")
                traceback.print_exc()
                print("================================\n")

                return (
                    "LumaAssist encountered an error:\n\n"
                    f"`{type(e).__name__}: {str(e)}`"
                )

            # Add LLM response to the current request
            messages.append(response)

            # =================================================
            # No Tool Call
            # =================================================

            if not response.tool_calls:

                answer = response.content

                # Make sure answer is a string
                if not isinstance(answer, str):
                    answer = str(answer)

                # Save conversation to memory
                self.memory.add_user_message(
                    user_input
                )

                self.memory.add_assistant_message(
                    answer
                )

                return answer

            # =================================================
            # Tool Calls
            # =================================================

            for tool_call in response.tool_calls:

                tool_name = tool_call["name"]

                tool_args = tool_call.get(
                    "args",
                    {}
                )

                tool_call_id = tool_call["id"]

                # Execute requested tool
                tool_result = self.execute_tool(
                    tool_name=tool_name,
                    tool_args=tool_args,
                )

                # Add tool result back to the LLM conversation
                messages.append(
                    ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call_id,
                    )
                )

        # ====================================================
        # Maximum Iterations Reached
        # ====================================================

        return (
            "I couldn't complete the request safely "
            "because too many tool calls were attempted. "
            "Please try asking the question again."
        )


# ============================================================
# Quick Test
# ============================================================

def main():

    print("\n======================================")
    print("       LumaAssist Customer Support")
    print("======================================")

    print("\nType 'exit' to stop.\n")

    # Create agent
    agent = LumaAssistAgent()

    # Continuous conversation
    while True:

        user_input = input(
            "You: "
        ).strip()

        # Exit commands
        if user_input.lower() in {
            "exit",
            "quit",
        }:

            print("\nGoodbye!")
            break

        # Get assistant response
        answer = agent.chat(
            user_input
        )

        print(
            f"\nLumaAssist: {answer}\n"
        )


if __name__ == "__main__":
    main()