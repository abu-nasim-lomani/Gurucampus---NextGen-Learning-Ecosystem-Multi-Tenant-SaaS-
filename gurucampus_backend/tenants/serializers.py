# tenants/serializers.py
from rest_framework import serializers
from .models import Organization, Domain
from django_tenants.utils import schema_context  # <-- এটি ঠিক ছিল

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain'] # ইউজারের কাছ থেকে শুধু ডোমেইন নামটি নেব

class OrganizationSerializer(serializers.ModelSerializer):
    # 'domains' ফিল্ডটি ডোমেইন অবজেক্টের একটি লিস্ট হিসেবে ডেটা নেবে
    domains = DomainSerializer(many=True, required=True)

    class Meta:
        model = Organization
        fields = [
            'name', 
            'schema_name', 
            'user_limit', 
            'domains'
        ]

    def create(self, validated_data):
        # ১. প্রথমে 'domains'-এর ডেটা আলাদা করে ফেলি
        domains_data = validated_data.pop('domains')
        
        # --- এটি হলো ফিক্স ---
        # Organization এবং Domain উভয়ই SHARED_APPS (public স্কিমা) এর অংশ।
        # তাই এগুলো তৈরি করার আগে 'public' স্কিমাতে স্যুইচ করতে হবে।
        with schema_context('public'):
            # ২. 'Organization' (টেন্যান্ট) তৈরি করি
            organization = Organization.objects.create(**validated_data)

            # ৩. এখন এই নতুন Organization-এর জন্য Domain(s) তৈরি করি
            for domain_data in domains_data:
                Domain.objects.create(
                    tenant=organization,
                    **domain_data
                )
        # --- ফিক্স শেষ ---
        
        return organization