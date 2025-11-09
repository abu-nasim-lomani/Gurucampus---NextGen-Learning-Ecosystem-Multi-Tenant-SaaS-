# assessments/tasks.py
from celery import shared_task
from django_tenants.utils import schema_context
from .models import Submission, TestCase
from django.conf import settings # API Key-এর জন্য
import requests # Judge0-কে কল করার জন্য
import time

@shared_task
def grade_submission(submission_id, schema_name):
    """
    A Celery task to grade a code submission via Judge0 API.
    This runs in the background.
    """
    
    # --- ধাপ ১: সঠিক টেন্যান্ট স্কিমাতে স্যুইচ করুন ---
    with schema_context(schema_name):
        try:
            submission = Submission.objects.get(id=submission_id)
            problem = submission.problem
            
            # --- ধাপ ২: টাস্ক শুরু হয়েছে বলে চিহ্নিত করুন ---
            submission.status = 'Processing'
            submission.save()

            # --- ধাপ ৩: Judge0-এর জন্য টেস্ট কেস প্রস্তুত করুন ---
            testcases = TestCase.objects.filter(problem=problem)
            if not testcases.exists():
                submission.status = 'Runtime Error'
                submission.output = 'Grading failed: No TestCases found for this problem.'
                submission.save()
                return "Grading failed: No TestCases."

            # Judge0 API-এর জন্য হেডার (আমাদের পাসওয়ার্ড)
            headers = {
                "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com",
                "X-RapidAPI-Key": settings.JUDGE0_API_KEY,
                "content-type": "application/json"
            }

            # Judge0-তে পাঠানোর জন্য সমস্ত টেস্ট কেস প্রস্তুত করুন
            judge0_submissions = []
            for tc in testcases:
                judge0_submissions.append({
                    "language_id": 71,  # 71 হলো Python 3.8
                    "source_code": submission.submitted_code,
                    "stdin": tc.input_data,
                    "expected_output": tc.expected_output
                })

            # --- ধাপ ৪: Judge0-তে কোড সাবমিট করুন (ব্যাচ) ---
            response = requests.post(
                f"{settings.JUDGE0_API_URL}/submissions/batch?base64_encoded=false&wait=true",
                headers=headers,
                json={"submissions": judge0_submissions}
            )
            
            response.raise_for_status() # যদি API এরর দেয় (যেমন 401 - ভুল কী)
            results = response.json()

            # --- ধাপ ৫: Judge0-এর ফলাফল বিশ্লেষণ করুন ---
            final_status = 'Accepted'
            final_output = []

            for i, result in enumerate(results):
                status_description = result.get('status', {}).get('description', 'Error')
                stdout = result.get('stdout', '')
                stderr = result.get('stderr', '')

                # যদি একটিও টেস্ট কেস ফেইল করে, তবে পুরো সাবমিশন ফেইল
                if status_description != 'Accepted':
                    final_status = status_description
                    output = f"--- TestCase {i+1} Failed ---\n"
                    output += f"Status: {status_description}\n"
                    if stderr:
                        output += f"Error: {stderr}\n"
                    else:
                        output += f"Output: {stdout}\n"
                        output += f"Expected: {testcases[i].expected_output}\n"
                    final_output.append(output)
                    break # একটি ফেইল করলেই লুপ ব্রেক করুন
                else:
                    final_output.append(f"--- TestCase {i+1} Passed ---")

            # --- ধাপ ৬: ডাটাবেস আপডেট করুন ---
            submission.status = final_status
            submission.output = "\n".join(final_output)
            submission.save()

        except requests.exceptions.RequestException as e:
            # যদি Judge0 API-তে কল করতে সমস্যা হয়
            submission.status = 'Runtime Error'
            submission.output = f"Judge0 API Error: {str(e)}"
            submission.save()
        except Submission.DoesNotExist:
            print(f"Submission {submission_id} not found in schema {schema_name}")
        except Exception as e:
            # অন্যান্য যেকোনো অপ্রত্যাশিত এরর
            submission.status = 'Runtime Error'
            submission.output = f"An unexpected error occurred: {str(e)}"
            submission.save()

    return f"Grading complete for Submission {submission_id} in {schema_name}"