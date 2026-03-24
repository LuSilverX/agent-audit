import asyncio
from agents.reviewer import reviewer_agent

# FLAW #1: No error handling for division by zero
def divide_numbers(a, b):
    return a / b 

# FLAW #2: Brittle string parsing (will crash if input isn't 'user/repo')
def get_repo_name(repo_string):
    parts = repo_string.split("/")
    return parts[1]

# FLAW #3: Massive performance inefficiency (O(n) junk loop)
def process_data_inefficiently(data):
    result = []
    for i in range(len(data)):
        for j in range(1000): # Pointless nested work
            pass
        result.append(data[i])
    return result

async def main():
    print("🚀 AgentAudit: Starting Autonomous PR Review...")
    
    # User inputs for the test
    repo = input("Enter repo (e.g., LuSilverX/agent-audit): ")
    pr_num = int(input("Enter PR number: "))

    # --- THE BAIT ---
    # We call these functions with safe data locally so the script doesn't die,
    # but the AI will see the "unsafe" logic in the code itself.
    repo_name = get_repo_name(repo) 
    print(f"Targeting Repository: {repo_name}")

    # result = divide_numbers(10, 0) # <--- If you uncomment this, the script crashes!

    # --- THE ORCHESTRATION ---
    # Now we wake up the agent to review the code you pushed to GitHub.
    result = await reviewer_agent.run(
        f"Please review the changes in PR #{pr_num} for the repository '{repo}'."
    )

    # --- THE RESULTS ---
    print("\n" + "="*40)
    print("🧠 ARCHITECT REVIEW RESULTS")
    print("="*40)
    print(f"SUMMARY: {result.data.summary}")
    print(f"RISK SCORE: {result.data.risk_score}/10")
    
    print("\n✅ SUGGESTIONS:")
    for suggestion in result.data.suggestions:
        print(f"  - {suggestion}")
    
    if result.data.critical_flaws:
        print("\n🚨 CRITICAL FLAWS FOUND:")
        for flaw in result.data.critical_flaws:
            print(f"  !! {flaw}")

if __name__ == "__main__":
    asyncio.run(main())