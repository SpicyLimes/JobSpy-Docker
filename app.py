from __future__ import annotations

import io
import gradio as gr
import pandas as pd

from jobspy import scrape_jobs
from jobspy.model import Country


SITE_CHOICES = ["LinkedIn", "Indeed", "Zip-Recruiter", "Glassdoor", "Google", "Bayt", "Naukri", "BDJobs"]

JOB_TYPE_CHOICES = ["", "Fulltime", "PartTime", "Contract", "Internship", "Temporary"]

COUNTRY_CHOICES = sorted(
    [c.value[0].split(",")[0].title() for c in Country
     if c not in (Country.US_CANADA, Country.WORLDWIDE)],
    key=str.lower
)


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
        "Site", "Title", "Company", "Location", "Date-Posted",
        "Job-Type", "Interval", "Min-Amount", "Max-Amount", "Currency",
        "Is-Remote", "Job-URL",
    ]
    display_cols = [c for c in display_cols if c in df.columns]

    return df[display_cols], f"{len(df)} jobs found across {len(sites)} site(s)."


def export_csv(df_state):
    if df_state is None or (isinstance(df_state, pd.DataFrame) and df_state.empty):
        return None
    buf = io.BytesIO()
    df_state.to_csv(buf, index=False)
    buf.seek(0)
    return gr.File.update(value=buf, visible=True) if hasattr(gr.File, "update") else buf


with gr.Blocks(title="JobSpy Docker — Job Search Aggregator", theme=gr.Theme.from_hub("d8ahazard/rd_blue")) as demo:
    gr.Markdown("# JobSpy Docker — Job Search Aggregator")
    gr.Markdown(
        "Search across LinkedIn, Indeed, ZipRecruiter, Glassdoor, Google Jobs, and more — all at once!"
    )

    df_state = gr.State(None)

    with gr.Row():
        with gr.Column(scale=2):
            search_term = gr.Textbox(label="Search Query", placeholder="e.g. Software Engineer")
            location = gr.Textbox(label="Location", placeholder="e.g. San Francisco, CA (leave blank for remote/global)")

        with gr.Column(scale=1):
            sites = gr.CheckboxGroup(
                choices=SITE_CHOICES,
                value=["Indeed", "LinkedIn", "Glassdoor", "Zip-Recruiter"],
                label="Job Sites",
            )

    with gr.Row():
        results_wanted = gr.Slider(5, 100, value=20, step=5, label="Jobs per Site")
        distance = gr.Slider(0, 100, value=50, step=5, label="Distance (Miles)")
        hours_old = gr.Number(label="Posted within... (Hours)", value=None, minimum=1, precision=0)

    with gr.Row():
        country_indeed = gr.Dropdown(
            choices=COUNTRY_CHOICES,
            value="USA",
            label="Country (Indeed & Glassdoor)",
        )
        job_type = gr.Dropdown(choices=JOB_TYPE_CHOICES, value="", label="Job Type")

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
        "Built on [JobSpy](https://github.com/cullenwatson/JobSpy). "
        "Scraping is subject to each site's rate limits — if results are sparse, try fewer sites or add a delay between searches."
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
