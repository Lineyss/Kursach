from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django import forms
from .models import *

class TegForm(forms.ModelForm):
    class Meta:
        model = Teg
        fields = ['Title', 'Color', 'IDUser']
        widgets = {
            'Color': forms.TextInput(attrs={'type': 'color'}),
        }

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = UserSite
        fields = ('username', 'password1', 'password2')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

class SingUp(CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/reg.html"

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = UserSite
        fields = ['username']
    
    def clean_username(self):
        new_username = self.cleaned_data['username']
        if UserSite.objects.filter(username=new_username).exists():
            raise ValidationError("Such a name already exists")

        return new_username

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['IDFolder', 'File', 'Owner']

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['IDFolder', 'Title', 'Owner']

class AddAction(forms.Form):
    selected_options = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(content_type__model='Folder'),
        widget=forms.CheckboxSelectMultiple, 
    )

    file_folder_id = forms.IntegerField(
        widget=forms.HiddenInput(),
    )

    def clean_file_folder_id(self):
        id = self.cleaned_data['file_folder_id']
        try:
            self.file_folder = FileFolder.objects.get(id=id)
        except:
            raise ValidationError('Объекта с таким id не существует')
        
        return id

    def save(self):
        selected_perms = self.cleaned_data['selected_options']
        perms = ''

        for perm in selected_perms:
            perms += f'{perm.name};'

        shared = SharedURI(IDSender=self.user,
                Premissions = perms,
                IDFileFolder=self.id)
        
        shared.save()

        return shared