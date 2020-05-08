from django import forms
from django.contrib.auth.forms import UserCreationForm#, UserChangeForm
from django.contrib.auth import authenticate


from account.models import Account, Profile, SocialNetwork


class ProfileForm(forms.ModelForm):
    password_check = forms.CharField(
        label='Your password',
        widget=forms.PasswordInput,
        help_text='Introduce your password to save changes.'
    )
    
    class Meta:
        model = Profile
        fields = ['profile_pic', 'bio', 'profession', 'interests', 'country', 'show_activity']

class ConnectForm(forms.ModelForm):
    class Meta:
        model = SocialNetwork
        exclude = ('profile',)


class RegistrationForm(UserCreationForm): #Extiende a usercreationform
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2') #Pasamos los campos del form que tendrá el form

class AccountAuthenticationForm(forms.ModelForm): #No extiende funcionalidades de ningún form, es un form personalizado
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput, #Éste widget se usa para que la contraseña no se vea mientra el user la tipea
    )

    class Meta:
        model = Account #El modelo del form
        fields = ('email', 'password') #Los campos del modelo que quiero aparezcan en el form

    def clean(self): #Sobreescribimos el método clean de ModelForm cuya función es ejecutar dentro lógica antes de POSTear el form, para mandarlo así limpio en el request
        if self.is_valid():
            email = self.cleaned_data['email'] #Obtenemos el mail para anaizar si está bien hecho (si tiene @, etc.)
            password = self.cleaned_data['password'] #Obtenemos la contraseña para analizar si cumple los requisitos de seguridad que indica el form
            if not authenticate(email=email, password=password): #Autenticamos con ésta función las variables que ingresó el user al form
                raise forms.ValidationError('Invalid login') #Si alguna está mal, se larga el ValidationError que el form después lo usa para mostrar que estuvo mal
        
        