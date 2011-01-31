from django.contrib.syndication.feeds import *
from thebus.web.models import Update

class UpdateFeed(Feed):
    title = "TheBus.ws"
    link = "/updates/"
    description = "TheBus.ws Updates and Announcements"

    def items(self):
        return Update.objects.order_by('-published')[:10]
        
    def item_pubdate(self, item):
        return item.published