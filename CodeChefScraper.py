import grequests
import requests
import json
from bs4 import BeautifulSoup, SoupStrainer

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
}


def get_links(username):
    html = requests.get(
        f'https://www.codechef.com/users/{username}', headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    for link in soup.select('a[href^="/problems/"]'):
        yield 'https://www.codechef.com' + link['href'] + '?status=FullAC'


def get_submission_links(html):
    soup = BeautifulSoup(html, 'lxml', parse_only=SoupStrainer('td'))
    return [f'https://www.codechef.com{obj.a["href"]}' for obj in soup.find_all('td', class_='solution-submission-time')]


def get_info(solution_id):
    link1 = f'https://www.codechef.com/api/submission-code/{solution_id}'
    link2 = f'https://www.codechef.com/api/submission-details/{solution_id}'
    data1 = requests.get(link1, headers=headers).text
    data2 = requests.get(link2, headers=headers).text
    json_data1 = json.loads(data1)
    json_data2 = json.loads(data2)

    contest_code = json_data2['data']['other_details']['contestCode']
    problem_code = json_data2['data']['other_details']['problemCode']

    return {
        'language': json_data1['data']['language']['short_name'],
        'problem_code': problem_code,
        'solution_id': solution_id,
        'problem_link': f'https://www.codechef.com/{contest_code}/problems/{problem_code}',
        'link': f'https://www.codechef.com/viewsolution/{solution_id}',
        'solution': json_data1['data']['code'],
    }


def get_solutions(username):
    links = list(get_links(username))[::-1]
    reqs = (grequests.get(u, headers=headers) for u in links)
    responses = grequests.map(reqs)

    submission_links = [
        link for response in responses for link in get_submission_links(response.content)]
    submission_reqs = (grequests.get(u, headers=headers)
                       for u in submission_links)
    submission_responses = grequests.map(submission_reqs)

    for response in submission_responses:
        solution_id = response.url.split('/')[-1]
        yield get_info(solution_id)


# Example usage:
username = 'your_username'
for solution in get_solutions(username):
    print(solution)
