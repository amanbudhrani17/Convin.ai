from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'GoogleCalendarIntegration/client_secret_637959868969-goepeoark2gir48nupsc5gf4umo67uji.apps.googleusercontent.com.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
            redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect/'
        )

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return HttpResponseRedirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Get the authorization code from the request
        authorization_code = request.GET.get('code')
        flow = InstalledAppFlow.from_client_secrets_file(
            'GoogleCalendarIntegration/client_secret_637959868969-goepeoark2gir48nupsc5gf4umo67uji.apps.googleusercontent.com.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
            redirect_uri='http://127.0.0.1:8000/rest/v1/calendar/redirect/'
        )
        flow.fetch_token(code=authorization_code)
        service = build('calendar', 'v3', credentials=flow.credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])
        return HttpResponse(events)
