import requests
import bs4

# course = ["LE", "EECS", "3101"]
course = ["SC", "PHYS", "1411"]

URL = f"https://w2prod.sis.yorku.ca/Apps/WebObjects/cdm.woa/wa/crsq1?faculty={course[0]}&subject={course[1]}&academicyear=2020&studysession=FW"
page = requests.get(URL)

soup = bs4.BeautifulSoup(page.content, 'html.parser')
rows = soup.find_all('table')[6].find_all('tr')
  
def lookup(rows, course_code):
    for row in rows[1:]:
        code, link = row.find_all('td')[::2]
        if code.text.split()[1] == course_code:
            return ''.join(("https://w2prod.sis.yorku.ca/", link.find('a')['href']))

URL = lookup(rows, course[2])
page = requests.get(URL)
soup = bs4.BeautifulSoup(page.content, 'html.parser')

courses = [section for section in soup.find_all('table')[6] if isinstance(section, bs4.element.Tag)]

for section in courses:
    info = section.find('tr').text.strip()
    print(info)
    rows = section.find_all('tr')[2].find('table')
    for row in list(rows)[1:]:
        children = list(row.children)
        instructor = ', '.join(c.text for c in children[3].find_all('a'))
        lect = children[0].text
        times = ' '.join(c.text for c in children[1].find_all('td'))
        if children[2].text == 'Cancelled':
            print('Cancelled')
        if len(instructor) > 1:
            print("Instructor:", instructor)
        if len(times):
            print(lect, times, sep=': ')