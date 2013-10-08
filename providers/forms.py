# -*- coding: utf-8 -*-


from django import forms


class UploadForm(forms.Form):

    """ UploadForm for providers.
        @author kid143
        @version 0.0.1
        @since 1.0
    """

    upload_file = forms.FileField()


class ProviderInfoForm(forms.Form):

    ''' ProviderInfoForm
        @author kid143
        @version 0.0.1
        @since 1.0
    '''

    name = forms.CharField(max_length=200, widget=forms.TextInput({'class': 'text'}), required=True)
    address = forms.CharField(widget=forms.Textarea({'class': 'text'}))
    contact = forms.CharField(widget=forms.Textarea({'class': 'text'}))
    site_url = forms.CharField(widget=forms.URLField(initial='http://', class='text'))
    email = forms.CharField(widget=forms.EmailField(class='text'))

