from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import call_openai
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI()
# Load templates from the "templates" directory
templates = Jinja2Templates(directory="templates")

# Define the root endpoint that serves the HTML page

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class EmailContent(BaseModel):
    email: str

class RewriteRequest(BaseModel):
    email: str
    tone: str


@app.post("/classify_email")
def classify_email(data: EmailContent):
    try:
        with open("prompts/emailclassifier_prompt.txt") as f:
            system_prompt = f.read()
        user_prompt = f"Email:\n{data.email}\n\nCategory:"
        category = call_openai(system_prompt, user_prompt)
        return {"category": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rewrite_email")
def rewrite_email(data: RewriteRequest):
    try:
        with open("prompts/emailrewriter_prompt.txt") as f:
            system_prompt = f.read()
        user_prompt = f"Input Email:\n{data.email}\n\nDesired Tone: {data.tone}\n\nRewritten Email:"
        rewritten = call_openai(system_prompt, user_prompt)
        return {"rewritten_email": rewritten}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
