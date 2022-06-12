import json
import os
import requests
from bs4 import BeautifulSoup

# Making variable for checking url status code
url = 'https://www.indeed.com/jobs?'
site = 'https://www.indeed.com'
params = {
    'q': 'Python Developer',
    'l': 'United States',
    'vjk': '676599852a737304'
}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/102.0.5005.63 Safari/537.36'}

# Request form url with parameters & headers
req = requests.get(url, params=params, headers=headers)

# Function for scraping job-list
def job_list():
    params = {
        'q': 'Python Developer',
        'l': 'United States',
        'vjk': '676599852a737304'
    }
    req = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/req.html', 'w+') as outfile:
        outfile.write(req.text)
        outfile.close()

    soup = BeautifulSoup(req.text, 'html.parser')
    contents = soup.find_all('table', 'jobCard_mainContent big6_visualChanges')

    jobs_db = []

    for list in contents:
        title = list.find('h2', 'jobTitle').text
        company = list.find('span', 'companyName')
        company_name = company.text
        try:
            company_web = site + company.find('a')['href']
        except:
            company_web = 'Company Web Is Not Available'

        # Sorting data with dictionary
        data_dict = {
            'title': title,
            'company': company_name,
            'website': company_web
        }
        jobs_db.append(data_dict)

    # Create JSON File
    try:
        os.mkdir('json_res')
    except FileExistsError:
        pass

    with open('json_res/joblist.json', 'w+') as json_data:
        json.dump(jobs_db, json_data)

    print("JSON File Has Been Created!")


if __name__ == '__main__':
    job_list()


