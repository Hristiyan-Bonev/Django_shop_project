from .forms import UserCreationForm, CheckoutItemForm
from .models import Item, CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, TemplateView, FormView, View
from django.shortcuts import get_object_or_404, redirect, reverse, render


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    paginate_by = 3
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


class CheckoutView(FormView):
    template_name = 'checkout.html'
    # form_class = CheckoutItemForm

    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        # Get total price
        total_price = round(float(cart.pop('total', 0)), 2)

        return render(request, self.template_name, {'cart': cart, 'total_price': total_price})



@login_required
def remove_from_cart(request, **kwargs):
    pass

@login_required
def add_to_cart(request, **kwargs):
    item = Item.objects.filter(id=kwargs.pop('pk', None)).first()
    cart = request.session.get('cart', dict({'total': 0}))

    if cart.get(item.name, False):
        # Increase quantity of item if already exist.
        cart[item.name]['quantity'] += 1
    else:
        # Add item in cart
        cart.update({item.name: {
                    'quantity': 1,
                    'name': item.name,
                    'price': str(item.price)
                    }
        })
    cart['total'] += float(item.price)
    request.session['cart'] = cart
    request.session['item'] = {'name': item.name,
                               'image': item.image.url}
    print(cart)
    messages.success(request, 'Item added to cart.')
    print(messages)
    return HttpResponseRedirect('/items')
