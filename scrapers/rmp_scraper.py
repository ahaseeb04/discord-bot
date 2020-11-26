import bs4
import requests

def get_professors(professor_name):
    name = '+'.join(professor_name)
    url = 'https://www.ratemyprofessors.com/search.jsp?queryBy=teacherName&schoolName=york+university&query=' + name + '&country=canada'

    page = requests.get(url)

    soup = bs4.BeautifulSoup(page.content, 'html.parser', from_encoding='UTF-8')

    for result in soup.find_all('li', class_='listing'):
        institution = result.find('span', class_='sub').text.lower()
        if 'york university' in institution and 'new' not in institution:
            yield result.find('a')['href']

def scrape_rmp(professor_name):
    search = lambda s: { 'class': lambda e: e.startswith(s) if e else False }

    for professor in get_professors(professor_name):
        url = 'https://www.ratemyprofessors.com' + professor
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser', from_encoding='UTF-8')

        def _scrape_name():
            return soup.find(attrs=search('NameTitle__Name')).text.strip()

        def _scrape_department():
            return soup.find(attrs=search('NameTitle__Title')).text

        def _scrape_rating():
            return soup.find(attrs=search('RatingValue__Numerator')).text

        def _scrape_based_on_count():
            number = soup.find(attrs=search('RatingValue__NumRatings')).find('a').text.split()[0]
            return f'{number} rating' if number == '1' else f'{number} ratings'

        def _scrape_feedback():
            for div in soup.find_all(attrs=search('FeedbackItem__StyledFeedbackItem')):
                label = div.find(attrs=search('FeedbackItem__FeedbackDescription'))
                rating = div.find(attrs=search('FeedbackItem__FeedbackNumber'))
                yield (label.text, rating.text)

        def _scrape_top_review():
            for div in soup.find_all(attrs=search('Comments__StyledComments'), limit=1):
                yield div.text

        professor = {}
        professor['url'] = url
        professor['name'] = _scrape_name()
        professor['department'] = _scrape_department()
        professor['rating'] = _scrape_rating()
        professor['based_on_count'] = _scrape_based_on_count()
        professor['feedback'] = list(_scrape_feedback())[::-1]
        professor['top_review'] = next(_scrape_top_review(), None)

        yield professor
