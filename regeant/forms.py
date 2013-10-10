#-*- coding: utf-8 -*-


from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'id': 'searchinput'
            }))
