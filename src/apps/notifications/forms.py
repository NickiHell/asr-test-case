from django import forms


class NotificationForm(forms.Form):
    user = forms.CharField(max_length=256)
    text = forms.CharField(widget=forms.Textarea(attrs={'size': '256'}))
