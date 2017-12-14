from django import forms


class SignupForm(forms.Form):
    """
        Defining form fields for sign up form
    """
    f_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'form-control'}))
    l_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=25, widget=forms.PasswordInput(attrs={'class':'form-control'}))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))


class LoginForm(forms.Form):
    """
        Defining form fields for login form
    """
    email = forms.EmailField(max_length=25, widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=25, widget=forms.PasswordInput(attrs={'class':'form-control'}))

class CommentForm(forms.Form):
    """
        Defining form fields for Comment form
    """
    comment = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 5, 'cols': 12,'class':'form-control'}))

class ProfileForm(forms.Form):
    """
        Defining form fields for editing profile
    """
    f_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    l_name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
