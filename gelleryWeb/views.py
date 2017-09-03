from django.shortcuts import render
from.import models


# Home page views
def index(request):
    # Return some artwork list in the home page
    artworks = models.ArtWork.objects.all()
    return render(request, 'home/index.html', {'artworks': artworks})



