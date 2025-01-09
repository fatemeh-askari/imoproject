# # forms.py
# from django import forms
# from .models import Request
#
# class RequestForm(forms.ModelForm):
#     class Meta:
#         model = Request
#         fields = ['name', 'details', 'description']


from django import forms
from .models import Request  # Import your Request model

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['name', 'details']  # Include your actual field names here
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control mb-3'



from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)




from django import forms
from .models import RequestDetail

class RequestDetailForm(forms.ModelForm):
    class Meta:
        model = RequestDetail
        fields = ['detail_spacial']  # فیلدهای فرم
        widgets = {
            'detail_spacial': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': '', 'style': 'width: 100%; margin: 0; padding-left: 5px; background-color:#bff3c3'}),
            'description_spacial': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter special description'}),
        }

