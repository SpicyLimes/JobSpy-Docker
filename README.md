# JobSpy Docker

A self-hosted Gradio web UI for [JobSpy](https://github.com/speedyapply/JobSpy), packaged as a Docker container. Search across LinkedIn and Indeed simultaneously — filter, compare, and export results in one place.

## Features

- Search LinkedIn and Indeed simultaneously
- Filter by job type, location, country, remote status, salary, and recency
- Export results to CSV
- Runs entirely locally — no external accounts or API keys required

## Quick Start

### Docker Compose (recommended)

```yaml
services:
  jobspy:
    image: ghcr.io/spicylimes/jobspy:latest
    container_name: jobspy
    ports:
      - "7860:7860"
    restart: unless-stopped
```

```bash
docker compose up -d
```

Then open [http://localhost:7860](http://localhost:7860) in your browser.

### Build locally

```bash
docker build -t jobspy .
docker run -p 7860:7860 jobspy
```

## Usage

1. Enter a search term and optional location
2. Select one or both job sites (LinkedIn, Indeed)
3. Adjust filters (job type, remote, salary, recency, etc.)
4. Click **Search Jobs**
5. Optionally export results with **Export to CSV**

## Notes

- LinkedIn rate-limits aggressively — results may be sparse without proxies.
- Indeed is generally the most reliable source with the fewest restrictions.
- Scraping is subject to each site's terms of service.

## License

MIT — based on [JobSpy](https://github.com/speedyapply/JobSpy) by SpeedyApply.
