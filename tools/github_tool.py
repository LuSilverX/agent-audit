import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

def get_pr_diff(repo_name: str, pr_number: int) -> str:
    """
    Connects to GitHub and pulls the text diff of a specific Pull Request.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "Error: GITHUB_TOKEN not found in .env file."

    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        
        # Grabbing the 'patch' data—this is exactly what changed in the PR.
        files = pr.get_files()
        diff_text = ""
        for file in files:
            diff_text += f"--- File: {file.filename} ---\n"
            diff_text += f"{file.patch}\n\n"
        
        return diff_text if diff_text else "No code changes found in this PR."

    except Exception as e:
        return f"Failed to fetch PR: {str(e)}"