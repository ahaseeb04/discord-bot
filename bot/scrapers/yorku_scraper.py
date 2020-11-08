import csv
from itertools import islice

import bs4
import requests

def scrape_course_list(course):
    def build_link(department, course=None, faculty=None, session=None, year=None):
        faculty = faculty or dict(csv.reader(open('bot/support/faculties.csv', 'r'))).get(department)
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
        code, title, link = row.find_all('td', recursive=False)[:3]
        yield (code.text, title.text, ''.join(("https://w2prod.sis.yorku.ca/", link.find('a')['href'])))

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
            if columns[2].text != 'Cancelled':
                lect_type = columns[0].text
                sect[info][lect_type] = {}
                instructor = ', '.join(c.text for c in row.find_all('a'))
                if len(instructor) > 1:
                    sect[info][lect_type]['instructors'] = instructor
                sect[info][lect_type]['lectures'] = []
                for row in columns[1].find_all('tr'):
                    lec = { l : r.text for l, r in zip(labels, row) }
                    if columns[4].find(string= lambda t: "backup" in t.lower()) is not None:
                        lec['Backup'] = 'backup'
                    sect[info][lect_type]['lectures'].append(lec)
        return sect


    URLS = list(scrape_course_list(course))

    for URL in URLS:
        if URL[0].split()[1] == course['course']:
            page = requests.get(URL[2])
            soup = bs4.BeautifulSoup(page.content, 'html.parser')

            crs = {}
            crs['heading'] = scrape_heading(soup)
            crs['description'] = scrape_description(soup)
            sections = filter(lambda s: isinstance(s, bs4.element.Tag), soup.find_all('table')[6])
            crs['sections'] = list(map(scrape_section, sections))
            crs['url'] = URL[2]
            yield crs
