from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control




    
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url="/login/")
def notes (request):
    userNotes = [{'date_added':'12-10-2023','title':'Meetings','content':'Attend the marketing team meeting at 10 AM.Prepare the presentation slides for the project review meeting.'},
                 {'date_added':'14-10-2023','title':'Ideas for Vacation','content':'Plan a romantic weekend getaway or a surprise dinner date'},
                 {'date_added':'15-10-2023','title':'Gift Ideas','content':'Look for a unique kitchen gadget or a personalized photo frame.'},
                 {'date_added':'12-10-2023','title':'Kitchen renovation','content':'Consider factors like budget, weather, and available activities.'},
                 {'date_added':'19-5-2023','title':'Accommodation','content':'Research deck designs and materials suitable'}]
    return render(request, 'notes/notes.html',{'userNotes':userNotes})
