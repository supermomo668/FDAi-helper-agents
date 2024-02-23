
_REQUIRED_ENV_VARS = [
  "GITHUB_TOKEN", 
  "OPENAI_API_KEY"
  # GITHUB REPO QUERY
  "GITHUB_OWNER",
  "GITHUB_REPO",
  "GITHUB_BRANCH"
]

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/contents/"
