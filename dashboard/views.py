from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def DashboardView(request):
    return render(request, 'dashboard.html')
