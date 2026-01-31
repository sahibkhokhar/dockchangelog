"""
Command-line interface for dockchangelog.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from . import __version__
from .checker import DockerChecker
from .config import Config, create_example_config, load_config
from .formatter import OutputFormatter
from .github_client import GitHubClient
from .mapper import ImageMapper

app = typer.Typer(
    name="dockchangelog",
    help="check docker updates with github release notes",
    add_completion=False,
)

console = Console()


@app.command()
def check(
    compose_dir: Optional[Path] = typer.Option(
        None,
        "--compose-dir",
        "-d",
        help="directory containing compose files (default: current directory)",
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        help="path to config file",
    ),
    service: Optional[str] = typer.Option(
        None,
        "--service",
        "-s",
        help="check specific service only",
    ),
    no_cache: bool = typer.Option(
        False,
        "--no-cache",
        help="disable cache for GitHub API responses",
    ),
    no_interactive: bool = typer.Option(
        False,
        "--no-interactive",
        help="show all results at once (no pausing between services)",
    ),
):
    """
    check for docker image updates and show release notes
    
    This is the main command - it's safe and read-only.
    By default, pauses after each service with updates.
    """
    # Load configuration
    config = load_config(config_file)
    
    # Use interactive mode if stdout is a terminal and not disabled
    interactive = not no_interactive and console.is_terminal
    
    # Initialize components
    checker = DockerChecker(compose_dir)
    github = GitHubClient(
        token=config.github_token,
        cache_dir=None if no_cache else config.cache.path,
    )
    mapper = ImageMapper(config)
    formatter = OutputFormatter(console)
    
    # Show header
    formatter.show_header()
    
    # Find and parse compose files
    services = checker.get_all_services()
    
    if not services:
        formatter.show_no_services_found()
        raise typer.Exit(0)
    
    # Filter to specific service if requested
    if service:
        services = [s for s in services if s.name == service]
        if not services:
            formatter.show_error(f"service '{service}' not found")
            raise typer.Exit(1)
    
    # Check each service
    services_with_updates = 0
    services_checked = 0
    
    for svc in services:
        # Map to GitHub repo
        repo = mapper.map(svc)
        
        if not repo:
            console.print(f"[dim]• {svc.name}: no github mapping found[/dim]")
            continue
        
        # Get latest release
        release = github.get_latest_release(repo)
        
        if not release:
            console.print(f"[dim]• {svc.name}: no releases found for {repo}[/dim]")
            continue
        
        # Check if update available (simple tag comparison)
        current_tag = svc.image.tag
        has_update = current_tag != release.tag
        
        # Show results
        formatter.show_service_update(svc.name, current_tag, release, has_update)
        
        if has_update:
            services_with_updates += 1
            services_checked += 1
            
            # In interactive mode, pause after showing each service with updates
            if interactive and services_checked < len([s for s in services if mapper.map(s)]):
                console.print()
                console.print("[dim]Press Enter to continue to next service (or Ctrl+C to stop)...[/dim]", end="")
                try:
                    input()
                except (KeyboardInterrupt, EOFError):
                    console.print("\n")
                    break
                console.print()  # Add spacing after continue
    
    # Show summary
    formatter.show_summary(len(services), services_with_updates)
    
    # Exit code: 0 if up to date, 1 if updates available
    raise typer.Exit(0 if services_with_updates == 0 else 1)


@app.command()
def init(
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="output path for config file (default: ./config.yml)",
    ),
):
    """
    create example configuration file
    """
    output_path = output or Path("config.yml")
    
    if output_path.exists():
        overwrite = typer.confirm(f"{output_path} already exists. overwrite?")
        if not overwrite:
            console.print("cancelled")
            raise typer.Exit(0)
    
    # Create config
    config_content = create_example_config()
    output_path.write_text(config_content)
    
    console.print(f"[green]✓[/green] created config file: {output_path}")
    console.print()
    console.print("edit this file to add image mappings and settings")


@app.command()
def version():
    """
    show version information
    """
    console.print(f"dockchangelog version {__version__}")


def main():
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
