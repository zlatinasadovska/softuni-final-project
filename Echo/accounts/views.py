from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, FormView
from Echo.accounts.forms import UserLoginForm, UserRegistrationForm
from Echo.accounts.models import UserProfile
from django.urls import reverse_lazy


class CustomLoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, "Invalid email or password.")
        return self.form_invalid(form)


class RegisterView(CreateView):
    model = UserProfile
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        return redirect('home')

    return render(request, 'accounts/delete_profile.html')


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = self.object.playlists.all() if hasattr(self.object, 'playlists') else []
        return context


@login_required
def edit_profile(request):
    user_profile = request.user

    if request.method == 'POST':
        # Handle profile picture updates
        if 'remove_picture' in request.POST:
            user_profile.profile_picture.delete()
            user_profile.profile_picture = None
        elif 'profile_picture' in request.FILES:
            user_profile.profile_picture.delete()
            user_profile.profile_picture = request.FILES['profile_picture']

        # Handle password updates
        current_password = request.POST.get('current_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_new_password = request.POST.get('confirm_new_password', '').strip()

        # Password change validation
        if current_password or new_password or confirm_new_password:
            if not (current_password and new_password and confirm_new_password):
                messages.error(request, "All password fields must be filled to change your password.")
                return render(request, 'accounts/edit_profile.html', {'user': user_profile})
            elif new_password != confirm_new_password:
                messages.error(request, "New passwords do not match.")
                return render(request, 'accounts/edit_profile.html', {'user': user_profile})
            elif not user_profile.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return render(request, 'accounts/edit_profile.html', {'user': user_profile})
            else:
                user_profile.set_password(new_password)
                user_profile.save()

                # Keep the user logged in after password change
                update_session_auth_hash(request, user_profile)
                messages.success(request, "Your password has been updated.")
                return redirect('profile')

        # Handle username update
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != user_profile.username:
            user_profile.username = new_username

        # Save any other changes
        user_profile.save()
        messages.success(request, "Your profile has been updated.")
        return redirect('profile')

    return render(request, 'accounts/edit_profile.html', {'user': user_profile})

