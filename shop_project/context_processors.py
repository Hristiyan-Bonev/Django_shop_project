from .forms import UserCreationForm, UserAuthenticationForm, CheckoutForm

def SignUpModalForm(request):
    '''
    Add UserCreationForm in context of each template
    '''
    return {
        'signup_modal_form': UserCreationForm(),
        'login_modal_form': UserAuthenticationForm(),
        'checkout_form': CheckoutForm(request.session.get('cart'))
    }
