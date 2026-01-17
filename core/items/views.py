from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {
        'title': 'CampusFound | Lost & Found for Students'
    })
    
    
