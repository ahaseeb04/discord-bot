import bs4
import requests
from bot.exceptions import DataNotFoundError

def get_professor_id(professor_name):
    url = 'https://www.ratemyprofessors.com/search.jsp?query=' + '+'.join(s for s in professor_name)
    page = requests.get(url)

    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    for result in soup.find_all('li', class_='listing'):
        institution = result.find('span', class_='sub').text.lower()
        if 'york university' in institution and 'new' not in institution:
            return result.find('a')['href']
    raise DataNotFoundError()

def scrape_rmp(professor_name):
    search = lambda e, s: e.startswith(s) if e else False

    url = 'https://www.ratemyprofessors.com' + get_professor_id(professor_name)
    page = requests.get(url)

    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    metrics = soup.find_all(attrs={ 'class': lambda e: search(e, 'FeedbackItem__FeedbackNumber') })

    professor = {}
    professor['url'] = url
    professor['name'] = ' '.join(s.capitalize() for s in professor_name)
    professor['rating'] = soup.find(attrs={ 'class': lambda e: search(e, 'RatingValue__Numerator') }).text
    professor['take_again'] = metrics[0].text
    professor['difficulty'] = metrics[1].text
    professor['review'] = soup.find(attrs={ 'class': lambda e: search(e, 'Comments__StyledComments') }).text

    return professor
