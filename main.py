# ============================================
# STUDY BOT API - Google Gemini Version
# Complete API with all endpoints
# ============================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from database import save_chat, get_chat_history, test_connection

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Study Bot API",
    description="AI Study Assistant with Memory using Google Gemini",
    version="1.0.0",
    docs_url="/docs",        # Swagger UI
    redoc_url="/redoc",      # ReDoc documentation
    openapi_url="/openapi.json"  # OpenAPI schema
)

# Request/Response models
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    user_id: str
    user_message: str
    bot_response: str
    status: str

class HistoryRequest(BaseModel):
    user_id: str
    limit: Optional[int] = 5

class HistoryResponse(BaseModel):
    user_id: str
    history: str
    status: str

# ============================================
# ROOT ENDPOINT - http://localhost:8000
# ============================================
@app.get("/")
async def root():
    """Welcome message and API information"""
    return {
        "message": "Welcome to Study Bot API",
        "version": "1.0.0 (Gemini)",
        "author": "Study Bot Project",
        "endpoints": {
            "/": "GET - This welcome message",
            "/health": "GET - Check API and database status",
            "/docs": "GET - Interactive Swagger UI documentation",
            "/redoc": "GET - Alternative ReDoc documentation",
            "/openapi.json": "GET - OpenAPI JSON schema",
            "/chat": "POST - Send message to chatbot",
            "/history": "POST - Get chat history for a user"
        },
        "how_to_use": {
            "chat": "Send POST request to /chat with {'user_id': 'name', 'message': 'question'}",
            "history": "Send POST request to /history with {'user_id': 'name', 'limit': 5}"
        }
    }

# ============================================
# HEALTH ENDPOINT - http://localhost:8000/health
# ============================================
@app.get("/health")
async def health_check():
    """Check if API and database are working"""
    db_status = test_connection()
    
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    api_status = "available" if api_key else "missing"
    
    return {
        "api_status": "healthy",
        "database": "connected" if db_status else "disconnected",
        "api_key": api_status,
        "model": "models/gemini-2.5-flash",
        "timestamp": str(__import__('datetime').datetime.now()),
        "server": "running"
    }

# ============================================
# CHAT ENDPOINT - http://localhost:8000/chat (POST)
# ============================================
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send message to chatbot
    
    Example request:
    {
        "user_id": "izza",
        "message": "What is photosynthesis?"
    }
    """
    try:
        # Initialize Google Gemini LLM
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise HTTPException(status_code=500, detail="Google API key not found")
            
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Get chat history from database
        chat_history = get_chat_history(request.user_id)
        
        # Create prompt with history context
        if chat_history:
            context = f"Previous conversation:\n{chat_history}\n\nCurrent question: {request.message}"
        else:
            context = request.message
        
        messages = [
            SystemMessage(content="You are a helpful study assistant. Help students with their academic questions. Give clear, educational responses."),
            HumanMessage(content=context)
        ]
        
        # Get response from Gemini
        response = llm.invoke(messages)
        bot_response = response.content
        
        # Save chat to database
        save_chat(request.user_id, request.message, bot_response)
        
        return ChatResponse(
            user_id=request.user_id,
            user_message=request.message,
            bot_response=bot_response,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# HISTORY ENDPOINT - http://localhost:8000/history (POST)
# ============================================
@app.post("/history", response_model=HistoryResponse)
async def get_history(request: HistoryRequest):
    """Get chat history for a user
    
    Example request:
    {
        "user_id": "izza",
        "limit": 5
    }
    """
    try:
        history = get_chat_history(request.user_id, request.limit)
        return HistoryResponse(
            user_id=request.user_id,
            history=history if history else "No chat history found",
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ADDITIONAL USEFUL ENDPOINTS
# ============================================

@app.get("/info")
async def info():
    """Get detailed API information"""
    return {
        "name": "Study Bot API",
        "version": "1.0.0",
        "description": "AI Study Assistant with Memory using Google Gemini",
        "framework": "FastAPI",
        "model": "gemini-2.5-flash",
        "database": "MongoDB",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        }
    }

@app.get("/models")
async def models():
    """Get available AI models"""
    return {
        "current_model": "gemini-2.5-flash",
        "available_models": [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash",
            "gemini-1.5-flash"
        ],
        "note": "Current model is set in the code"
    }

@app.get("/test")
async def test():
    """Simple test endpoint to check if API is working"""
    return {"message": "API is working!", "status": "ok"}

# ============================================
# RUN THE SERVER
# ============================================
if __name__ == "__main__":
    print("="*60)
    print("🚀 STARTING STUDY BOT API SERVER")
    print("="*60)
    print("\n📌 Available endpoints:")
    print("   ✅ http://localhost:8000/         - Welcome message")
    print("   ✅ http://localhost:8000/health    - Health check")
    print("   ✅ http://localhost:8000/info      - API information")
    print("   ✅ http://localhost:8000/models    - Available models")
    print("   ✅ http://localhost:8000/test      - Test endpoint")
    print("   ✅ http://localhost:8000/docs      - Swagger UI")
    print("   ✅ http://localhost:8000/redoc     - ReDoc")
    print("   ✅ http://localhost:8000/chat      - POST - Send message")
    print("   ✅ http://localhost:8000/history   - POST - Get history")
    print("="*60)
    print("\n⚡ Server starting...")
    
    # Run server on localhost
    uvicorn.run(app, host="127.0.0.1", port=8000)