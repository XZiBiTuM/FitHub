from django import forms
from .models import Form


class OrderForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['name', 'email', 'phone_number', 'city', 'street', 'house', 'comment']
        labels = {
            'name': 'Имя',
            'email': 'Электронная почта',
            'phone_number': 'Номер телефона',
            'city': 'Город',
            'street': 'Улица',
            'house': 'Дом',
            'comment': 'Комментарий'
        }
