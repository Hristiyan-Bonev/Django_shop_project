from .forms import UserCreationForm, UserAuthenticationForm
from .models import Item, CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, TemplateView, FormView
from django.shortcuts import get_object_or_404, redirect, reverse, render


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    paginate_by = 7
    context_object_name = 'products'

class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(FormView):
    template_name = 'sign_up.html'
    form_class = UserCreationForm
    success_url = '/items'

    def post(self, request, *args, **kwargs):
        super(SignUpView, self).post(request, *args, **kwargs)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(self.get_success_url())
        # If form not saved, return form
        context = {}
        context.update({
            'form': UserCreationForm(request.POST)
        })
        return JsonResponse({'errors':form.errors}, safe=False)


@login_required
def add_to_cart(request, **kwargs):
    import ipdb; ipdb.set_trace()
    user_profile = get_object_or_404(CustomUser, username=request.user.username)

    item = Item.objects.filter(id=kwargs.get('pk', None)).first()
    return redirect(reverse('item_list'))
