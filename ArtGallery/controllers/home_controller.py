import json
from ..forms import SearchForm
from django.shortcuts import render
from django.http import HttpResponse
from ArtGallery.models import ArtWork
from ArtGallery.models import User
from ArtGallery.models import AuctionRecord
from django.db import transaction


@transaction.atomic
def home_page(request):
    # Newest artworks
    artworks = ArtWork.objects.all()
    if len(artworks) >= 4:
        latest_artworks = artworks.order_by('-aw_time')[len(artworks) - 4:]
        artworks_list_by_awards = artworks.order_by('-aw_totalAward')[len(artworks) - 4:]
    else:
        latest_artworks = artworks.order_by('-aw_time')
        artworks_list_by_awards = artworks.order_by('-aw_totalAward')

    # Get artwork with auction open
    try:
        auction_artwork = AuctionRecord.objects.order_by('-ar_end_time')[0]
    except IndexError:
        auction_artwork = None

    artists = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request,
                  'home_page/index.html',
                  {'artworks': artworks,
                   'latest_artworks': latest_artworks,
                   'aw_by_awards': artworks_list_by_awards,
                   'artists': artists,
                   'auction_aw': auction_artwork,
                   })


@transaction.atomic
# art_list page
def art_list(request):
    if request.method == "POST" and request.is_ajax():
        form = SearchForm(request.POST)
        if form.is_valid():
            keyword = request.POST.get('filter', '')

            artworks = ArtWork.objects.filter(aw_name__contains=keyword)
            if request.POST.get("genre-form"):
                genre = request.POST.get("genre-form")
                if genre != "All":
                    artworks = artworks.filter(aw_genre=genre)
            if request.POST.get('period-form'):
                period = request.POST.get('period-form')
                if period != "All":
                    artworks = artworks.filter(aw_time__year=period)

            artworks = list(artworks.values('id', 'aw_name', 'aw_genre', 'aw_img', 'aw_description', 'aw_location',
                                            'aw_totalAward'))
            return HttpResponse(json.dumps(artworks), content_type='application/json')

    return render(request, 'home_page/art_list.html')
