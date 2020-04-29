from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url

def registration_view(request):
    context = {}
    if request.POST: #Si el request es post se inició con el botón submit del form
        form = RegistrationForm(request.POST) #Rellenamos al form con los elementos del POST request que és lo que ingresó el user
        if form.is_valid(): #Qué pasa si el form fué llenado sin errores
            form.save() #Guardamos el form con los datos que el user ingreso para, si lo ingresó mal, devolvérselo con lo que puso para que lo modifique y vea que hizo mal
            email = form.cleaned_data.get('email') #obtenemos el valor que pasó el user en el form como email para luego verificar que está bien
            raw_password = form.cleaned_data.get('password1') #La primera contraseña que ingrese el user
            #Pasamos las dos variables que acabamos de definir dentro de authenticate()
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('main')
        else:
            context['registration_form'] = form
    else: #Si el request es GET significa que el user intentó obtener ésta página, por ende quiere registrarse
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context) #Pasamos el request, la ubicación de la template en el esquema de tempaltes, y el context

def logout_view(request): #La view a lacual mandamos al user cuando da click en logout
    logout(request) #Lo deslogueamos
    return redirect('main') #Lo redirigimos a la página principal


class login_view(auth_views.LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        return resolve_url('main')