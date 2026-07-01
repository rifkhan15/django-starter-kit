from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from customer.models import Customer, Company, Inquiry, InquiryItem

def DashboardView(request):
    last_7_days = timezone.now() - timedelta(days=7)

    pending_inquiries = InquiryItem.objects.filter(
        status='pending'
    )
    
    new_companies = Company.objects.filter(
        created_date__gte=last_7_days
    ).order_by("-created_date")

    new_customers = Customer.objects.filter(
        created_date__gte=last_7_days
    ).order_by("-created_date")

    new_inquiryitems = InquiryItem.objects.filter(
        created_date__gte=last_7_days
    ).order_by("created_date")


    context = {
        "pending_inquiries" : pending_inquiries.count(),
        "new_companies_count": new_companies.count(),
        "new_customers_count": new_customers.count(), 
        "new_inquiryitems_count": new_inquiryitems.count(),
        "total_companies": Company.objects.count(),
        "total_customers": Customer.objects.count(),
        "total_inquiries": InquiryItem.objects.count(),
        "recent_inquiryitems": InquiryItem.objects.order_by("-id")[:15],
        "recent_customers": Customer.objects.order_by("-created_date")[:7],
    }

    return render(request, "dashboard.html", context)