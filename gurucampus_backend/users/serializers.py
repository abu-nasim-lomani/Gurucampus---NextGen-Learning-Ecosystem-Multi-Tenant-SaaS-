# users/serializers.py
from rest_framework import serializers
from .models import CustomUser
from academics.models import Class, ClassroomMember
from django.db import transaction # পারমাণবিক (Atomic) লেনদেনের জন্য

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for our CustomUser model.
    Used to display user info in other APIs (like the "Waiting Room").
    """
    class Meta:
        model = CustomUser
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'student_id' 
        ]

# --- এই নতুন সিরিয়ালাইজারটি নিচে যোগ করুন ---

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Handles B2B student registration via invite code.
    Validates user data, creates a CustomUser, finds the Class via
    invite_code, and creates a 'Pending' ClassroomMember entry.
    """
    
    # আপনার প্রস্তাবিত ফিল্ডগুলো
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    invite_code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'first_name', 
            'last_name', 
            'password', 
            'password2',
            'student_id',  # আপনার ভেরিফিকেশন ফিল্ড
            'phone',
            'date_of_birth',
            'invite_code'  # ইনভাইট লিংক থেকে আসবে
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        Validate passwords match and invite code is valid.
        """
        # ১. পাসওয়ার্ড চেক
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        
        # ২. ইনভাইট কোড চেক
        try:
            Class.objects.get(invite_code=data['invite_code'])
        except Class.DoesNotExist:
            raise serializers.ValidationError({"invite_code": "Invalid invite code."})
            
        return data

    def create(self, validated_data):
        """
        Create the User and the Pending ClassroomMember in a transaction.
        """
        invite_code = validated_data.pop('invite_code')
        validated_data.pop('password2') # এটি আমাদের আর দরকার নেই
        
        # 'email'-কে 'username' হিসেবেও সেট করছি
        validated_data['username'] = validated_data['email']
        
        try:
            # --- "ওয়ার্ল্ড-ক্লাস" ফ্লো: ধাপ ১ ---
            # এটি নিশ্চিত করে যে দুটি কাজই একসাথে হবে, নতুবা কিছুই হবে না
            with transaction.atomic():
                # ১. ইউজার তৈরি করুন
                user = CustomUser.objects.create_user(**validated_data)
                
                # --- "ওয়ার্ল্ড-ক্লাস" ফ্লো: ধাপ ২ ---
                # ২. ইনভাইট কোড দিয়ে ক্লাসটি খুঁজুন
                classroom = Class.objects.get(invite_code=invite_code)
                
                # ৩. ছাত্রকে "লবি"-তে পাঠান (Pending Status)
                ClassroomMember.objects.create(
                    user=user,
                    classroom=classroom,
                    role=ClassroomMember.ROLE_STUDENT,
                    status=ClassroomMember.STATUS_PENDING
                )
                
                return user
                
        except Exception as e:
            # যদি কোনো কারণে ইউজার তৈরি হলেও ক্লাস মেম্বার তৈরি না হয়
            raise serializers.ValidationError(f"An error occurred during registration: {str(e)}")