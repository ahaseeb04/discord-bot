import bs4
import requests

from bot.exceptions import DataNotFoundError

def get_professor_id(professor_name):
    name = '+'.join(professor_name)
    url = 'https://www.ratemyprofessors.com/search.jsp?queryBy=teacherName&schoolName=york+university&query=' + name + '&country=canada'

    page = requests.get(url)

    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    for result in soup.find_all('li', class_='listing'):
        institution = result.find('span', class_='sub').text.lower()
        if 'york university' in institution and 'new' not in institution:
            yield result.find('a')['href']

def scrape_rmp(professor_name):
    # search = lambda e, s: e.startswith(s) if e else False
    search = lambda s: { 'class': lambda e: e.startswith(s) if e else False }

    for professor in get_professor_id(professor_name):
        url = 'https://www.ratemyprofessors.com' + professor
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')

        # def _scrape_first_name():
        #     return soup.find(attrs={ 'class': lambda e: search(e, 'NameTitle__Name') }).find('span').text.strip()

        # def _scrape_last_name():
        #     return soup.find(attrs={ 'class': lambda e: search(e, 'NameTitle__LastNameWrapper') }).text.strip()

        def _scrape_full_name():
            # return soup.find(attrs={ 'class': lambda e: search(e, 'NameTitle__Name') }).text.strip()
            return soup.find(attrs=search('NameTitle__Name')).text.strip()
            # return f'{_scrape_first_name()} {_scrape_last_name()}'

        def _scrape_department():
            # department = soup.find(attrs={ 'class': lambda e: search(e, 'NameTitle__Title') }).find('span').text
            # institution = soup.find(attrs={ 'class': lambda e: search(e, 'NameTitle__Title') }).find('a').text

            # return f'{department.strip()} {institution.strip()}'
            return soup.find(attrs=search('NameTitle__Title')).text

        def _scrape_rating():
            return soup.find(attrs=search('RatingValue__Numerator')).text

        # def _scrape_retake_percentage():
        #     s = soup.find_all(attrs={ 'class': lambda e: search(e, 'FeedbackItem__FeedbackNumber') })
        #     return s[0].text

        # def _scrape_difficulty():
        #     s = soup.find_all(attrs={ 'class': lambda e: search(e, 'FeedbackItem__FeedbackNumber') })
        #     return s[1].text

        def _scrape_feedback():
            for div in soup.find_all(attrs=search('FeedbackItem__StyledFeedbackItem')):
                label = div.find(attrs=search('FeedbackItem__FeedbackDescription'))
                rating = div.find(attrs= search('FeedbackItem__FeedbackNumber'))
                yield ( label.text, rating.text )

        def _scrape_top_review():
            for div in soup.find_all(attrs=search('Comments__StyledComments'),limit=1):
                yield div.text

        professor = {}
        professor['url'] = url
        professor['name'] = _scrape_full_name()
        professor['description'] = _scrape_department()
        professor['rating'] = _scrape_rating()
        # professor['retake_percentage'] = _scrape_retake_percentage()
        # professor['difficulty'] = _scrape_difficulty()
        professor['feedback'] = list(_scrape_feedback())[::-1]
        professor['top_review'] = next(_scrape_top_review(), None)

        yield professor
