# academics/admin.py
from django.contrib import admin
from .models import Department, Batch, Semester, Class

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'start_date')
    list_filter = ('department',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'teacher', 'invite_code')
    list_filter = ('batch', 'semester', 'teacher')