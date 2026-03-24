from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from tools.github_tool import get_pr_diff 

# The Structured Output
class PRReviewResult(BaseModel):
    summary: str
    risk_score: int
    suggestions: list[str]
    critical_flaws: list[str]

# The Agent (Clean constructor for v0.8+)
reviewer_agent = Agent(
    'openai:gpt-4o', 
    output_type=PRReviewResult,
)

# System Prompt (The Decorator Pattern)
@reviewer_agent.system_prompt
def add_system_prompt() -> str:
    return (
        "You are an expert Senior Software Architect. Your task is to review Pull Requests. "
        "Look for logic gaps, security holes, and performance issues. "
        "Always provide a risk score from 1 (safe) to 10 (critical)."
    )

# The Tool (The "Hands")
@reviewer_agent.tool
async def fetch_code_changes(ctx: RunContext[None], repo: str, pr_id: int) -> str:
    """Fetch the code diff for a specific GitHub Pull Request."""
    return get_pr_diff(repo, pr_id)