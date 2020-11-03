import csv
from itertools import islice

import bs4
import requests


def find_course_URL(course):
    def build_link(faculty, department, number, session, year):
        faculty = faculty or dict(csv.reader(open('bot/scraper/faculties.csv', 'r'))).get(department)
        yield f'faculty={faculty}'
        yield f'subject={department}'
        if session is not None and year is not None:
            yield f'academicyear={year}'
            yield f'studysession={session}'

    prefix = "https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/wa/crsq1?"
    suffix = '&'.join(build_link(**course))
    URL = ''.join([prefix, suffix])

    page = requests.get(URL)

    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    try:
        rows = soup.find_all('table')[6].find_all('tr', recursive=False)
    except:
        return None

    for row in rows[1:]:
        code, link = row.find_all('td', recursive=False)[::2]
        if code.text.split()[1] == course['number']:
            return ''.join(("https://w2prod.sis.yorku.ca/", link.find('a')['href']))
    return None

def scrape_course(course):
    def scrape_heading(soup):
        return soup.find(class_="heading").text

    def scrape_description(soup):
        return soup.find_all('table')[2].find_all('p')[3].text

    def scrape_section(section):
        sect = {}
        info = ' '.join(section.tr.stripped_strings)
        rows = section.find_all('tr')[2].table
        labels = [r.text for r in rows.td.next_sibling.find_all('b')]

        sect[info] = {}
        for row in islice(rows, 1, None):
            columns = row.find_all('td', recursive=False)
            if columns[2].text == 'Cancelled':
                sect[info] = 'Cancelled'
            else:
                lect_type = columns[0].text
                sect[info][lect_type] = {}
                instructor = ', '.join(c.text for c in row.find_all('a'))
                if len(instructor) > 1:
                    sect[info][lect_type]['instructors'] = instructor
                sect[info][lect_type]['lectures'] = []
                for row in columns[1].find_all('tr'):
                    lec = { l : r.text for l, r in zip(labels, row) }
                    sect[info][lect_type]['lectures'].append(lec)
        return sect
        

    URL = find_course_URL(course)
    if URL is None:
        return {'error': 'page_not_found'}
    page = requests.get(URL)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    crs = {}
    crs['heading'] = scrape_heading(soup)
    crs['description'] = scrape_description(soup)
    sections = filter(lambda s: isinstance(s, bs4.element.Tag), soup.find_all('table')[6])
    crs['sections'] = list(map(scrape_section, sections))

    return crs
    
if __name__ == "__main__":
    import re

    # course = "LE EECS 3101 FW 2020"
    # course = "LE EECS 3101"
    course = "EECS 3101"
    # course = "EN 3101 FW 2020"
    m = re.match("(?:(?P<faculty>[a-z]{2})\s)?(?:(?P<department>[a-z]{2,4})\s(?P<number>[0-9]{4}))+(?:\s(?P<session>[a-z]{2})\s(?P<year>[0-9]{4}))?", course.lower())

    print(scrape_course(m.groupdict()))
