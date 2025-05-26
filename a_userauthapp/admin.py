# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Voter_User, College, Department, Profile

@admin.register(Voter_User)
class VoterUserAdmin(UserAdmin):
    model = Voter_User

    list_display = ('username', 'college', 'department', 'is_active', 'is_staff', 'is_student', 'is_superuser')
    list_editable = ('college', 'department', 'is_active', 'is_staff', 'is_student', 'is_superuser')  # <- make them editable here
    list_filter = ('is_active', 'is_staff', 'college', 'department', 'gender')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'location')}),
        ('Academic Info', {'fields': ('college', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'college', 'department')}
        ),
    )

    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

# Register College and Department normally
admin.site.register(Profile)
admin.site.register(College)
admin.site.register(Department)




