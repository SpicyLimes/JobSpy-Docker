from __future__ import annotations

import io
import gradio as gr
import pandas as pd

from jobspy import scrape_jobs
from theme import theme


SITE_CHOICES = ["linkedin", "indeed"]
SITE_LABELS = {"linkedin": "LinkedIn", "indeed": "Indeed"}

JOB_TYPE_CHOICES = ["", "fulltime", "parttime", "contract", "internship", "temporary"]
JOB_TYPE_LABELS = {"": "Any", "fulltime": "Full Time", "parttime": "Part Time", "contract": "Contract", "internship": "Internship", "temporary": "Temporary"}

HEADER_HTML = """
<div style="display:flex; align-items:center; gap:16px; padding:8px 0 4px;">
    <img src="/gradio_api/file=/app/Logo.png" style="height:60px; width:auto;">
    <span style="font-size:1rem; opacity:0.7; line-height:1.4;">
        Search LinkedIn &amp; Indeed simultaneously —<br>filter, compare, and export results in one place.
    </span>
</div>
"""


def run_scrape(
    sites: list[str],
    search_term: str,
    location: str,
    results_wanted: int,
    hours_old: int | None,
    is_remote: bool,
    job_type: str,
    distance: int,
):
    if not sites:
        return None, "Select at least one Job Site"
    if not search_term.strip():
        return None, "Enter a Search Query"

    try:
        df = scrape_jobs(
            site_name=sites,
            search_term=search_term.strip(),
            location=location.strip() or None,
            country_indeed="usa",
            results_wanted=int(results_wanted),
            hours_old=int(hours_old) * 24 if hours_old else None,
            is_remote=is_remote,
            job_type=job_type or None,
            distance=int(distance),
            description_format="markdown",
            verbose=0,
        )
    except Exception as e:
        return None, f"Error: {e}"

    if df.empty:
        return None, "No Jobs Found - Use a Broader Search Query"

    display_cols = [
        "site", "title", "company", "location", "date_posted",
        "job_type", "interval", "min_amount", "max_amount", "currency",
        "is_remote", "job_url",
    ]
    display_cols = [c for c in display_cols if c in df.columns]

    return df[display_cols], f"{len(df)} jobs found across {len(sites)} site(s)."


with gr.Blocks(title="JobSpy Docker — Job Search Aggregator", theme=theme) as demo:

    df_state = gr.State(None)

    # ── Header: logo + subtitle left, action buttons right ───────────
    with gr.Row(equal_height=True):
        with gr.Column(scale=6):
            gr.HTML(HEADER_HTML)
        with gr.Column(scale=1, min_width=140):
            search_btn = gr.Button("Search Jobs", variant="primary")
        with gr.Column(scale=1, min_width=140):
            export_btn = gr.Button("Export to CSV")

    # ── Row 1: Search Query (+ site checkboxes) | Location (+ remote) ──
    with gr.Row():
        with gr.Column(scale=1):
            search_term = gr.Textbox(label="Search Query", placeholder="e.g. Software Engineer")
            sites = gr.CheckboxGroup(
                choices=[(SITE_LABELS[s], s) for s in SITE_CHOICES],
                value=["indeed", "linkedin"],
                label="",
                container=False,
            )
        with gr.Column(scale=1):
            location = gr.Textbox(label="Location", placeholder="e.g. San Francisco, CA (leave blank for remote/global)")
            is_remote = gr.Checkbox(label="Remote Only")

    # ── Row 2: Job Type | Posted Within | Jobs per Site | Distance ───
    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            job_type = gr.Dropdown(
                choices=[(JOB_TYPE_LABELS[t], t) for t in JOB_TYPE_CHOICES],
                value="",
                label="Job Type",
            )
        with gr.Column(scale=1):
            hours_old = gr.Number(label="Posted Within (Days)", value=None, minimum=1, precision=0)
        with gr.Column(scale=1):
            results_wanted = gr.Slider(5, 100, value=20, step=5, label="Jobs per Site")
        with gr.Column(scale=1):
            distance = gr.Slider(0, 100, value=50, step=5, label="Distance (Miles)")


    status_msg = gr.Markdown("")

    results_table = gr.Dataframe(
        label="Results",
        interactive=False,
        wrap=True,
    )

    csv_file = gr.File(label="Download CSV", visible=False)

    def on_search(*args):
        df, msg = run_scrape(*args)
        return df, df, msg

    search_btn.click(
        fn=on_search,
        inputs=[
            sites, search_term, location,
            results_wanted, hours_old, is_remote, job_type, distance,
        ],
        outputs=[results_table, df_state, status_msg],
    )

    def on_export(df):
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            return gr.update(visible=False)
        buf = io.StringIO()
        df.to_csv(buf, index=False)
        tmp_path = "/tmp/jobspy_results.csv"
        with open(tmp_path, "w") as f:
            f.write(buf.getvalue())
        return gr.update(value=tmp_path, visible=True)

    export_btn.click(fn=on_export, inputs=[df_state], outputs=[csv_file])

    gr.Markdown(
        "\n[GitHub](https://github.com/SpicyLimes/JobSpy-Docker) · Dockerized with Claude Code · "
        "Based on [JobSpy](https://github.com/speedyapply/JobSpy) by [SpeedyApply](https://www.speedyapply.com)\n\n"
        "Scraping is subject to each site's rate limits — if results are sparse, try fewer sites or add a delay between searches."
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, allowed_paths=["/app/Logo.png"])
