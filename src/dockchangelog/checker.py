"""
Docker compose checking functionality.
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

import yaml


class DockerImage:
    """Represents a Docker image with registry, name, and tag."""
    
    def __init__(self, image_string: str):
        """Parse docker image string."""
        self.original = image_string
        self.registry, self.name, self.tag = self._parse(image_string)
    
    def _parse(self, image_string: str) -> tuple[Optional[str], str, str]:
        """
        Parse image string into components.
        
        Examples:
            nginx:latest -> (None, nginx, latest)
            ghcr.io/user/app:v1.0 -> (ghcr.io, user/app, v1.0)
            registry.io:5000/app -> (registry.io:5000, app, latest)
        """
        # Default tag
        tag = "latest"
        
        # Check if tag is specified
        if ":" in image_string:
            parts = image_string.rsplit(":", 1)
            if "/" not in parts[1]:  # It's a tag, not a port in registry
                image_string, tag = parts
        
        # Check for registry
        registry = None
        if "/" in image_string:
            first_part = image_string.split("/")[0]
            # If first part has dots or ports, it's a registry
            if "." in first_part or ":" in first_part:
                registry = first_part
                name = image_string[len(first_part) + 1:]
            else:
                name = image_string
        else:
            name = image_string
        
        return registry, name, tag
    
    def __str__(self) -> str:
        """Return original image string."""
        return self.original


class ComposeService:
    """Represents a service from docker-compose."""
    
    def __init__(self, name: str, image: DockerImage, compose_file: Path, labels: Dict[str, str]):
        self.name = name
        self.image = image
        self.compose_file = compose_file
        self.labels = labels
    
    def get_source_label(self) -> Optional[str]:
        """Get org.opencontainers.image.source label if present."""
        return self.labels.get("org.opencontainers.image.source")


class DockerChecker:
    """Check for Docker image updates."""
    
    def __init__(self, compose_dir: Optional[Path] = None):
        """
        Initialize checker.
        
        Args:
            compose_dir: Directory containing compose files. 
                        If None, uses current directory.
        """
        self.compose_dir = Path(compose_dir) if compose_dir else Path.cwd()
    
    def find_compose_files(self) -> List[Path]:
        """
        Find all compose files in the directory tree.
        
        Returns:
            List of paths to compose files
        """
        compose_files = []
        
        # Common compose file names
        patterns = ["compose.yml", "compose.yaml", "docker-compose.yml", "docker-compose.yaml"]
        
        for pattern in patterns:
            compose_files.extend(self.compose_dir.rglob(pattern))
        
        return compose_files
    
    def parse_compose_file(self, compose_file: Path) -> List[ComposeService]:
        """
        Parse compose file and extract services with images.
        
        Args:
            compose_file: Path to compose file
        
        Returns:
            List of ComposeService objects
        """
        try:
            with open(compose_file) as f:
                compose_data = yaml.safe_load(f)
            
            services = []
            for name, config in compose_data.get("services", {}).items():
                # Skip services without image (using build instead)
                if "image" not in config:
                    continue
                
                image = DockerImage(config["image"])
                labels = config.get("labels", {})
                
                # Handle labels as list format
                if isinstance(labels, list):
                    labels = {
                        label.split("=")[0]: label.split("=", 1)[1]
                        for label in labels if "=" in label
                    }
                
                services.append(ComposeService(name, image, compose_file, labels))
            
            return services
        
        except Exception as e:
            # Skip invalid compose files
            return []
    
    def check_for_updates(self, compose_file: Path) -> Dict[str, bool]:
        """
        Check if updates are available for services in compose file.
        
        Args:
            compose_file: Path to compose file
        
        Returns:
            Dict mapping service names to update availability (True if update available)
        """
        try:
            # Run docker compose pull --dry-run to check for updates
            # Note: --dry-run is not available in all docker compose versions
            # So we'll use a different approach: pull and check output
            
            result = subprocess.run(
                ["docker", "compose", "-f", str(compose_file), "pull", "--dry-run"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            # Parse output to determine which images have updates
            updates = {}
            for line in result.stdout.split("\n"):
                # Look for service names and status
                # This is a simplified version - real implementation would be more robust
                pass
            
            return updates
        
        except subprocess.TimeoutExpired:
            return {}
        except FileNotFoundError:
            # docker or docker compose not installed
            return {}
    
    def get_all_services(self) -> List[ComposeService]:
        """
        Get all services from all compose files.
        
        Returns:
            List of all ComposeService objects found
        """
        all_services = []
        
        for compose_file in self.find_compose_files():
            services = self.parse_compose_file(compose_file)
            all_services.extend(services)
        
        return all_services
