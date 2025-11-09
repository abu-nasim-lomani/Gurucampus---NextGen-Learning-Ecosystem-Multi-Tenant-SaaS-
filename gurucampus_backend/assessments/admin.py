# assessments/admin.py
from django.contrib import admin
from .models import (
        Assessment, 
        Problem, 
        TestCase, 
        Submission, 
        QuizQuestion, 
        QuizAttempt
    ) # <-- TestCase, Submission ইম্পোর্ট করুন

# --- এটি একটি নতুন ইনলাইন ---
class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1 # ডিফল্টভাবে ১টি নতুন টেস্ট কেস যোগ করার স্লট

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'assessment')
    list_filter = ('assessment',)
    inlines = [TestCaseInline] # <-- Problem পেজের ভেতরে TestCase যোগ করার সুবিধা
# ------------------------------

class ProblemInline(admin.TabularInline):
    model = Problem
    extra = 1 

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    inlines = [ProblemInline]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('problem', 'student', 'status', 'timestamp')
    list_filter = ('status', 'problem__assessment__course')
    readonly_fields = ('output',) # Judge0-এর আউটপুট শুধু দেখা যাবে, এডিট করা যাবে না
    
    
    
@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'assessment', 'question_type')
    list_filter = ('assessment', 'question_type')
    search_fields = ('question_text',)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'selected_answer', 'is_correct')
    list_filter = ('is_correct', 'question__assessment')
    search_fields = ('student__username', 'question__question_text')