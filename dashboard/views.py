from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from customer.models import Customer, Company, Inquiry, InquiryItem

def DashboardView(request):
    last_30_days = timezone.now() - timedelta(days=30)

    new_companies = Company.objects.filter(
        created_date__gte=last_30_days
    ).order_by("-created_date")

    new_customers = Customer.objects.filter(
        created_date__gte=last_30_days
    ).order_by("-created_date")

    new_inquiries = InquiryItem.objects.filter(
        created_date__gte=last_30_days
    ).order_by("created_date")

    context = {
        "new_companies_count": new_companies.count(),
        "new_customers_count": new_customers.count(), 
        "new_inquiries_count": new_inquiries.count(),
        "total_companies": Company.objects.count(),
        "total_customers": Customer.objects.count(),
        "total_inquiries": InquiryItem.objects.count(),
        "recent_inquiries": InquiryItem.objects.order_by("-created_date")[:10],
        "recent_customers": Customer.objects.order_by("-created_date")[:10],
    }

    return render(request, "dashboard.html", context)