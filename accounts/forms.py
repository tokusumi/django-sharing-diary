from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = UserCreationForm.Meta.fields + ('email', 'birth_date','location',) #add your custom field
