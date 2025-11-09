from django.contrib import admin
from .models import Course, Module, Lesson

class LessonInline(admin.TabularInline):
    """
    Allows adding Lessons directly inside the Module admin page.
    """
    model = Lesson
    extra = 1 # Show one empty slot for a new lesson

class ModuleInline(admin.TabularInline):
    """
    Allows adding Modules directly inside the Course admin page.
    """
    model = Module
    extra = 1 # Show one empty slot for a new module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # --- This is the "FINAL UNDO" fix ---
    # We are changing 'organization' back to 'department'
    # to match our correct TENANT_APP model.
    list_display = ('title', 'department', 'price', 'is_b2c_public', 'created_at')
    list_filter = ('department', 'is_b2c_public')
    # ------------------------------------
    
    inlines = [ModuleInline]
    search_fields = ('title',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    inlines = [LessonInline]
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'order')
    list_filter = ('module__course', 'lesson_type')
    search_fields = ('title', 'module__title')