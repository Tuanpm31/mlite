from django import forms
from .models import ContentSendInbox


class CreateContentSendInbox(forms.ModelForm):
    # content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'required': True, 'class': 'content-send-inbox'}))
    # image = forms.ImageField(label='Hình Ảnh')
    def __init__(self, *args, **kwargs):
        super(CreateContentSendInbox, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs["class"] = 'content-send-inbox'
        self.fields['content'].widget.attrs["id"] = 'content'
    class Meta:
        model = ContentSendInbox
        fields=['content', 'image']


class UpdateContentSendInbox(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateContentSendInbox, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs["class"] = 'content-send-inbox'
        self.fields['content'].widget.attrs["id"] = 'content'
    class Meta:
        model = ContentSendInbox
        fields = ['content', 'image']