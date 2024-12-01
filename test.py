# -*- coding: utf-8 -*-

import os
import flask
import requests

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "./google_client_secret_977307236610-3r86qn6g6irer7qhfn2q028uf13cabjl.apps.googleusercontent.com.json"

# The OAuth 2.0 access scope allows for access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/webmasters', 'https://www.googleapis.com/auth/indexing']
API_SERVICE_NAME = 'searchconsole'
API_VERSION = 'v1'

INDEXING_API_SERVICE_NAME = 'indexing'
INDEXING_API_VERSION = 'v3'

app = flask.Flask(__name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See https://flask.palletsprojects.com/quickstart/#sessions.

with open('./google_secret_key', 'r') as f:
    app.secret_key = f.read()

@app.route('/')
def index():
  return print_index_table()

@app.route('/drive')
def drive_api_request():
  if 'credentials' not in flask.session:
    return flask.redirect('authorize')

  features = flask.session['features']

  if features['drive']:
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    drive = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    files = drive.files().list().execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**files)
  else:
    # User didn't authorize read-only Drive activity permission.
    # Update UX and application accordingly
    return '<p>Drive feature is not enabled.</p>'

@app.route('/calendar')
def calendar_api_request():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    features = flask.session['features']

    if features['calendar']:
        # User authorized Calendar read permission.
        # Calling the APIs, etc.
        return ('<p>User granted the Google Calendar read permission. '+
                'This sample code does not include code to call Calendar</p>')
    else:
        # User didn't authorize Calendar read permission.
        # Update UX and application accordingly
        return '<p>Calendar feature is not enabled.</p>'

@app.route('/authorize')
def authorize():
  # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)

  # The URI created here must exactly match one of the authorized redirect URIs
  # for the OAuth 2.0 client, which you configured in the API Console. If this
  # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
  # error.
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  
  credentials = credentials_to_dict(credentials)
  flask.session['credentials'] = credentials

  # Check which scopes user granted
  features = check_granted_scopes(credentials)
  flask.session['features'] = features
  return flask.redirect('/')


@app.route('/test')
def test_api_request():
  if 'credentials' not in flask.session:
    return flask.redirect('authorize')

  # Load credentials from the session.
  credentials = google.oauth2.credentials.Credentials(
      **flask.session['credentials'])

  # Retrieve list of properties in account
  search_console_service = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, credentials=credentials)
  site_list = search_console_service.sites().list().execute()

  # Filter for verified URL-prefix websites.
  verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                        if s['permissionLevel'] != 'siteUnverifiedUser'
                        and s['siteUrl'].startswith('http')]

  # Print the sitemaps for all websites that you can access.
  results = '<!DOCTYPE html><html><body><table><tr><th>Verified site</th><th>Sitemaps</th></tr>'
  for site_url in verified_sites_urls:

    # Retrieve list of sitemaps submitted
    sitemaps = search_console_service.sitemaps().list(siteUrl=site_url).execute()
    results += '<tr><td>%s</td>' % (site_url)

    # Add a row with the site and the list of sitemaps
    if 'sitemap' in sitemaps:
      sitemap_list = "<br />".join([s['path'] for s in sitemaps['sitemap']])
    else:
      sitemap_list = "<i>None</i>"
    results += '<td>%s</td></tr>' % (sitemap_list)

  results += '</table></body></html>'

  # Save credentials back to session in case access token was refreshed.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  flask.session['credentials'] = credentials_to_dict(credentials)

  return results
  
@app.route('/index_url', methods=['POST'])
def index_url():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    # Initialize Indexing API
    indexing_service = googleapiclient.discovery.build(
        INDEXING_API_SERVICE_NAME, INDEXING_API_VERSION, credentials=credentials)

    # 요청된 URL 가져오기
    url_to_index = flask.request.form.get('url')
    if not url_to_index:
        return "URL is required", 400

    # 색인 요청 보내기
    body = {
        "url": url_to_index,
        "type": "URL_UPDATED"  # URL_UPDATED or URL_DELETED
    }
    try:
        response = indexing_service.urlNotifications().publish(body=body).execute()
        return flask.jsonify(response)
    except googleapiclient.errors.HttpError as error:
        return f"An error occurred: {error}", 500
    
@app.route('/update_sitemap', methods=['POST'])
def update_sitemap():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    search_console_service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # 사이트맵 URL 가져오기
    sitemap_url = flask.request.form.get('sitemap_url')
    if not sitemap_url:
        return "Sitemap URL is required", 400

    # 사이트맵 제출 요청
    # try:
    response = search_console_service.sitemaps().submit(
        siteUrl='https://inmonim.github.io',
        feedpath=sitemap_url
    ).execute()
    return flask.jsonify(response)
    # except googleapiclient.errors.HttpError as error:
    #     return f"An error occurred: {error}", 500

@app.route('/manage', methods=['GET'])
def manage_urls():
    return '''
        <h1>Google Search Console API</h1>
        <form action="/index_url" method="POST">
            <label for="url">URL to Index:</label>
            <input type="text" id="url" name="url">
            <button type="submit">Request Indexing</button>
        </form>
        <form action="/update_sitemap" method="POST">
            <label for="sitemap_url">Sitemap URL:</label>
            <input type="text" id="sitemap_url" name="sitemap_url" value="https://inmonim.github.io/sitemap.xml">
            <button type="submit">Submit Sitemap</button>
        </form>
    '''

@app.route('/revoke')
def revoke():
  if 'credentials' not in flask.session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' + print_index_table())
  else:
    return('An error occurred.' + print_index_table())

@app.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'granted_scopes': credentials.granted_scopes}

def check_granted_scopes(credentials):
  features = {}
  if 'https://www.googleapis.com/auth/drive.metadata.readonly' in credentials['granted_scopes']:
    features['drive'] = True
  else:
    features['drive'] = False

  if 'https://www.googleapis.com/auth/calendar.readonly' in credentials['granted_scopes']:
    features['calendar'] = True
  else:
    features['calendar'] = False

  return features

def print_index_table():
  return ('<table>' +
          '<tr><td><a href="/test">Test an API request</a></td>' +
          '<td>Submit an API request and see a formatted JSON response. ' +
          '    Go through the authorization flow if there are no stored ' +
          '    credentials for the user.</td></tr>' +
          '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
          '<td>Go directly to the authorization flow. If there are stored ' +
          '    credentials, you still might not be prompted to reauthorize ' +
          '    the application.</td></tr>' +
          '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
          '<td>Revoke the access token associated with the current user ' +
          '    session. After revoking credentials, if you go to the test ' +
          '    page, you should see an <code>invalid_grant</code> error.' +
          '</td></tr>' +
          '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
          '<td>Clear the access token currently stored in the user session. ' +
          '    After clearing the token, if you <a href="/test">test the ' +
          '    API request</a> again, you should go back to the auth flow.' +
          '</td></tr></table>')

if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # This disables the requested scopes and granted scopes check.
  # If users only grant partial request, the warning would not be thrown.
  os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  app.run('localhost', 8080, debug=True)