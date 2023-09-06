from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

# Create a UserUpdateForm to update a user profile
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email']

BRICK_STAGES = (
    ("1", "Brick Drafting"),
    ("2", "SME Review"),
    ("3", "Editor Review"),
    ("4", "Ready For Insert"),
    ("5", "Complete"),
)

EXT_CHOICES =(
    ("1", "All"),
    ("2", "docx"),
    ("3", "png"),
    ("4", "jpg"),
)

class SearchForm(forms.Form):
    extensions = forms.MultipleChoiceField(required=False, choices=EXT_CHOICES)
    sDateModified = forms.DateField(required=False)
    eDateModified = forms.DateField(required=False)
    wordCountMin = forms.IntegerField(required=False)
    wordCountMax = forms.IntegerField(required=False)
    terms = forms.CharField(required=False, max_length=100)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['terms'].label = "Search Terms"
        self.fields['sDateModified'].label = "Date Modified (Start)"
        self.fields['eDateModified'].label = "Date Modified (End)"
        self.fields['wordCountMin'].label = "Word Count Min"
        self.fields['wordCountMax'].label = "Word Count Max"
        self.fields['extensions'].label = "File Extensions"

