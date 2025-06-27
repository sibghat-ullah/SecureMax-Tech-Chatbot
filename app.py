from fastapi import FastAPI, Request
from views.chatbot import chat

app = FastAPI()

# Route to handle the chatbot interaction
@app.get("/", response_class="HTMLResponse")
async def root(request: Request):
    return await chat(request)
