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

    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput({'class': 'text'}),
        required=True)
    address = forms.CharField(widget=forms.Textarea({'class': 'text'}))
    contact = forms.CharField(widget=forms.Textarea({'class': 'text'}))
    site_url = forms.CharField(
        widget=forms.URLField(
            initial='http://'))
    email = forms.CharField(widget=forms.EmailField())


class ProviderRegisterForm(forms.Form):
    ''' ProviderRegisterForm
        @author kid143
        @version 0.0.1
        @since 1.0
    '''

    username = forms.CharField(
        widget=forms.Textarea({'class': 'text'}),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'text'}),
        required=True)
    provider_name = forms.CharField(
        maxlength=200,
        widget=forms.TextInput({'class': 'text'}),
        required=True)
