from django.db import models

class Update(models.Model):
    """
    An update is a small bit of text used to share info like a new version

    If a version exists, this is a "New Version" update.
    """
    
    title = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, null=False)
    published = models.DateTimeField(blank=False, null=False)
    body = models.TextField(u'Update Body', blank=True, null=True)
    version = models.DecimalField(max_digits=10, decimal_places=1, default=None, blank=True, null=True)
    
    @models.permalink
    def get_absolute_url(self):
        return ('thebus.web.views.update_detail', [str(self.slug)])