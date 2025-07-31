import requests
from bs4 import BeautifulSoup
import pandas as pd

import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_jobs(query):
    url = 'https://www.python.org/jobs/'  # You can change this to scrape other job sites
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Prepare lists to collect data
    titles, companies, locations, descriptions, links = [], [], [], [], []

    # Get job cards from the page
    job_cards = soup.select('ol.list-recent-jobs li')
    print(f"[DEBUG] Found {len(job_cards)} job cards")

    query = query.lower()

    for job in job_cards:
        title_elem = job.find('h2')
        company_elem = job.find('span', class_='listing-company-name')
        location_elem = job.find('span', class_='listing-location')
        link_elem = job.find('a', href=True)

        title = title_elem.text.strip() if title_elem else 'N/A'
        company = company_elem.text.strip() if company_elem else 'N/A'
        location = location_elem.text.strip() if location_elem else 'N/A'
        description = ''
        job_url = ''

        print(f"[CHECKING] Title: {title}")

        if link_elem:
            job_url = f"https://www.python.org{link_elem['href']}" # Will also need to be changed if scraping a different site
            job_page = requests.get(job_url, headers=headers)
            job_soup = BeautifulSoup(job_page.text, 'html.parser')
            desc_elem = job_soup.find('div', class_='job-description')
            if desc_elem:
                description = desc_elem.get_text(separator=' ', strip=True)

        # Filter jobs based on query 
        if any(q in title.lower() or q in description.lower() for q in query.split()):
            titles.append(title)
            companies.append(company)
            locations.append(location)
            descriptions.append(description)
            links.append(job_url)
            print(f"[ADDED] {title} | {company} | {location}")

    print(f"[DEBUG] Titles collected: {titles}")
    # Create DataFrame
    df = pd.DataFrame({
        'title': titles,
        'company': companies,
        'location': locations,
        'description': descriptions,
        'link': links
    })
    # Save to CSV
    df.to_csv('data/jobs.csv', index=False)
    return df
