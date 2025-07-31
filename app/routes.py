from flask import Blueprint, render_template, request
from .scraper import scrape_jobs
from .processor import analyse_jobs

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/results')
def results():
    query = request.args.get('query', 'developer')
    jobs_df = scrape_jobs(query)
    skills, _ = analyse_jobs(jobs_df)
    job_list = jobs_df[['title', 'company', 'location']].to_dict(orient='records')
    job_links = jobs_df['link'].tolist() if 'link' in jobs_df else []
    return render_template('results.html', skills=skills, job_list=list(zip(job_list, job_links)))
