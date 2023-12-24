from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=4)

class UserRegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput,  min_length=4)
    confirm_password = forms.CharField(label='Repeat password', widget=forms.PasswordInput,  min_length=4)

class UserSettingsForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', required=False)
    bio = forms.CharField(label='Bio', widget=forms.Textarea)
    avatar = forms.ImageField(label='Avatar', required=False)
    
