# ============================================
# STUDY BOT - Google Gemini API Version
# ============================================

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Google Gemini LLM
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",  # ✅ Updated correct model name
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True
)

def simple_chat():
    """Simple chatbot function without memory"""
    print("\n" + "="*50)
    print("🤖 STUDY BOT - Google Gemini Version")
    print("="*50)
    print("Type 'quit' to exit")
    print("-"*50)
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ")
        
        # Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("🤖 Bot: Goodbye! Happy studying! 👋")
            break
        
        try:
            # Create messages for the AI
            messages = [
                SystemMessage(content="You are a helpful study assistant. Help students with their academic questions. Give clear, educational responses."),
                HumanMessage(content=user_input)
            ]
            
            # Get response from AI
            print("🤖 Bot: Thinking...")
            response = llm.invoke(messages)
            
            # Print response
            print(f"\n🤖 Bot: {response.content}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please check your API key and internet connection.")

# Run the chatbot if this file is executed directly
if __name__ == "__main__":
    simple_chat()