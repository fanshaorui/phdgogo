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
    #site_url = forms.CharField(
     #   widget=forms.URLField(
      #      initial='http://'))
    email = forms.CharField(widget=forms.EmailField())


class ProviderRegisterForm(forms.Form):
    ''' ProviderRegisterForm
        @author kid143
        @version 0.0.1
        @since 1.0
    '''

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'用户名'}),
        required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'密码'}),
        required=True)
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'重复密码'}),
        required=True)
    provider_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder':'公司名称'}),
        required=True)
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'邮箱','type':'text'}))
    phonenumber=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'电话号码','type':'text'}))
    qqnumber=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'QQ号','type':'text'}))
    def clean_repeatpassword(self):
		if self.cleaned_data['password']==self.cleaned_data['repeat_password']:
			return self.cleaned_data['repeat_password']
		else:
			raise  forms.ValidationError(u"密码输入不一样,请重新输入")
class ProviderInfoForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'密码'}),
        required=True)
    repeat_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'重复密码'}),
        required=True)
    provider_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder':'公司名称'}),
        required=True)
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'邮箱','type':'text'}))
    phonenumber=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'电话号码','type':'text'}))
    qqnumber=forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'QQ号','type':'text'}))
    def clean_repeatpassword(self):
		if self.cleaned_data['password']==self.cleaned_data['repeat_password']:
			return self.cleaned_data['repeat_password']
		else:
			raise  forms.ValidationError(u"密码输入不一样,请重新输入")

class ProviderLoginForm(forms.Form):
	username=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder':'用户名'}))
	password=forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'placeholder':'密码'}))

