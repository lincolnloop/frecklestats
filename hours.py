#!/usr/bin/env python

import requests
import json
from os import path, environ
from bottle import Bottle, template, static_file, request
from bottle.ext import memcache

# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

try:
    FRECKLE_USER_ID = environ['FRECKLE_USER_ID']
    FRECKLE_API_KEY = environ['FRECKLE_API_KEY']
    FRECKLE_HOST = environ['FRECKLE_HOST']
except KeyError:
    print '''
-----------------------------------------------------
Freckle credentials not found in os.environ. Put them
in your .profile or .bash_rc:

export FRECKLE_USER_ID=12345
export FRECKLE_API_KEY=abcdefghijklmnopqrstuvwxyz
export FRECKLE_HOST=mycompany
-----------------------------------------------------
'''
    raise RuntimeError('Freckle credentials not configured')


WEEKLY_GOAL = 30

FRECKLE__HOURS_URL = 'https://{host}.letsfreckle.com/api/entries.json?' \
                     '&search[people]={id}&search[from]={start}'.format(
                         host=FRECKLE_HOST, id=FRECKLE_USER_ID, start='2013-07-01')
FRECKLE_PROJECTS_URL = 'https://{host}.letsfreckle.com/api/projects.json'.format(
                          host=FRECKLE_HOST)

STATIC_DIR = path.join(path.dirname(__file__), 'static')

CACHE_KEY_PROJ = 'hours_{}_projects'.format(FRECKLE_USER_ID)
CACHE_KEY_DATA = 'hours_{}_data'.format(FRECKLE_USER_ID)

# -----------------------------------------------------------------------------
# Code
# -----------------------------------------------------------------------------

def get_data(mc):
    projects = mc.get(CACHE_KEY_PROJ)
    hours = mc.get(CACHE_KEY_DATA)

    if projects and hours and not 'force' in request.GET:
        print('*** Using cached data')
        return projects, hours

    headers = {'X-FreckleToken': FRECKLE_API_KEY}

    # Fetch the project list and collect its id:name
    projects = json.loads(requests.get(FRECKLE_PROJECTS_URL, headers=headers).content)
    project_list = {}
    for p in projects:
        project_list[p['project']['id']] = p['project']['name']

    """
    Convert this:

    {
        u'entry': {
            u'import_id': None,
            u'formatted_description':
            u'#internal-communication',
            u'user_id': 13524,
            u'description': u'internal-communication, !#internal-communication',
            u'tags': [{u'id': 381468, u'name': u'internal-communication', u'billable': True}],
            u'url': None, u'invoice_id': None,
            u'created_at': u'2013-09-10T10:56:19Z',
            u'time_from': None,
            u'updated_at': u'2013-09-10T10:56:19Z',
            u'money_status': None,
            u'description_text': u'#internal-communication',
            u'invoiced_at': None,
            u'billable': False,
            u'date': u'2013-09-10',
            u'time_to': None,
            u'project_id': 44691,
            u'minutes': 45,
            u'id': 4558115,
            u'billable_status': None,
            u'recently_updated_at': u'2013-09-10T10:56:19Z'
        }
    }
    """

    # Load all hours. This is likey paginated so look recursive through it
    hour_list = []

    def _get_hours(response, page=1):
        print 'Parsing page {}'.format(page)

        hours = json.loads(response.content)

        for h in hours:
            h = h['entry']
            hour_list.append({
                'datetime': h['created_at'],
                'minutes': h['minutes'],
                'project': project_list[h['project_id']]
            })

        # Iterate over paginated hours
        if 'link' in response.headers:
            page += 1
            link = response.headers['link'][1:response.headers['link'].find(';')-1]
            _get_hours(requests.get(link, headers=headers), page=page)

    _get_hours(requests.get(FRECKLE__HOURS_URL, headers=headers))

    mc.set(CACHE_KEY_PROJ, project_list)
    mc.set(CACHE_KEY_DATA, hour_list)

    return project_list, hour_list


# -----------------------------------------------------------------------------
# App
# -----------------------------------------------------------------------------

app = Bottle()
app.install(memcache.MemcachePlugin(servers=['localhost:11211']))

@app.route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_DIR)

@app.route('/')
def index(mc):
    projects, hours = get_data(mc)
    return template('hours',
        projects=projects,
        hours=hours,
        last_update='',
    )

app.run(host='localhost', port=8080)
