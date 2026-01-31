# quick start guide

get up and running with dockchangelog in 5 minutes.

## installation

```bash
# using uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install dockchangelog

# using pipx
pipx install dockchangelog

# using pip
pip install dockchangelog

# from source
git clone https://github.com/yourusername/dockchangelog
cd dockchangelog
uv pip install -e .
```

## first run

go to a directory with docker compose files and run:

```bash
dockchangelog check
```

that's it! you'll see:
- which services have updates available
- what versions are available
- what changed in each release

## example

```bash
cd ~/docker/services
dockchangelog check
```

output:
```
dockchangelog - checking for updates...

✓ postgres: up to date

⚠  traefik: update available
   Current: v2.10.7
   Latest:  v3.0.0
   Published: 2024-04-29

   ✨ Features:
      • kubernetes gateway api provider
      • new plugin architecture

   🐛 Fixes:
      • fixed tls certificate reload

   https://github.com/traefik/traefik/releases/tag/v3.0.0

────────────────────────────────────────────────────────────
Found 1 update available
```

## configuration (optional)

create a config file for custom image mappings:

```bash
dockchangelog init
```

edit `config.yml`:

```yaml
image_mappings:
  myregistry.io/myapp:latest: username/myapp
```

## github token (optional but recommended)

without token: 60 API requests per hour  
with token: 5000 API requests per hour

```bash
# create token at: https://github.com/settings/tokens
# needs only public repo read access

export GITHUB_TOKEN=your_token_here
dockchangelog check
```

or add to `~/.bashrc`:

```bash
echo 'export GITHUB_TOKEN=your_token_here' >> ~/.bashrc
```

## common use cases

### check all services

```bash
dockchangelog check
```

### check specific service

```bash
dockchangelog check --service vaultwarden
```

### check different directory

```bash
dockchangelog check --compose-dir /path/to/services
```

### use in scripts

```bash
if ! dockchangelog check; then
    echo "updates available!"
    # send notification, etc
fi
```

### disable cache

```bash
dockchangelog check --no-cache
```

## troubleshooting

**no services found**
- make sure you have `compose.yml` or `docker-compose.yml` files
- try `--compose-dir` to specify location

**no github mapping found**
- add mapping to `config.yml`
- check if image uses github (some don't)

**rate limit exceeded**
- add github token (see above)
- or wait 1 hour for reset

## next steps

- add custom image mappings in `config.yml`
- set up github token for higher rate limits
- integrate into your update workflow
- run regularly to stay informed

## getting help

```bash
dockchangelog --help
dockchangelog check --help
```

or open an issue: https://github.com/yourusername/dockchangelog/issues
