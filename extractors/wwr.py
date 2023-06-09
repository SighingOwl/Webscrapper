from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = 'https://weworkremotely.com/remote-jobs/search?term='
    response = get(f'{base_url}{keyword}')
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = []
        soup = BeautifulSoup(response.text, 'html.parser')
        jobs = soup.find_all('section', class_="jobs")  #   'class' 대신 'class_'를 사용하는 이유는 'class'는 이미 python 예약어이기 때문
        for job_section in jobs:
            job_posts = job_section.find_all('li')  #   find_all은 조건에 부합하는 모든 항목을 리스트로 return한다.
            job_posts.pop()
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]
                link = anchor['href']   #   find_all로 찾은 요소 하나하나는 dict로 표현되어 key로 value를 찾을 수 있다.
                company, kind, region = anchor.find_all('span', class_='company')
                title = anchor.find('span', class_='title')
                job_data = {
                    'link' : f'https://weworkremotely.com{link}',
                    'company' : company.string.replace(',', ' '),
                    'location' : region.string.replace(',', ' '),
                    'position' : title.string.replace(',', ' ')
                }
                results.append(job_data)
        return results