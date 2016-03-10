import csv
from urllib.request import urlopen

from bs4 import BeautifulSoup

BASE_URL = 'http://www.weblancer.net/projects/'


def get_html(url):
    response = urlopen(url)
    return response.read()


def get_page_count(html):
    soup = BeautifulSoup(html, "html5lib")
    pagination = soup.find('ul', class_='pagination')
    return int(pagination.find_all('a')[-3].text)


def parse(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', class_='container-fluid cols_table show_visited')
    rows = table.find('div', class_='row')

    projects = []
    for row in rows:
        cols = row.find_all('td')

        projects.append({
            'title': cols[0].a.text,
            'categories': [category.text for category in cols[0].find_all('noindex')],
            'price': cols[1].text.strip().split()[0],
            'application': row.find('div', class_='col-sm-3')[0].text.split()[0]
        })

    return projects


def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(('Project', 'Category', 'Price', 'Request'))

        writer.writerows(
            (project['title'], ', '.join(project['categories']), project['price'], project['application']) for project
            in projects
        )


def main():
    total_pages = get_page_count(get_html(BASE_URL))

    print('Found %d pages...' % total_pages)

    projects = []

    for page in range(1, total_pages + 1):
        print('Parsing %d%% (%d/%d)' % (page / total_pages * 100, page, total_pages))
        projects.extend(parse(get_html(BASE_URL + "page=%d" % page)))

    print('saving...')
    save(projects, 'projects.csv')


if __name__ == '__main__':
    main()
