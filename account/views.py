from .forms import RegistrationForm, AccountAuthenticationForm
from .models import Account, Profile
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import DetailView
from django.shortcuts import resolve_url, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from roadmaps.models import RoadmapMembership, Roadmap, RoadmapTagRelationship
from .forms import RegistrationForm, AccountAuthenticationForm, ProfileForm


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    fields = ['email', 'username', 'date_joined']
    template_name = 'account/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_seen"] = self.request.session.get('last_seen', None)

        #Código para pasar al update form de nuestro profile dentro de la view
        profile = get_object_or_404(Profile, user=self.kwargs['pk'])
        context['profile_form'] = ProfileForm(instance=profile)
        
        # Código para agregar a la feed roadmaps recomendados en base a cuando se actualizaron por última vez
        def user_roadmaps_feed(some_request:HttpRequest): #Algoritmo que nos dá la feed de los últimos roadmaps actualizados que entran en los intereses de nuestro user
            updated_roadmaps_feed = []
            new_roadmaps_feed = []
            
            if some_request.user.profile.interests.count() > 0:
                
                for interest in some_request.user.profile.interests.all():
                    if len(updated_roadmaps_feed) > 2: #Si la len ya tiene 3 objetos cortamos el loop
                        break
                    qs = RoadmapTagRelationship.objects.filter(tag=interest).order_by('updated_at')
                    for rtr in qs:
                        if len(updated_roadmaps_feed) > 2: #Si la len ya tiene 3 objetos cortamos el loop
                            break
                        updated_roadmaps_feed.append(rtr.roadmap)
                
                for interest in some_request.user.profile.interests.all():
                    if len(new_roadmaps_feed) > 2: #Si la len ya tiene 3 objetos cortamos el loop
                        break
                    qs = RoadmapTagRelationship.objects.filter(tag=interest).order_by('created_at')
                    for rtr in qs:
                        if len(new_roadmaps_feed) > 2: #Si la len ya tiene 3 objetos cortamos el loop
                            break
                        new_roadmaps_feed.append(rtr.roadmap)
                
                # Si la feed tiene elementos la devuelvo
                return updated_roadmaps_feed, new_roadmaps_feed

            else: #Si el user no tiene intereses devuelvo el None para que lo evalúe como False la tempalte
                
                context['feed_message'] = 'Add some interests to see recommended content. '
                return None, None

        a, b = user_roadmaps_feed(self.request)
        
        context['updated_roadmaps_feed'] = a
        context['new_roadmaps_feed'] = b

        return context

    def post(self, request, pk):
        profile = get_object_or_404(Profile, user=self.kwargs['pk']) #Agarramos el perfil donde el user sea el de la primary key que pasamos
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if not profile_form.is_valid():
            context['profile_form', profile_form]
            # form no cumple con los validators: cargamos de nuevo el form con los mensajes de error
            return render(request, self.template_name, context)
        password_check = profile_form.cleaned_data.get('password_check')
        account = authenticate(email=self.request.user.email, password=password_check)
        if account is None:
            context.get('error_messages', []).append('Wrong user')
        # Si todo sale bien guardamos al form en la db y volvemos a la home
        profile = profile_form.save()
        profile.save() # no se por qué, si no agrego ésta línea no se guarda
        return redirect('account', pk)
    

def registration_view(request):
    context = {}
    if request.POST: #Si el request es post se inició con el botón submit del form
        form = RegistrationForm(request.POST, request.FILES) #Rellenamos al form con los elementos del POST request que és lo que ingresó el user
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


@login_required(login_url='login')
def logout_view(request): #La view a lacual mandamos al user cuando da click en logout
    logout(request) #Lo deslogueamos
    return redirect('main') #Lo redirigimos a la página principal


class login_view(auth_views.LoginView):
    template_name = 'account/login.html'

    def get_success_url(self):
        return resolve_url('account', self.request.user.id) #Si se logueó lo mandamos a su home personalizada


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)