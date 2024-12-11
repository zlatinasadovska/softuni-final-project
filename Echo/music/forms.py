from django import forms
from Echo.music.models import Playlist, Track, Testimonial


class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


class AddTrackToPlaylistForm(forms.Form):
    track = forms.ModelChoiceField(queryset=Track.objects.all(), label="Select Track")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your feedback...',
                'rows': 5
            }),
        }
        labels = {
            'text': 'Your Feedback',
        }
