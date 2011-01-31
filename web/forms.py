from django import forms

class SearchForm(forms.Form):
    
    """
    This is the standard HTML form for searching for routes, and retrieving a list back.
    """
    
    query = forms.CharField(max_length=100)


class FeedbackForm(forms.Form):
    message = forms.CharField(label='Your Message', help_text='Enter any kind of feedback you\'d like to give TheBus.ws', widget=forms.Textarea)
    email = forms.EmailField(label='Your Email Address', help_text='If you would like a response, you can optionally enter your email address so we can contact you.', required=False)
        