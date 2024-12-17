from flask import Flask, Blueprint, session, url_for, redirect, request
import google_auth_oauthlib.flow
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import google.oauth2.credentials
from googleapiclient.discovery import build
import logging
import json
logging.basicConfig(level=logging.DEBUG)
SAMPLE_SPREADSHEET_ID = "1Q3w-UW3jlXMKMgNaFjdrLVV2PPAuWf-DJ9dZjxuX81A"
SAMPLE_RANGE_NAME = "ชีท1!A1:F7"
oauth_bp = Blueprint('oauth_bp', __name__)

CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['openid',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/contacts.readonly',
          'https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/spreadsheets.readonly']

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'granted_scopes': credentials.granted_scopes}

@oauth_bp.route('/clear')
def clear_credentials():
  if 'credentials' in session:
    del session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())

@oauth_bp.route('/')
def index():
  return print_index_table()

@oauth_bp.route('/authorize')
def authorize():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth_bp.oauth2callback', _external=True)
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent')
    
    session['state'] = state

    return redirect(authorization_url)

@oauth_bp.route('/oauth2callback')
def oauth2callback():
    state = session['state']

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth_bp.oauth2callback', _external=True)

    authorization_response = request.url
  
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    
    credentials = credentials_to_dict(credentials)
    session['credentials'] = credentials
    
    with open("token.json", "w") as token:
            token.write(json.dumps(credentials))

#   features = check_granted_scopes(credentials)
#   oauth_bp.session['features'] = features
  
    return redirect('/')

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