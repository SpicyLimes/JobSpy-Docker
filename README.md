# JobSpy Docker

A self-hosted Gradio web UI for [JobSpy](https://github.com/cullenwatson/JobSpy), packaged as a Docker container. Search across LinkedIn, Indeed, ZipRecruiter, Glassdoor, Google Jobs, Bayt, Naukri, and BDJobs from a single interface.

## Features

- Search multiple job boards simultaneously
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
2. Select one or more job sites to search
3. Adjust filters (job type, remote, salary, recency, etc.)
4. Click **Search Jobs**
5. Optionally export results with **Export to CSV**

## Notes

- LinkedIn rate-limits aggressively — use proxies if scraping at scale.
- Indeed is generally the most reliable source with the fewest restrictions.
- All job board endpoints cap results at roughly 1,000 jobs per search.
- Scraping is subject to each site's terms of service.

## License

MIT — based on [JobSpy](https://github.com/cullenwatson/JobSpy) by Cullen Watson.
