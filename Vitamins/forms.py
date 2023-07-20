from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Не забудьте написать комментарий!'}))

    class Meta:
        model = Comment
        fields = ['body', 'rating']





