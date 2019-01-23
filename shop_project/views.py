from .forms import UserCreationForm, UserAuthenticationForm
from .models import Item, CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, TemplateView, FormView, View
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



class CheckoutView(View):
    template_name = 'checkout.html'

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        print(cart)
        return render(request, self.template_name, context={'cart':cart})

@login_required
def view_cart(request, **kwargs):
    pass

@login_required
def remove_from_cart(request, **kwargs):
    pass

@login_required
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(CustomUser, username=request.user.username)

    item = Item.objects.filter(id=kwargs.get('pk', None)).first()
    cart = request.session.get('cart', {})
    cart.update({item.name: {
                'quantity': 1,
                'name': item.name,
                'price': str(item.price)
    }})
    # TODO: RETURN TOTAL AS WELL
    print(cart)
    request.session['cart'] = cart
    return redirect(reverse('item_list'))
