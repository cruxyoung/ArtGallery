from django.shortcuts import render, redirect
from ArtGallery import models
import datetime


# add complaints
def edit_complaints(request, artwork_id):
    artwork = models.ArtWork.objects.get(pk=artwork_id)
    artist_id = artwork.artist_id_id
    artist = models.User.objects.get(pk=artist_id)
    # judge if this customer has complained this artwork, they  only can complain it one time
    for complaint in models.Complaint.objects.all():
        if complaint.aw_id_id == int(artwork_id):
            if complaint.customer_id_id == 6:
                return render(request, 'complaint/art_info.html', {'warning': 'You have complained this artwork!'})
    # complaint = models.Complaint.objects.get(customer_id_id=6, aw_id_id=artwork_id)
    # if complaint:
    #     return render(request, 'complaint/art_info.html', {'warning': 'You have complained this artwork!'})
    return render(request, 'complaint/complaint_page.html', {'artwork': artwork, 'artist': artist})


# fake art_info page
def art_info(request):
    return render(request, 'complaint/art_info.html')


def complaints_action(request):
    aw_id = request.POST.get('artwork_id', '0')
    # not write: fetch session customer_id
    complaint_type = request.POST.get('complaint_type', 'ILLEGAL')
    complaint_content = request.POST.get('complaint_content', 'COMPLAINTS')
    complaint_time = datetime.datetime.now()
    models.Complaint.objects.create(complaint_type=complaint_type, complaint_content=complaint_content,
                                    complaint_time=complaint_time, aw_id_id=aw_id, customer_id_id=6)
    return render(request, 'complaint/art_info.html', {'warning': 'Complained Successfully!'})


def withdraw_complaints(request, artwork_id):
    for complaint in models.Complaint.objects.all():
        if complaint.aw_id_id == int(artwork_id):
            if complaint.customer_id_id == 6:
                models.Complaint.objects.filter(id=complaint.id).delete()
                return render(request, 'complaint/art_info.html', {'warning': 'Withdraw successfully!'})
    return render(request, 'complaint/art_info.html', {'warning': 'You did not complained this artwork before!'})



