from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, FormView
from Echo.accounts.forms import UserLoginForm, UserRegistrationForm, ProfilePictureForm
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
        user.delete()  # Deletes the user's profile
        logout(request)  # Log the user out after deletion
        return redirect('home')  # Redirect to home or another page

    return render(request, 'accounts/delete_profile.html')


class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['playlists'] = self.object.playlists.all() if hasattr(self.object, 'playlists') else []
        return context


@login_required
def update_profile_picture(request):
    user = request.user

    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfilePictureForm(instance=user)

    return render(request, 'accounts/update_profile_picture.html', {'form': form})
