# app.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from automation import run_automation  # ⬅ make sure this is correct

app = FastAPI()

# ✅ Enable CORS so frontend can communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/automate")
async def automate(request: Request):
    data = await request.json()
    url = data.get("url")
    action = data.get("action")

    try:
        result = run_automation(url, action)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "result": str(e)}
