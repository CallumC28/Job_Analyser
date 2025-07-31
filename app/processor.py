import pandas as pd
from collections import Counter
import re

SKILLS_DB = ['Python', 'JavaScript', 'SQL', 'React', 'AWS', 'Django', 'Flask', 'Machine Learning', 'Data Analysis', 'HTML', 'CSS', 'Java', 'C++', 'Git', 'Docker']

def extract_skills(text):
    found = [skill for skill in SKILLS_DB if re.search(r'\b' + re.escape(skill) + r'\b', text, re.I)]
    return found

def analyse_jobs(df):
    df['skills'] = df['description'].apply(lambda x: extract_skills(x))

    skill_counts = Counter()
    for skills in df['skills']:
        skill_counts.update(skills)

    return dict(skill_counts.most_common(10)), {}
