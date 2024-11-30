from django import forms
from Echo.music.models import Playlist, Track


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

