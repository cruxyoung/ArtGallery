from django.contrib.auth.models import User
from .models import UserProfile
from .models import ArtWork
from .models import AuctionRecord
from .models import AuctionHistory
from .models import Reward
from .models import FavoriteRecord
from .models import Complaint
from .models import Comment
from .models import Notification
from django.contrib import admin


admin.site.register(UserProfile)
admin.site.register(ArtWork)
admin.site.register(AuctionHistory)
admin.site.register(AuctionRecord)
admin.site.register(FavoriteRecord)
admin.site.register(Comment)
admin.site.register(Complaint)
admin.site.register(Reward)
admin.site.register(Notification)



