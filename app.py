from __future__ import annotations

import io
import gradio as gr
import pandas as pd

from jobspy import scrape_jobs
from jobspy.model import Country
from theme import theme


SITE_CHOICES = ["linkedin", "indeed"]
SITE_LABELS = {"linkedin": "LinkedIn", "indeed": "Indeed"}

JOB_TYPE_CHOICES = ["", "fulltime", "parttime", "contract", "internship", "temporary"]
JOB_TYPE_LABELS = {"": "", "fulltime": "Full Time", "parttime": "Part Time", "contract": "Contract", "internship": "Internship", "temporary": "Temporary"}

COUNTRY_CHOICES = sorted(
    [c.value[0].split(",")[0].title() for c in Country
     if c not in (Country.US_CANADA, Country.WORLDWIDE)],
    key=str.lower
)

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
    country_indeed: str,
    results_wanted: int,
    hours_old: int | None,
    is_remote: bool,
    job_type: str,
    distance: int,
    easy_apply: bool,
    enforce_annual_salary: bool,
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
            country_indeed=country_indeed.lower(),
            results_wanted=int(results_wanted),
            hours_old=int(hours_old) if hours_old else None,
            is_remote=is_remote,
            job_type=job_type or None,
            distance=int(distance),
            easy_apply=easy_apply or None,
            enforce_annual_salary=enforce_annual_salary,
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
    gr.HTML(HEADER_HTML)

    df_state = gr.State(None)

    with gr.Row():
        with gr.Column(scale=3):
            search_term = gr.Textbox(label="Search Query", placeholder="e.g. Software Engineer")
        with gr.Column(scale=3):
            location = gr.Textbox(label="Location", placeholder="e.g. San Francisco, CA (leave blank for remote/global)")
        with gr.Column(scale=1, min_width=160):
            sites = gr.CheckboxGroup(
                choices=[(SITE_LABELS[s], s) for s in SITE_CHOICES],
                value=["indeed", "linkedin"],
                label="Job Sites",
            )

    with gr.Row():
        with gr.Column(scale=2):
            country_indeed = gr.Dropdown(
                choices=COUNTRY_CHOICES,
                value="Usa",
                label="Country (Indeed)",
            )
        with gr.Column(scale=2):
            job_type = gr.Dropdown(choices=[(JOB_TYPE_LABELS[t], t) for t in JOB_TYPE_CHOICES], value="", label="Job Type")
        with gr.Column(scale=3):
            results_wanted = gr.Slider(5, 100, value=20, step=5, label="Jobs per Site")
        with gr.Column(scale=3):
            distance = gr.Slider(0, 100, value=50, step=5, label="Distance (Miles)")
        with gr.Column(scale=2):
            hours_old = gr.Number(label="Posted Within (Hours)", value=None, minimum=1, precision=0)

    with gr.Row():
        is_remote = gr.Checkbox(label="Remote Only")
        easy_apply = gr.Checkbox(label="Easy Apply Only (LinkedIn & Indeed)")
        enforce_annual_salary = gr.Checkbox(label="Convert Salary to Annual")
        search_btn = gr.Button("Search Jobs", variant="primary")

    status_msg = gr.Markdown("")

    results_table = gr.Dataframe(
        label="Results",
        interactive=False,
        wrap=True,
    )

    with gr.Row():
        export_btn = gr.Button("Export to CSV")
        csv_file = gr.File(label="Download CSV", visible=False)

    def on_search(*args):
        df, msg = run_scrape(*args)
        return df, df, msg

    search_btn.click(
        fn=on_search,
        inputs=[
            sites, search_term, location, country_indeed,
            results_wanted, hours_old, is_remote, job_type,
            distance, easy_apply, enforce_annual_salary,
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
        "---\n"
        "[GitHub](https://github.com/SpicyLimes/JobSpy-Docker) · Dockerized with Claude Code · "
        "Based on [JobSpy](https://github.com/speedyapply/JobSpy) by [SpeedyApply](https://www.speedyapply.com)\n\n"
        "Scraping is subject to each site's rate limits — if results are sparse, try fewer sites or add a delay between searches."
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, allowed_paths=["/app/Logo.png"])
