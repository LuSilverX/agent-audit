import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
from agents.reviewer import reviewer_agent

async def main():
    print("🚀 AgentAudit: Starting Autonomous PR Review...")
    
    repo = input("Enter repo (e.g., User/Repo-Name): ")
    pr_num = int(input("Enter PR number: "))

    print(f"Targeting Repository: {repo}")

    # Wake up the agent
    result = await reviewer_agent.run(
        f"Please review the changes in PR #{pr_num} for the repository '{repo}'."
    )

    print("\n" + "="*40)
    print("🧠 ARCHITECT REVIEW RESULTS")
    print("="*40)
    print(f"SUMMARY: {result.output.summary}")
    print(f"RISK SCORE: {result.output.risk_score}/10")
    
    print("\n✅ SUGGESTIONS:")
    for suggestion in result.output.suggestions:
        print(f"  - {suggestion}")
    
    if result.output.critical_flaws:
        print("\n🚨 CRITICAL FLAWS FOUND:")
        for flaw in result.output.critical_flaws:
            print(f"  !! {flaw}")

if __name__ == "__main__":
    asyncio.run(main())