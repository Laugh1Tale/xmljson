from itertools import groupby
from urllib.request import urlopen
import urllib.parse
from json import loads
import datetime
from colorama import init


def set_title():
    print()
    print('\033[37mВведите заголовок статьи, выглядящий как часть ссылки, выделенная зеленым цветом.')
    print("\033[31mhttps://ru.wikipedia.org/wiki/\033[32mГрадский,_Александр_Борисович")
    title = input()
    print('\033[37m')
    return title


def title_processing(title):
    return urllib.parse.quote_plus(title)


def revision_search(title):
    url = (
            'https://ru.wikipedia.org/w/api.php'
            '?action=query'
            '&format=json'
            '&prop=revisions'
            '&rvlimit=500'
            '&titles=' + ''.join(title))
    data = loads(urlopen(url).read().decode('utf8'))
    revision = data['query']['pages'][list(data['query']['pages'])[0]]['revisions']
    return revision


def make_revisions_stat(revision):
    max_revisions = 0
    date_of_revision = datetime.datetime
    for date, count in groupby(revision,
                               lambda revision_date: datetime.datetime.strptime(revision_date['timestamp'],
                                                                                '%Y-%m-%dT%H:%M:%SZ').date()):
        count1 = len(list(count))
        # print(date, count1)
        if max_revisions < count1:
            date_of_revision = date
            max_revisions = count1
    return date_of_revision, max_revisions


def write_revisions_stat(revision_stat):
    date_of_revisions = revision_stat[0]
    max_revisions = revision_stat[1]
    print('|    date    | revisions per day |')
    space_number = int((18 - len(str(max_revisions))) / 2)
    print('| {} |{}{}{} |'.format(date_of_revisions,
                                  ' ' * space_number if len(str(max_revisions)) % 2 == 0 else ' ' * (space_number + 1),
                                  max_revisions, ' ' * space_number))


def death_date_search(title):
    url = (
            'https://www.wikidata.org/w/api.php'
            '?action=wbgetentities'
            '&format=json'
            '&sites=ruwiki'
            '&props=claims'
            '&titles=' + ''.join(title))
    data = loads(urlopen(url).read().decode('utf8'))
    try:
        death_date = data['entities'][list(data['entities'])[0]]['claims']['P570'][0]['mainsnak']['datavalue']['value'][
            'time']
    except Exception as e:
        death_date = e
    return death_date


def write_death_date(death_date):
    if type(death_date) is KeyError:
        print()
        print('{} отстустствует))) думаю понятно что значит)))'.format(death_date))
    else:
        print()
        print('date of death')
        print(datetime.datetime.strptime(death_date, '+%Y-%m-%dT%H:%M:%SZ').date())


if __name__ == "__main__":
    init()
    #title_name = set_title()
    titles = ['Lil_Peep', 'XXXTentacion', 'Pop_Smoke', 'Young_Dolph', 'DMX',
              'Oxxxymiron', 'Градский,_Александр_Борисович', 'Бельмондо,_Жан-Поль']
    for title_name in titles:
        print(title_name)
        print()
        title_name = title_processing(title_name)
        revisions = revision_search(title_name)
        stat = make_revisions_stat(revisions)
        write_revisions_stat(stat)
        date_of_death = death_date_search(title_name)
        write_death_date(date_of_death)
        print()
