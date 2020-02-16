from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from django.contrib.auth.forms import UserChangeForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('avatar', 'location', 'birth_date')}),
    )

admin.site.register(MyUser, MyUserAdmin)

# class MyUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username' ,'birth_date' )  # 一覧に出したい項目
#     list_display_links = ('username', 'birth_date')

# admin.site.register(MyUser, MyUserAdmin)
