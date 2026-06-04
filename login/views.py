from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'login/login.html')

def LogoutView(request):
    logout(request)
    return redirect('login')