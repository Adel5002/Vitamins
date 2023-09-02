from django import forms
from django.core.validators import MinValueValidator

from .models import Comment, CartOrder

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Не забудьте написать комментарий!'}))

    class Meta:
        model = Comment
        fields = ['body', 'rating']





PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartSubtractProductForm(forms.Form):
    quantity = forms.IntegerField(
        label='Quantity',
        validators=[MinValueValidator(1)]
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = CartOrder
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'phone_number']
