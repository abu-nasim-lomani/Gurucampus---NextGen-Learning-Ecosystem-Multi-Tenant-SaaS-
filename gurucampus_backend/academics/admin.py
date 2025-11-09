# academics/admin.py
from django.contrib import admin
from .models import Department, Batch, Semester, Class, ClassroomMember

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

# 'Class' মডেলটি এখানে একবারই রেজিস্টার করা হয়েছে
@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'teacher', 'invite_code')
    list_filter = ('batch', 'semester', 'teacher')

# 'ClassroomMember' মডেলটি এখানে রেজিস্টার করা হয়েছে
@admin.register(ClassroomMember)
class ClassroomMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'classroom', 'role', 'status')
    list_filter = ('classroom', 'role', 'status')
    list_editable = ('status', 'role')