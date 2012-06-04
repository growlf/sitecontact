from django.forms import widgets, Form, CharField, EmailField, TextInput, Textarea, IntegerField, DateField, TimeField, Select
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.localflavor.us.forms import USPhoneNumberField, USStateField, USZipCodeField
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django.template import Template, Context
from form_utils.forms import BetterForm


def sendEMail(self, site_email, body=None, subject=None, replyto=None):
    headers = {}
    
    if not body:
        format = ""
        for key in self.cleaned_data.keys():
            format += "%s: {{ %s }}\n" % (key, key)
        t = Template(format)
        body = t.render(Context(self.cleaned_data))
    
    if not subject:
        subject = 'Website feedback'
        
    if replyto:
        headers['Reply-To'] = replyto
        
    email_message = EmailMessage(
                                subject=subject,
                                body=body,
                                #from_email=site_email,
                                to=[site_email],
                                #connection=connection,
                                headers=headers,
                                #cc=['',]
                                )    

    ret = email_message.send(fail_silently=True)
    print ret


class ContactForm(BetterForm):
    name = CharField()
    email = EmailField()
    phone = USPhoneNumberField()
    company = CharField()
    subject = CharField()
    content	= CharField(widget=Textarea())

    class Meta:
        row_attrs = {
            'name': {'id': 'name',},
            'email': {'id': 'email',},
            'phone': {'id': 'phone',},
            'company': {'id': 'company',},
            'subject': {'id': 'phone',},
            'content': {'id': 'content',},
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs={'placeholder': 'Your name...',}
        self.fields['name'].help_text = " "
        self.fields['email'].widget.attrs={'placeholder': 'Your email...',}
        self.fields['email'].help_text = " "
        self.fields['phone'].widget.attrs={'placeholder': 'Your contact phone number...',}
        self.fields['phone'].help_text = " "
        self.fields['company'].widget.attrs={'placeholder': 'Company name...',}
        self.fields['company'].help_text = " "
        self.fields['subject'].widget.attrs={'placeholder': 'Subject...',}
        self.fields['subject'].help_text = " "
        self.fields['content'].widget.attrs={'placeholder': 'Message...',}
        self.fields['content'].help_text = " "

    def send(self, site_email):
        body = render_to_string("email_feedback.txt", {
                                               'data': self.cleaned_data,
                                               })
        subject = "SITE FEEDBACK: "+self.cleaned_data['subject']
        replyto = self.cleaned_data['email']
        sendEMail(self, site_email, body=body, subject=subject, replyto=replyto)

