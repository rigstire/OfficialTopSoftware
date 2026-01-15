# sales_application/admin.py
from django.contrib import admin
from .models import SalesApplication
@admin.register(SalesApplication)
class SalesApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'has_worked_sales_before', 
                    'years_of_sales_experience', 'status', 'application_date']
    list_filter = ['status', 'has_worked_sales_before', 'can_relocate', 'application_date']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    readonly_fields = ['application_date', 'last_modified']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'resume')
        }),
        ('Sales Experience', {
            'fields': ('has_worked_sales_before', 'years_of_sales_experience',
                      'is_certified_sales_professional')
        }),
        ('Background', {
            'fields': ('previous_work_experience', 'educational_experience')
        }),
        ('Additional Information', {
            'fields': ('can_relocate', 'has_own_vehicle', 'cover_letter')
        }),
        ('Application Status', {
            'fields': ('status', 'application_date', 'last_modified')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
