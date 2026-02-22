# ============================================
# STUDY BOT WITH MEMORY - Google Gemini Version
# ============================================

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from database import save_chat, get_chat_history, test_connection

# Load environment variables
load_dotenv()

# Initialize Google Gemini LLM
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",  # ✅ Updated correct model name
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True
)

def chat_with_memory():
    """Chatbot with memory using MongoDB"""
    print("\n" + "="*60)
    print("🤖 STUDY BOT WITH MEMORY - Google Gemini")
    print("="*60)
    
    # Test MongoDB connection
    if test_connection():
        print("✅ MongoDB connected - I will remember our conversation!")
    else:
        print("⚠️ MongoDB not connected - I won't remember previous chats")
    
    # Get user ID
    user_id = input("\n👤 Enter your name: ")
    print(f"\nWelcome {user_id}! Type 'quit' to exit")
    print("-"*60)
    
    while True:
        # Get user input
        user_input = input("\n👤 You: ")
        
        # Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("🤖 Bot: Goodbye! Happy studying! 👋")
            break
        
        try:
            # Get previous chat history from database
            chat_history = get_chat_history(user_id)
            
            # Create context with history
            if chat_history:
                context = f"Previous conversation:\n{chat_history}\n\nCurrent question: {user_input}"
            else:
                context = user_input
            
            # Create messages
            messages = [
                SystemMessage(content="You are a helpful study assistant. Help students with their academic questions. Give clear, educational responses."),
                HumanMessage(content=context)
            ]
            
            # Get response from AI
            print("🤖 Bot: Thinking...")
            response = llm.invoke(messages)
            bot_response = response.content
            
            # Save to database
            save_chat(user_id, user_input, bot_response)
            
            # Print response
            print(f"\n🤖 Bot: {bot_response}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please check your Google API key and internet connection.")

if __name__ == "__main__":
    chat_with_memory()