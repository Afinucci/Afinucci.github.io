"""
Inventory Management AI Agent

This agent handles all inventory-related queries and actions.
"""
from typing import List, Dict, Any
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

from ai_engine.tools.inventory_tools import (
    get_stock_levels,
    update_stock,
    get_low_stock_items,
    search_products,
)


class InventoryAgent:
    """
    AI Agent for inventory management
    """

    def __init__(self, api_key: str):
        """
        Initialize the inventory agent

        Args:
            api_key: OpenAI API key
        """
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            api_key=api_key,
            temperature=0.7,
        )

        self.tools = self._setup_tools()
        self.agent = self._create_agent()

    def _setup_tools(self) -> List[Tool]:
        """
        Set up tools available to the agent
        """
        return [
            Tool(
                name="get_stock_levels",
                func=get_stock_levels,
                description="Get current stock levels for a product by SKU or product ID. "
                "Use this when user asks about inventory levels.",
            ),
            Tool(
                name="update_stock",
                func=update_stock,
                description="Update stock levels for a product. "
                "Use this when user wants to add or remove stock.",
            ),
            Tool(
                name="get_low_stock_items",
                func=get_low_stock_items,
                description="Get a list of products with low stock. "
                "Use this when user asks about items that need reordering.",
            ),
            Tool(
                name="search_products",
                func=search_products,
                description="Search for products by name, SKU, or category. "
                "Use this for general product queries.",
            ),
        ]

    def _create_agent(self) -> AgentExecutor:
        """
        Create the agent executor
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an AI assistant for an inventory management system.
You help users manage their inventory through natural conversation.

Key capabilities:
- Check stock levels
- Update inventory quantities
- Identify low stock items
- Search for products
- Provide insights and recommendations

Be conversational, helpful, and proactive. If you notice issues (like low stock),
mention them to the user. Always confirm actions before executing them.

When presenting data, use clear formatting and highlight important information.
""",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt,
        )

        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=3,
            early_stopping_method="generate",
        )

    async def process_message(
        self, message: str, chat_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process a user message and return the agent's response

        Args:
            message: User's input message
            chat_history: Previous conversation history

        Returns:
            Dictionary containing the response and metadata
        """
        if chat_history is None:
            chat_history = []

        try:
            response = await self.agent.ainvoke(
                {
                    "input": message,
                    "chat_history": chat_history,
                }
            )

            return {
                "success": True,
                "message": response["output"],
                "intermediate_steps": response.get("intermediate_steps", []),
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"I encountered an error: {str(e)}",
                "error": str(e),
            }
