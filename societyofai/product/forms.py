from django import forms


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_state = forms.CharField(required=False)
    shipping_country = forms.CharField(required=True)
    shipping_zip = forms.CharField(required=False)

