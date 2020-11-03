from itertools import islice

import requests
import bs4
  
def find_course_URL(course):
    URL = f"https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/wa/crsq1?faculty={course[0]}&subject={course[1]}&academicyear=2020&studysession=FW"
    page = requests.get(URL)

    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all('table')[6].find_all('tr', recursive=False)

    for row in rows[1:]:
        code, link = row.find_all('td', recursive=False)[::2]
        if code.text.split()[1] == course[2]:
            return ''.join(("https://w2prod.sis.yorku.ca/", link.find('a')['href']))

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
    page = requests.get(URL)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')

    crs = {}
    crs['heading'] = scrape_heading(soup)
    crs['description'] = scrape_description(soup)
    sections = filter(lambda s: isinstance(s, bs4.element.Tag), soup.find_all('table')[6])
    crs['sections'] = list(map(scrape_section, sections))

    return crs
    
if __name__ == "__main__":
    course = ["LE", "EECS", "3101"]
    # course = ["SC", "PHYS", "1421"]
    # course = ["AP", "ECON", "1000"]

    print(scrape_course(course))
