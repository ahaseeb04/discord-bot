import bs4
import requests

def get_professors(professor_name):
    name = '+'.join(professor_name)
    url = ''.join(('https://www.ratemyprofessors.com/search.jsp?queryBy=teacherName&schoolName=york+university&query=', name, '&country=canada'))
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser', from_encoding='UTF-8')

    for result in soup.find_all('li', class_='listing'):
        yield result.find('a')['href']

def scrape_rmp(professor_name):
    search = lambda s: { 'class': lambda e: e.startswith(s) if e else False }

    def _scrape_field(soup, field):
        return soup.find(attrs=search(field)).text.strip()

    def _scrape_based_on_count(soup):
        return soup.find(attrs=search('RatingValue__NumRatings')).find('a').text.split()[0]

    def _scrape_feedback(soup):
        for div in soup.find_all(attrs=search('FeedbackItem__StyledFeedbackItem')):
            label = _scrape_field(div, 'FeedbackItem__FeedbackDescription')
            rating = _scrape_field(div, 'FeedbackItem__FeedbackNumber')

            yield (label, rating)

    def _scrape_top_review(soup):
        for div in soup.find_all(attrs=search('Comments__StyledComments'), limit=1):
            yield div.text

    for professor in get_professors(professor_name):
        url = ''.join(('https://www.ratemyprofessors.com', professor))
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser', from_encoding='UTF-8')

        yield {
            'url': url,
            'name': _scrape_field(soup, 'NameTitle__Name'),
            'department': _scrape_field(soup, 'NameTitle__Title'),
            'rating': _scrape_field(soup, 'RatingValue__Numerator'),
            'based_on_count': _scrape_based_on_count(soup),
            'feedback': list(_scrape_feedback(soup))[::-1],
            'top_review': next(_scrape_top_review(soup), None)
        }