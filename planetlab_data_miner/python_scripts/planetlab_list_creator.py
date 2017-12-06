#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Vytvoril Pavol Ilko
# Vysoke uceni technicke v Brne
#
import argparse
import codecs
import getpass
import os
import datetime
import textwrap
import requests
import re
import socket
import geocoder
import time

from shutil import copyfile
from urlparse import urljoin
from bs4 import BeautifulSoup
from requests.packages.urllib3.connection import ConnectionError
from contextlib import closing

user_data = {'username': '', 'password': '', 'base_url': 'https://planet-lab.org/', 'save_path': '', 'id_host': 30001,
             'first': True, 'timeout': 60, 'exception_repetition': 5, 'exception_occurred': 0}
list_of_planetlab_hosts = []
planetlab_hosts_href = []
continents = {
    'AF': {'name': 'Africa',
           'countries': ['DZ', 'AO', 'BJ', 'BW', 'BF', 'BI', 'CM', 'CV', 'CF', 'TD', 'KM', 'CD', 'CG', 'CI', 'DJ', 'EG',
                         'GQ', 'ER', 'ET', 'GA', 'GM', 'GH', 'GN', 'GW', 'KE', 'LS', 'LR', 'LY', 'MG', 'MW', 'ML', 'MR',
                         'MU', 'YT', 'MA', 'MZ', 'NA', 'NE', 'NG', 'RE', 'RW', 'SH', 'ST', 'SN', 'SC', 'SL', 'SO', 'ZA',
                         'SD', 'SZ', 'TZ', 'TG', 'TN', 'UG', 'EH', 'ZM', 'ZW'], 'center': [1.054628, 29.53125]},
    'NA': {'name': 'North America',
           'countries': ['AI', 'AG', 'AW', 'BS', 'BB', 'BZ', 'BM', 'VG', 'CA', 'KY', 'CR', 'CU', 'DM', 'DO', 'SV', 'GL',
                         'GD', 'GP', 'GT', 'HT', 'HN', 'JM', 'MQ', 'MX', 'MS', 'AN', 'NI', 'PA', 'PR', 'BL', 'KN', 'LC',
                         'MF', 'PM', 'VC', 'TT', 'TC', 'US', 'VI'], 'center': [47.694974, -94.042969]},
    'OC': {'name': 'Oceania',
           'countries': ['AS', 'AU', 'CK', 'FJ', 'PF', 'GU', 'KI', 'MH', 'FM', 'NR', 'NC', 'NZ', 'NU', 'NF', 'MP', 'PW',
                         'PG', 'PN', 'WS', 'SB', 'TK', 'TO', 'TV', 'UM', 'VU', 'WF'], 'center': [-8.05923, 142.734375]},
    'AN': {'name': 'Antarctica', 'countries': ['AQ', 'BV', 'TF', 'HM', 'GS'], 'name': 'Antarctica',
           'center': [-78.836065, 39.375]},
    'AS': {'countries': ['AF', 'AM', 'AZ', 'BH', 'BD', 'BT', 'IO', 'BN', 'KH', 'CN', 'CX', 'CC', 'CY', 'GE',
                         'HK', 'IN', 'ID', 'IR', 'IQ', 'IL', 'JP', 'JO', 'KZ', 'KP', 'KR', 'KW', 'KG', 'LA',
                         'LB', 'MO', 'MY', 'MV', 'MN', 'MM', 'NP', 'OM', 'PK', 'PS', 'PH', 'QA', 'SA', 'SG',
                         'LK', 'SY', 'TW', 'TJ', 'TH', 'TL', 'TR', 'TM', 'AE', 'UZ', 'VN', 'YE'],
           'name': 'Asia', 'center': [30.448674, 125.15625]}, 'EU': {
        'countries': ['AX', 'AL', 'AD', 'AT', 'BY', 'BE', 'BA', 'BG', 'HR', 'CZ', 'DK', 'EE', 'FO', 'FI', 'FR', 'DE',
                      'GI', 'GR', 'GG', 'VA', 'HU', 'IS', 'IE', 'IM', 'IT', 'JE', 'LV', 'LI', 'LT', 'LU', 'MK', 'MT',
                      'MD', 'MC', 'ME', 'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS', 'SK', 'SI', 'ES', 'SJ', 'SE',
                      'CH', 'UA', 'GB'], 'name': 'Europe', 'center': [45.521744, 21.972656]},
    'SA': {'countries': ['AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'FK', 'GF', 'GY', 'PY', 'PE', 'SR', 'UY', 'VE'],
           'name': 'South America', 'center': [-4.039618, -65.039062]}}


def parse_arguments():
    """
    Parse arguments program runs with.
    """
    # Argument parser
    parser = argparse.ArgumentParser(
        prog='planet-lab_list_creator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
        Program planet_lab_creator.py sluzi na automatizovane vytvorenie zoznamu stanic siete planet-lab.\n
        Fungovanie programu:
        Pomocou uzivatelskych udajov zadanych v parametroch (-u, -p) sa program prihlasi na web https://planet-lab.org/.
        Pri pouziti parametru -e sa program prihlasi na web https://www.planet-lab.eu/.
        Po sputeni programu nieje vyzadovana ziadna interakcia s uzivatelom.\n
        Vygenerovany zoznam bude ulozeny do suboru planetlab.node do zlozky, kde je umiestneny program.
        V pripade, ked si uzivatel zvoli prepinac -f moze urcit, kde sa ma subor ulozit.
        Po vytvoreni suboru planetlab.node sa vytvori jeho kopia s casom vytvorenia v nazve ("planetlab_%d-%m-%y_%H-%M.node").\n
        Zoznam obsahuje stlpce: 'ID', 'IP', 'DNS', 'continent', 'country', 'region', 'city', 'url', 'full_name',
        'latitude', 'longitude', 'flag if web IP is different from DNS conversion'.\n
        Pri zvoleni prepinaca -s mozme zvojit ake bude ID prvej stanice. Bez prepinaca sa automaticky voli 30001.\n
        IP adresa zariadenia je vycitana z webu planet-lab, ked je na webe dostupna. Ta je spravidla dostupna na
        staniciach, ktore su sucastou PLC. V pripade, ze IP adresa nieje na webe dostupna, adresu program ziska pomocou
        prekladu z DNS mena stanice. Program navyse overi, ci IP adresa, ktoru ziskal z webovej stranky planet-labu je
        zhodna s adresou ziskanou pomocou prekladu domenoveho mena. Ked sa nezhoduje vypise sa chybova hlaska s dns
        menom a oboma IP adresami. Do vysledneho suboru sa ulozi IP adresa ziskana z webu. Pri vyhodnocovani IP sa
        uklada flag 'diffIpFromDns' - rozdiela IP na webe a z DNS, 'unknown' - IP adresa nieje na webe dostupna,
        'noIpFromDns' - DNS meno nebolo mozne prelozit na IP adresu.\n
        Z webu je taktiez vycitany nazov institucie spravujucej danu stanicu a GPS suradnice, kde sa stanica nachadza.
        Pomocou reverznej geolokacie zistime adresu z GPS suradnic. Z adresy vyberieme krajinu, region a mesto.
        Kontinent je urceny na zaklade krajiny, kedze tanto udaj nieje poskytnuty v ramci reverznej geolokacie.\n
        Stanice v zozname nemusia byt sucastou ziadneho slice.\n
        Pri spracovani udajov moze nastat chyba komunikacie z PostgreSQL databazou webovej stranky planet-lab.org, preto
        je mozne prepinacom urcit timeout, kolko sa ma cakat na opakovanie merania, pri vyhodeni chyby a taktiez kolko
        maximalne opakovani ma byt na meranie kazdej stanice.\n
        Vygenerovanie zoznamu stanic trva programu priblizne 60 minut.

        Priklad pouzitia:
        python planetlab_list_creator.py -u uzivatel@gmail.com -p heslo -f . -s 50000
        '''),
        epilog='''
        Vytvoril Pavol Ilko
        Vysoke uceni technicke v Brne
        ''')
    parser.add_argument("-u", "--username", help="Username")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-e", "--eu", action="store_true", help="Planet-lab server - planet-lab.eu")
    parser.add_argument("-f", "--file_path", help="Path where you want to save file planetlab.node")
    parser.add_argument("-s", "--id_start", help="Starting id number")
    parser.add_argument("-t", "--timeout", help="Timeout on exception")
    parser.add_argument("-r", "--repetition", help="How many repetition on exception")
    args, unknown_argument = parser.parse_known_args()
    if args.username is not None:
        user_data['username'] = args.username
    else:
        print "Username is required.\n"
        parser.print_help()
        exit(1)
    if args.password is not None:
        user_data['password'] = args.password
    else:
        print "Password is required.\n"
        parser.print_help()
        exit(1)
    if args.eu:
        user_data['base_url'] = 'https://www.planet-lab.eu/'
    if args.file_path:
        if os.path.isdir(args.file_path):
            user_data['save_path'] = args.file_path
        else:
            print "Directory doesn't exist. I will create it for you."
            try:
                os.makedirs(args.file_path)
            except OSError:
                if not os.path.isdir(args.file_path):
                    raise
    if args.id_start:
        user_data['id_host'] = int(args.id_start)
    if args.timeout:
        user_data['timeout'] = int(args.timeout)
    if args.repetition:
        user_data['exception_repetition'] = int(args.repetition)
    if unknown_argument:
        print 'Zadaný chybný argument, očakávam iba argumenty:\n-u Username\n-p Password\n-f Path to file\n-e planet-lab.eu'
        print 'Wrong argument, we are expecting only:\n-u Username\n-p Password\n-f Path to file\n-e planet-lab.eu'


def is_request_ok(response):
    """
    Checking if request status is 200 - OK
    If not display status code and error.
    :param response: response object from session
    """
    if response.status_code == requests.codes.ok:
        pass
    else:
        print response.status_code, 'Request faild, try it againg.'


def log_in():
    """
    Log in to PlanetLab and create list of all PlanetLab hosts.
    """
    sess = requests.Session()  # session stores PHPSESSID between requests
    # make login request
    login_data = {
        "edit[form_id]": "planetlab_login_block",
        "edit[name]": user_data['username'],
        "edit[pass]": user_data['password'],
        "op": "Log in"
    }
    # Login to PlanetLab
    res = sess.post(urljoin(user_data['base_url'], "node?destination=node"), data=login_data)
    is_request_ok(res)
    return sess


def get_continent(country):
    """
    Determine on witch continent is country located.
    :param country: Short name od country
    :return: continent where county is located
    """
    for continent, val in continents.iteritems():
        for names, lists in val.iteritems():
            if names == 'countries':
                if country in lists:
                    return continent


def request_table_of_nodes(sess):
    """
    Request for table of all nodes in planet-lab.
    :param sess: Web session
    :return: DNS names of all hosts
    """
    print "Collecting list of all Planet-lab nodes, it can take few minutes..."
    try:
        with closing(sess.get(urljoin(user_data['base_url'], "db/nodes/index.php"))) as r:
            get = r
    except ConnectionError:
        time.sleep(1)
        with closing(sess.get(urljoin(user_data['base_url'], "db/nodes/index.php"))) as r:
            get = r
    is_request_ok(get)
    try:
        # Parse HTML
        soup = BeautifulSoup(get.text, "html.parser")
        # Find the table with hosts
        table = soup.find(lambda tag: tag.name == 'tbody')
        # Find first row
        rows = table.findAll(lambda tag: tag.name == 'tr')
        return rows
    except:
        print "I'm unable to connect, try it later"
        exit(1)


def find_continent(actual, latitude, longitude):
    continent_from_dns = actual.split('.')[-1]
    latitude = float(latitude)
    longitude = float(longitude)
    for difference in [0.5, 1, 2, 3]:
        g1 = geocoder.google([float(latitude) + difference, longitude], method='reverse')
        g2 = geocoder.google([latitude - difference, longitude], method='reverse')
        g3 = geocoder.google([latitude, longitude + difference], method='reverse')
        g4 = geocoder.google([latitude, longitude - difference], method='reverse')
        country_list = [i.country for i in [g1, g2, g3, g4] if i.country and not i.error]
    if len(set(country_list)) == 0:
        g_errors = [i.error for i in [g1, g2, g3, g4] if i.error]
        if len(set(g_errors)) == 1:
            if g_errors[0] == u'OVER_QUERY_LIMIT':
                print "Goecoder limit for today was exceeded."
        return None
    if len(set(country_list)) == 1:
        if continent_from_dns.upper() == country_list[0].upper():
            continent = get_continent(country_list[0])
            return continent
        else:
            print "Country domain of node:", actual, "it's not same as country from geocoder:", country_list[0]
            return None
    else:
        print "Geocoder gave me more than one country", country_list
        return None


def parse_all_date(sess, links):
    """
    Parse information about host from web. It will get DNS name, IP address, Name of institution, latitude, longitude.
    GPS location is translated by geocoder to address.
    :param sess: Web session
    :param links: Object with information about host
    :return:
    """
    try:
        exception = False
        # Take only all hosts
        all_hosts = links.find(lambda tag: tag.name == 'td' and tag.has_attr('class'))
        if all_hosts is not None:
            # Link to this host
            link = links.find(lambda tag: tag.name == 'a' and tag.has_attr('href'))
            # Take only PLE hosts
            ple = links.find(lambda tag: tag.name == 'td' and tag.has_attr('class') and tag['class'][0] == 'peer-ple')
            if ple:
                # If host is not in list
                if link.get_text() not in list_of_planetlab_hosts:
                    pass
                else:
                    return
            # Go to host
            with closing(sess.get(urljoin(user_data['base_url'], link['href']))) as r:
                get_ple = r
            is_request_ok(get_ple)
            # Parse web
            get_ple_soup = BeautifulSoup(get_ple.text, "html.parser")
            # Find the table plc_details
            sites = get_ple_soup.find(lambda tag: tag.name == 'table' and tag.has_attr('class') and
                                                  tag['class'][0] == 'plc_details')
            # Find all links
            all_links = sites.findAll(lambda tag: tag.name == 'a' and tag.has_attr('href'))
            actual_nodes = {}
            for some_link in all_links:
                # Store information about sites
                if re.match('.*/sites/.*', some_link['href']) is not None:
                    if some_link['href'] == re.match('.*/sites/.*', some_link['href']).string:
                        site_link = some_link.get('href')
                        site_name = some_link.get_text()
                if ple:
                    # Store information about nodes
                    if re.match('.*/nodes/.*', some_link['href']) is not None:
                        if some_link['href'] == re.match('.*/nodes/.*', some_link['href']).string:
                            list_of_planetlab_hosts.append(some_link.get_text())
                            actual_nodes[some_link.get_text()] = ''
                else:
                    actual_nodes[link.get_text()] = ''
                    list_of_planetlab_hosts.append(some_link.get_text())
            node_interfaces = get_ple_soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and
                                                            tag['id'] == 'node_interfaces')
            plc_ip = None
            if node_interfaces:
                plc_ip_table = node_interfaces.findAll(lambda tag: tag.name == 'a' and tag.has_attr('href'))
                plc_ip = plc_ip_table[0].get_text()
            # Get source code of site website
            with closing(sess.get(urljoin(user_data['base_url'], site_link))) as r:
                get_site = r
            # Parse site website
            get_site_soup = BeautifulSoup(get_site.text, "html.parser")
            # print get_site_soup
            site = get_site_soup.find(lambda tag: tag.name == 'table' and tag.has_attr('class') and
                                                  tag['class'][0] == 'plc_details')
            info = site.findAll(lambda tag: tag.name == 'tr')
            for part_of_info in info:
                if part_of_info.find(lambda tag: tag.name == 'th') is not None:
                    th = part_of_info.find(lambda tag: tag.name == 'th').get_text()
                    td = part_of_info.find(lambda tag: tag.name == 'td').get_text()
                    if th == 'Full name':
                        full_name = td
                        if full_name == '':
                            full_name = site_name
                    if th == 'URL':
                        url = td
                        if url == '':
                            url = 'unknown'
                    if th == 'Latitude':
                        latitude = td
                    if th == 'Longitude':
                        longitude = td
            if (latitude and longitude) == '':
                latitude = None
                longitude = None
                country = None
                city = None
                region = None
                continent = None
            else:
                g = geocoder.google([latitude, longitude], method='reverse')
                if g.error == u'OVER_QUERY_LIMIT':
                    print "Goecoder limit for today was exceeded."
                country = g.country
                city = g.city
                region = g.county
                # continent
                continent = None
                continent = get_continent(country)
            for actual in actual_nodes:
                print 'Currently working on id: 0' + str(user_data['id_host']) + ', host:', actual
                flag = None
                if continent is None:
                    if latitude is not None:
                        continent = find_continent(actual, latitude, longitude)
                try:
                    ip = socket.gethostbyname(actual)
                except socket.gaierror:
                    ip = 'unknown'
                    flag = 'noIpFromDns'
                if plc_ip:
                    if ip != plc_ip:
                        print 'IP address from planet-lab website is different from DNS translation for host: {}'.format(
                            actual)
                        print 'IP from web: {}, IP from DNS translation: {}'.format(plc_ip, ip)
                        # write to file ip from web
                        flag = 'diffIpFromDns'
                        if ip == 'unknown':
                            flag = 'noIpFromDns'
                        ip = plc_ip
                    else:
                        flag = 'identicalIP'
                if user_data['save_path'] == '':
                    user_data['save_path'] = os.path.dirname(os.path.abspath(__file__))
                with codecs.open(os.path.join(user_data['save_path'], 'planetlab_' + actual_time + '.node'),
                                 mode='a', encoding='utf-8') as f:
                    if user_data['first'] is True:
                        f.write(u"{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('# ID', 'IP', 'DNS',
                                                                                           'continent', 'country',
                                                                                           'region', 'city', 'url',
                                                                                           'full_name', 'latitude',
                                                                                           'longitude',
                                                                                           'flag if web IP is different from DNS translation'))
                        user_data['first'] = False
                    if ip is None:
                        ip = 'unknown'
                    if actual is None:
                        actual = 'unknown'
                    if continent is None:
                        continent = 'unknown'
                    if country is None:
                        country = 'unknown'
                    if region is None:
                        region = 'unknown'
                    if city is None:
                        city = 'unknown'
                    if url is None:
                        url = 'unknown'
                    if full_name is None:
                        full_name = 'unknown'
                    if latitude is None:
                        latitude = 'unknown'
                    if longitude is None:
                        longitude = 'unknown'
                    if flag is None:
                        flag = 'unknown'
                    f.write(
                        u"{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format('0' + str(user_data['id_host']),
                                                                                   ip, actual, continent, country,
                                                                                   region, city, url, full_name,
                                                                                   latitude, longitude, flag))
                    user_data['id_host'] += 1
            return
    except (KeyboardInterrupt, SystemExit):
        print "Program was stopped by user."
        exit(1)
    except Exception, e:
        print 'Exception has occurred, program will wait {}sec and continue, please wait.'.format(user_data['timeout'])
        print e
        exception = True
        time.sleep(user_data['timeout'])
        return
    finally:
        if exception is True:
            user_data['exception_occurred'] += 1
            if user_data['exception_occurred'] >= user_data['exception_repetition']:
                print "Could't get information for host: ", links.find(lambda tag: tag.name == 'a' and
                                                                                   tag.has_attr('href')).get_text()
                return
            parse_all_date(sess, links)


def collect_data(sess):
    """
    Main function for parsing data.
    :param sess: Web sestion
    """
    # Go to Nodes
    rows = request_table_of_nodes(sess)
    print "There is", len(rows), "hosts to process."
    # For columns in row
    start = 0
    for links in rows[start:]:
        user_data['exception_occurred'] = 0
        parse_all_date(sess, links)


if __name__ == "__main__":
    parse_arguments()
    print 'Program started.'
    actual_time = datetime.datetime.now().strftime("%d-%m-%y_%H-%M")
    collect_data(log_in())
    # copy file planetlab_actial_time.node to planetlab.node
    copyfile(os.path.join(user_data['save_path'], 'planetlab_' + actual_time + '.node'),
             os.path.join(user_data['save_path'], 'planetlab.node'))
    print 'Finished.'
