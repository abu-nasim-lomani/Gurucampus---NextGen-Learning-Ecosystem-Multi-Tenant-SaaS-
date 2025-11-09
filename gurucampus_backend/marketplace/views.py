# marketplace/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import InstructorApplication, InstructorProfile, Order
from .serializers import (
    InstructorApplicationSerializer, 
    InstructorProfileSerializer, 
    OrderSerializer
)

class InstructorApplicationViewSet(viewsets.ModelViewSet):
    """
    "ওয়ার্ল্ড-ক্লাস" ইন্সট্রাক্টর অনবোর্ডিং API।
    - সাধারণ ইউজাররা (ছাত্র) 'create' (POST) ব্যবহার করে আবেদন জমা দেবেন।
    - সুপার অ্যাডমিনরা (আপনি) 'list', 'retrieve', 'update' ব্যবহার করে রিভিউ এবং অনুমোদন (Approve) করবেন।
    """
    queryset = InstructorApplication.objects.all().order_by('-created_at')
    serializer_class = InstructorApplicationSerializer

    def get_permissions(self):
        """
        "ওয়ার্ল্ড-ক্লাস" সিকিউরিটি:
        - যে কেউ (লগইন করা) আবেদন (POST) করতে পারবে।
        - শুধুমাত্র সুপার অ্যাডমিন (is_staff=True) আবেদনগুলো দেখতে বা অনুমোদন (GET/PUT) করতে পারবেন।
        """
        if self.action == 'create':
            # যে কোনো লগইন করা ইউজার আবেদন করতে পারবেন
            return [permissions.IsAuthenticated()]
        
        # শুধুমাত্র সুপার অ্যাডমিন আবেদনগুলো ম্যানেজ করতে পারবেন
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        """
        যখন কোনো ইউজার আবেদন করেন, তখন স্বয়ংক্রিয়ভাবে 'user' ফিল্ডটি সেট করুন
        এবং স্ট্যাটাস 'Pending' রাখুন।
        """
        serializer.save(user=self.request.user, status='Pending')

    def update(self, request, *args, **kwargs):
        """
        "ওয়ার্ল্ড-ক্লাস" অটোমেশন:
        যখন সুপার অ্যাডমিন একজন ইন্সট্রাক্টরকে "Approve" (অনুমোদন) করবেন,
        তখন স্বয়ংক্রিয়ভাবে তার জন্য `InstructorProfile` তৈরি করুন।
        """
        application = self.get_object()
        new_status = request.data.get('status')

        # --- "ওয়ার্ল্ড-ক্লাস" অটোমেশন লজিক ---
        if new_status == 'Approved' and application.status != 'Approved':
            # যদি স্ট্যাটাস "Approved" করা হয়, স্বয়ংক্রিয়ভাবে প্রোফাইল তৈরি করুন
            InstructorProfile.objects.get_or_create(user=application.user)
        # ------------------------------------

        # মূল আপডেট ফাংশনটি কল করুন
        return super().update(request, *args, **kwargs)


class InstructorProfileViewSet(viewsets.ModelViewSet):
    """
    সুপার অ্যাডমিনের জন্য: অনুমোদিত ইন্সট্রাক্টরদের প্রোফাইল
    এবং Revenue Share ম্যানেজ করার জন্য।
    (শুধুমাত্র সুপার অ্যাডমিন এটি অ্যাক্সেস করতে পারবেন)
    """
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class OrderViewSet(viewsets.ModelViewSet):
    """
    সুপার অ্যাডমিনের জন্য: B2C (মার্কেটপ্লেস) বিক্রির হিসাব বা "লেজার বুক"।
    (শুধুমাত্র সুপার অ্যাডমিন এটি অ্যাক্সেস করতে পারবেন)
    """
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]