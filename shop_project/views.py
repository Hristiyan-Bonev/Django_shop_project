from .forms import UserCreationForm, UserAuthenticationForm
from .models import Item, CustomUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.views.generic import ListView, TemplateView, FormView
from django.http import HttpResponseRedirect


class ItemListView(ListView):

    model = Item
    template_name = 'item_list.html'

    def get_context_data(self, **kwargs):
        product_list = Item.objects.all()
        context = super().get_context_data( **kwargs)
        context['products'] = product_list
        return context


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(FormView):
    template_name = 'sign_up.html'
    form_class = UserCreationForm

    def post(self, request, *args, **kwargs):
        super(SignUpView, self).post(request, *args, **kwargs)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(self.get_success_url())
        # If form not saved, return form
        return render(self.get_success_url(), {'form': form})

    def get_success_url(self):
        return reverse('item_list')


class SignInView(FormView):
    template_name = 'sign_in.html'
    form_class = UserAuthenticationForm

    def get_success_url(self):
        return reverse('item_list')


@login_required
def add_to_cart(request, **kwargs):
    # import ipdb; ipdb.set_trace()
    user_profile = get_object_or_404(CustomUser, user=request.user)

    item = Item.objects.filter(id=kwargs.get('pk', None)).first()
    return redirect(reverse('item_list'))