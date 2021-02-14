from django.shortcuts import render,  get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import Product, CartItems, Cart, Address, Order
from .forms import CheckoutForm
# Create your views here.


class HomeView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 10
    template_name = "home.html"


@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item, created = CartItems.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    carts_qs = Cart.objects.filter(user=request.user, ordered=False)
    if carts_qs.exists():
        cart = carts_qs.first()
        if cart.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            cart.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:

        order = Cart.objects.create(
            user=request.user)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


@login_required
def remove_item_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    carts_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if carts_qs.exists():
        order = carts_qs.first()

        if order.items.filter(item__pk=item.pk).exists():
            order_item = CartItems.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            ).first()
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('home')
    else:
        messages.info(request, "You do not have an active order")
        return redirect("home")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("home")


class CheckoutView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:
            order = Cart.objects.get(user=self.request.user, ordered=False)

            form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("home")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            if form.is_valid():
                cart = Cart.objects.get(user=self.request.user, ordered=False)
                if form.is_valid():
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')
                    shipping_address = Address(
                        user=self.request.user,
                        street_address=shipping_address1,
                        apartment_address=shipping_address2,
                        country=shipping_country,
                        state=form.cleaned_data['shipping_state'],
                        zip_code=shipping_zip,
                    )
                    shipping_address.save()
                    cart.ordered = True
                    cart.save()
                    for item in cart.items.all():
                        item.ordered = True
                        item.save()
                    order = Order.objects.create(
                        user=self.request.user,
                        shipping_address=shipping_address
                    )
                    order.product.add(*cart.items.all())
                    messages.success(
                        self.request, "Order created successfully")
                    return redirect('home')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Cart.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs.first()
        if order.items.filter(item__slug=item.slug).exists():
            order_item = CartItems.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            ).first()
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("home",)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("home")