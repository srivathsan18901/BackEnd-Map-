from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from google.oauth2 import google
from google.auth.transport import requests
from googleapiclient.discovery import build

class GoogleCalendarInitView(APIView):
    def get(self, request):
        flow = google.OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
        )
        auth_url = flow.step1_get_authorize_url()
        return HttpResponseRedirect(auth_url)

class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        flow = google.OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            redirect_uri=request.build_absolute_uri(reverse('google-calendar-redirect'))
        )
        code = request.GET.get('code')
        credentials = flow.step2_exchange(code)
        access_token = credentials.access_token

        # Use the access_token to retrieve events from the user's calendar
        service = build('calendar', 'v3', credentials=credentials)
        events = service.events().list(calendarId='primary').execute()
        # Process the events as per your requirement
        ...

        return Response({'events': events})
