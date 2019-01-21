from .forms import UserCreationForm

def SignUpModalForm(request):
    '''
    Add UserCreationForm in context of each template
    '''
    return {
        'signup_modal_form': UserCreationForm()
    }
