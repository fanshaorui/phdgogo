#-*- coding: utf-8 -*-


from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': u'请输入搜索关键词',
                'style': 'width: 320px;'
            }))
