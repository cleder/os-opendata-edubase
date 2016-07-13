# -*- coding: utf-8 -*-

from django import forms

from .models import SiteComment

class SiteCommentForm(forms.ModelForm):

    class Meta:
        model = SiteComment
        fields = ['flag', 'comment']
        widgets = {'flag': forms.RadioSelect}
