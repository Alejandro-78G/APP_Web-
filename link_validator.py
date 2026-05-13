import asyncio
import json
import os
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from config import get_settings

console = Console()
settings = get_settings()

async def check_url(client: httpx.AsyncClient, url: str, headers: dict = None) -> tuple[bool, int]:
    """Check if a URL returns a 200 OK status."""
    try:
        response = await client.head(url, headers=headers, timeout=10.0, follow_redirects=True)
        # Some APIs don't like HEAD, fallback to GET if needed
        if response.status_code == 405:
            response = await client.get(url, headers=headers, timeout=10.0, follow_redirects=True)
        return response.status_code == 200, response.status_code
    except httpx.RequestError:
        return False, 0

async def validate_links(silent=False) -> dict:
    """Validates all links in proyectos.json."""
    file_path = os.path.join(os.path.dirname(__file__), 'proyectos.json')
    if not os.path.exists(file_path):
        if not silent:
            console.print(f"[red]Error: {file_path} no existe.[/red]")
        return {"status": "error", "message": "proyectos.json not found"}

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    projects = data.get('projects', [])
    
    if not silent:
        console.print(Panel.fit("[bold cyan]Portfolio Link Validator[/bold cyan]\nIniciando validación...", border_style="cyan"))

    results = []
    github_headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Portfolio-Validator"}
    if settings.GITHUB_TOKEN:
        github_headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        for p in projects:
            slug = p.get('id', 'Unknown')
            
            # Validate GitHub Repo
            github_repo = p.get('github_repo')
            if github_repo:
                url = f"{settings.GITHUB_API_BASE}/repos/{github_repo}"
                is_valid, status = await check_url(client, url, headers=github_headers)
                results.append({"project": slug, "type": "GitHub", "target": github_repo, "valid": is_valid, "status": status})
            
            # Validate Power BI
            pbi_url = p.get('powerbi_embed_url')
            if pbi_url:
                is_valid, status = await check_url(client, pbi_url)
                results.append({"project": slug, "type": "Power BI", "target": "URL", "valid": is_valid, "status": status})
            else:
                results.append({"project": slug, "type": "Power BI", "target": "N/A", "valid": True, "status": "SKIPPED"})

            # Validate Thumbnail
            thumbnail = p.get('thumbnail')
            if thumbnail:
                # Assuming path starts with /static
                local_path = os.path.join(os.path.dirname(__file__), thumbnail.lstrip('/'))
                is_valid = os.path.exists(local_path)
                results.append({"project": slug, "type": "Thumbnail", "target": thumbnail, "valid": is_valid, "status": "EXISTS" if is_valid else "MISSING"})

    if not silent:
        # Print results in a rich table
        table = Table(title="Validation Results")
        table.add_column("Project", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Target", style="blue")
        table.add_column("Valid", justify="center")
        table.add_column("Status", justify="center")

        passed = 0
        failed = 0
        skipped = 0

        for r in results:
            if r['status'] == 'SKIPPED':
                valid_str = "[yellow][SKIP][/yellow]"
                status_str = "[yellow]SKIPPED[/yellow]"
                skipped += 1
            elif r['valid']:
                valid_str = "[green][PASS][/green]"
                status_str = f"[green]{r['status']}[/green]"
                passed += 1
            else:
                valid_str = "[red][FAIL][/red]"
                status_str = f"[red]{r['status']}[/red]"
                failed += 1
            
            table.add_row(r['project'], r['type'], r['target'], valid_str, str(status_str))

        console.print(table)
        console.print(f"[bold]Total: {passed} passed, [red]{failed} failed[/red], [yellow]{skipped} skipped[/yellow][/bold]")

    return {
        "status": "success",
        "results": results
    }

if __name__ == "__main__":
    asyncio.run(validate_links())
