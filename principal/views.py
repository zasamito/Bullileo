from django.shortcuts import render,redirect
from datetime import datetime
from principal.forms import LoginForm, RegisterForm
from django.views.generic import CreateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from principal.models import Usuario

# Create your views here.

def index(request):
    return render(request, 'index.html')

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/Inicio/'
    succes_message = "%(name)s Se ha creado exitosamente!"

    def form_valid(self, form):
        request = self.request
        Usuario = form.cleaned_data.get("Usuario")
        password = form.cleaned_data.get("password")
        remember_me = form.cleaned_data['remember_me']
        user = authenticate(request, username=Usuario, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                            request.session.set_expiry(0)
            if user.admin or user.tecnico:
                return redirect('/Administracion/')
            return redirect('/Inicio/' + str(user.id))
        return super(LoginView, self).form_invalid(form)
    
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/Inicio/'
    succes_message = "%(name)s Se ha creado exitosamente!"
    def form_valid(self, form):
        print(len(self.request.POST['rut']))
        request = self.request
        login(request, form.save())
        if request.user.admin:
                return redirect('/Administracion/')
        return redirect('' + str(request.user.id))