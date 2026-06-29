from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from customer.models import Customer, Company, Inquiry, InquiryItem

def DashboardView(request):
    last_30_days = timezone.now() - timedelta(days=30)

    new_customers = Customer.objects.filter(
        created_date__gte=last_30_days
    ).order_by("-created_date")

    new_inquiries = InquiryItem.objects.filter(
        created_date__gte=last_30_days
    ).order_by("created_date")

    context = {
        "new_inquiries": new_inquiries.count(),
        "total_companies": Company.objects.count(),
        "total_customers": Customer.objects.count(),
        "new_customer_count": new_customers.count(), 
        "new_customer_list": new_customers, 
        "recent_inquiries": Inquiry.objects.order_by("-created_date")[:6],
    }

    return render(request, "dashboard.html", context)