from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Votre compte a bien été créé, vous pouvez désormais vous connecter !')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(
        request,
        'users/register.html',
        {'form': form}
    )


@login_required
def profile(request):
    return render(request, 'users/profile.html')
