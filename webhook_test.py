from fastapi import APIRouter, Request, HTTPException
from app.services.code_review import analyze_code_changes
from app.services.github_client import post_comment

router = APIRouter()

@router.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    
    # Verify the webhook event
    if payload.get("action") not in ["opened", "synchronize"]:
        return {"message": "Event not relevant"}

    pr_data = payload["pull_request"]
    repo_data = payload["repository"]
    changes = pr_data.get("diff_url")

    comments = analyze_code_changes(changes)
    for comment in comments:
        post_comment(repo_data, pr_data["number"], comment)

    return {"message": "Code review is completed but I like it"}

@router.get("/")
async def hello():
    return {"message": "Welcome"}
