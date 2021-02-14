from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from .forms import RegisterForm, FrontendAuthenticationForm
# Create your views here.


def register(request):
    """
    register user
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            RegisterForm.save(form)
            messages.success(request, _('Profile has been created successfully.'))
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
    else:
        form = RegisterForm()
    return render(request, 'account/signup.html', {'form': form})


class UserLoginView(LoginView):
    """
    checking user is login
    """
    form_class = FrontendAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        """
        checking user is login  and redirecting to user dash board
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if self.request.user.id:
            return redirect('home')
        return super(UserLoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Security check complete. Log the user in. remember me function """
        login(self.request, form.get_user())
        if self.request.POST.get('remember_me', None) and self.request.user.id:
            self.request.session.set_expiry(86400)
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        """"""
        context = super().get_context_data(**kwargs)
        context.update({'page_title': _(' | Login') , })
        return context


def logout_user(request):
    logout(request)
    return redirect("account_login")
