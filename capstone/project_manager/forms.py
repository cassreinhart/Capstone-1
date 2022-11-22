from django import forms
from django.forms import modelform_factory, ModelForm
from .models import People, User

class NameForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50)
    def save(self):
        pass

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }
    def save(self, commit = True, *args, **kwargs):
        #hash and save pwd in db
        m = super().save(commit=False)
        m.password = make_password(self.cleaned_data.get('password')) #make_password will hash pwd
        m.username = self.cleaned_data.get('username').lower()

        if commit:
            m.save()
        return m #return associated model obj

class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = ['name', 'email', 'title', 'bio', 'avatar_url']