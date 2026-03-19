from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

# Defining structured output
class PRReviewResult(BaseModel):
    summary: str
    risk_score: int  # 1-10
    suggestions: list[str]
    critical_flaws: list[str]

# Initialize the Agent
reviewer_agent = Agent(
    'openai:gpt-4o', # or 'google:gemini-2.0-flash'
    result_type=PRReviewResult,
    system_prompt=(
        "You are an expert Senior Software Architect. Your task is to review Pull Requests. "
        "Don't just look for typos—look for logic gaps, security holes, and performance issues. "
        "Always provide a risk score from 1 (safe) to 10 (critical)."
    )
)

# The Tool (The "Hands")
@reviewer_agent.tool
async def fetch_code_changes(ctx: RunContext[None], repo: str, pr_id: int) -> str:
    """Fetch the code diff for a specific GitHub Pull Request."""
    return f"Fetching diff for PR #{pr_id} in {repo}..."