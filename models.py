from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin

class Contact(CMSPlugin):
    site_email = models.EmailField(_('Email recipient address'))
    thanks = models.CharField(_('Message displayed on successful submit'), max_length=200)

    def __unicode__(self):
        return self.site_email

