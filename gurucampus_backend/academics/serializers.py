# academics/serializers.py
from rest_framework import serializers
from .models import Department, Batch, Semester, Class, ClassroomMember
from users.serializers import UserSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name', 'department', 'start_date', 'end_date']

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active']

class ClassSerializer(serializers.ModelSerializer):
    # We can add more details here later (like teacher name)
    # For now, we just use the IDs for creating/updating
    class Meta:
        model = Class
        fields = [
            'id', 
            'course', 
            'batch', 
            'semester', 
            'teacher', 
            'invite_code'
        ]
        # Make invite_code read-only; we'll generate it automatically
        read_only_fields = ['invite_code']
        
        
class ClassroomMemberSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True) 

    class Meta:
        model = ClassroomMember
        fields = [
            'id', 
            'user', 
            'classroom', 
            'role', 
            'status', 
            'joined_at'
        ]

        read_only_fields = ['user', 'role', 'status', 'joined_at']
        
class ClassroomMemberManageSerializer(serializers.Serializer):
    """
    Serializer for a Teacher to approve or reject a student.
    Validates 'member_id' and 'action'.
    """
    # ClassroomMember (Waiting Room) এন্ট্রির ID
    member_id = serializers.IntegerField()
    
    # টিচার কী করতে চান?
    VALID_ACTIONS = [
        ClassroomMember.STATUS_ACTIVE,   # "Active"
        ClassroomMember.STATUS_REJECTED  # "Rejected"
    ]
    action = serializers.ChoiceField(choices=VALID_ACTIONS)