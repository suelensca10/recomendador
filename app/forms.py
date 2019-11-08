from django import forms

from .models import Rating, Book

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('book', 'rating',)

    rating = forms.ChoiceField(
        choices=(
            ('0', '-'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        )
    )

#class ResultForm(forms.ModelForm):
#    class Meta:
#        model = Book
#        fields = ('title','author',)