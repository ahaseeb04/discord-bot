import csv
from itertools import islice

import bs4
import requests

def scrape_course_list(course):
    def csv_to_dict(path):
        return {row[0]: row[1:] for row in csv.reader(open(path, 'r'))}

    def _scrape_faculty(faculty):
        def _build_link(faculty, department, course=None, session=None, year=None):
            yield f'faculty={faculty}'
            yield f'subject={department.ljust(4)}'
            if session is not None and year is not None:
                yield f'academicyear={year}'
                yield f'studysession={session}'

        prefix = "https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/wa/crsq1?"
        suffix = '&'.join(_build_link(faculty, **course))
        url = ''.join((prefix, suffix))
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')

        try:
            rows = soup.find_all('table')[6].find_all('tr', recursive=False)
        except:
            return None

        for row in rows[1:]:
            code, title, link = row.find_all('td', recursive=False)[:3]
            yield (code.text, title.text, ''.join(("https://w2prod.sis.yorku.ca/", link.find('a')['href'])))

    faculty = course.pop('faculty', None)
    if faculty is None:
        for faculty in csv_to_dict('scrapers/support/faculties.csv').get(course.get('department'), []):
            yield from _scrape_faculty(faculty)
    else:
        yield from _scrape_faculty(faculty)

def scrape_course(course):
    def _scrape_heading(soup):
        return soup.find(class_="heading").text

    def _scrape_description(soup):
        return soup.find_all('table')[2].find_all('p')[3].text

    def _scrape_lecture(soup, labels):
        def _scrape_lecture_info(soup):
            lecture_info = { label : row.text for label, row in zip(labels, soup) }
            if columns[4].find(string= lambda t: "backup" in t.lower()) is not None:
                lecture_info['backup'] = 'backup'
            return lecture_info

        columns = soup.find_all('td', recursive=False)

        if columns[2].text != 'Cancelled':
            return (columns[0].text, {
                'instructors': ', '.join(instructor.text for instructor in columns[3].find_all('a')),
                'catalogue_numbers': columns[2].text if columns[2].text is not None else '',
                'lecture_info': [ _scrape_lecture_info(row) for row in columns[1].find_all('tr') ],
            })

    def _scrape_section(soup):
        rows = soup.find_all('tr')[2].table
        labels = [ r.text.lower() for r in rows.td.next_sibling.find_all('b') ]

        return {
            'section_info': ' '.join(soup.tr.stripped_strings),
            'lectures': dict(lecture for row in islice(rows, 1, None) if (lecture := _scrape_lecture(row, labels)) is not None)
        }

    for urls in scrape_course_list(course):
        if urls[0].split()[1].startswith(course['course']):
            page = requests.get(urls[2])
            soup = bs4.BeautifulSoup(page.content, 'html.parser')

            sections = filter(lambda s: isinstance(s, bs4.element.Tag), soup.find_all('table')[6])
            yield {
                'heading': _scrape_heading(soup),
                'description': _scrape_description(soup),
                'sections': [_scrape_section(section) for section in sections],
                'url': urls[2]
            }
