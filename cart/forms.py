from django import forms

PRODUCT_QUANTITY_CHOICES = [
    (i, str(i)) for i in range(1, 21)
]
# PRODUCT_QUANTITY_CHOICES = [
#     (1, 1),
#     (2, 2),
#     (3, 3)
# ]
# dict(PRODUCT_QUANTITY_CHOICES)
# {1:1, 2:2, 3:3}
# [
# (i, i), (i, i)
# ]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES
    )
    update = forms.BooleanField(
        required=False, widget=forms.HiddenInput
    )

