import httpx
import logging
from config import get_settings

logger = logging.getLogger(__name__)

class GitHubClient:
    """Async client for GitHub REST API v3 to fetch repository metrics."""

    def __init__(self):
        self.settings = get_settings()
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Portfolio-App"
        }
        if self.settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {self.settings.GITHUB_TOKEN}"
        else:
            logger.warning("GITHUB_TOKEN is missing or empty. API rate limits will be restricted and private repos inaccessible.")

        self._cache = {}

    async def get_repo_metrics(self, repo: str) -> dict:
        """
        Fetch repository metrics: stars, main language.
        repo format: "owner/repo" (e.g. "Alejandro-78G/excel-cleaner")
        """
        # Basic in-memory caching implementation
        if repo in self._cache:
            return self._cache[repo]

        url = f"{self.settings.GITHUB_API_BASE}/repos/{repo}"
        
        default_metrics = {
            "stars": 0,
            "language": "Desconocido",
            "error": False
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=5.0)
                
                if response.status_code == 200:
                    data = response.json()
                    metrics = {
                        "stars": data.get("stargazers_count", 0),
                        "language": data.get("language") or "Desconocido",
                        "error": False
                    }
                    self._cache[repo] = metrics
                    return metrics
                elif response.status_code == 404:
                    logger.error(f"Repository not found: {repo}")
                    default_metrics["error"] = "Repository not found"
                    return default_metrics
                elif response.status_code == 401:
                    logger.error("GitHub API unauthorized. Check GITHUB_TOKEN.")
                    default_metrics["error"] = "Unauthorized"
                    return default_metrics
                else:
                    logger.error(f"GitHub API Error for {repo}: Status {response.status_code}")
                    default_metrics["error"] = f"HTTP {response.status_code}"
                    return default_metrics

        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc.request.url!r}.")
            default_metrics["error"] = "Request failed"
            return default_metrics
