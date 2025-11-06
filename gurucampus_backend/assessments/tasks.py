# assessments/tasks.py
from celery import shared_task
from django_tenants.utils import schema_context
from .models import Submission, TestCase

# We use time.sleep() to simulate the grading process being slow
import time

@shared_task
def grade_submission(submission_id, schema_name):
    """
    A Celery task to grade a code submission.
    This runs in the background.
    """
    
    # IMPORTANT: We must switch to the correct tenant's schema
    # where this submission exists.
    with schema_context(schema_name):
        try:
            # 1. Get the submission
            submission = Submission.objects.get(id=submission_id)
            submission.status = 'Processing'
            submission.save()

            # 2. Get the problem's hidden test cases
            problem = submission.problem
            testcases = TestCase.objects.filter(problem=problem, is_hidden=True)

            # 3. Simulate the grading process (the "heavy" part)
            # This is where we will call Judge0 in the future.
            # For now, we'll just check if "Hello, World!" is in the code.
            time.sleep(5) # Simulate a 5-second grading process

            is_correct = "Hello, World!" in submission.submitted_code
            
            # 4. Update the submission status
            if is_correct:
                submission.status = 'Accepted'
                submission.output = "All test cases passed!"
            else:
                submission.status = 'Wrong Answer'
                submission.output = "Test case 1 failed."
            
            submission.save()

        except Submission.DoesNotExist:
            # Handle the case where the submission might have been deleted
            print(f"Submission {submission_id} not found in schema {schema_name}")

    return f"Grading complete for Submission {submission_id} in {schema_name}"