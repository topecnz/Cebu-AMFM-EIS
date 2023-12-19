from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    
class AddAccountForm(forms.Form):
    fname = forms.CharField()
    lname = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    cpassword = forms.CharField()
