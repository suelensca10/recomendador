from django import forms

from .models import Rating

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('book_id', 'rating',)

    book_id = forms.IntegerField()

    rating = forms.ChoiceField(
        choices=(
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        )
    )

