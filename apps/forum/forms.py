from django import forms
from django.conf import settings
from django.utils.text import slugify

from apps.forum.models import Post, Tag, Thread

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/gif"}


class ThreadForm(forms.ModelForm):
    tags_csv = forms.CharField(required=False, help_text="Comma-separated tags.")
    attachment = forms.FileField(required=False)

    class Meta:
        model = Thread
        fields = ("category", "title", "body_markdown")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"placeholder": "Thread title..."})
        self.fields["body_markdown"].required = False
        self.fields["body_markdown"].widget.attrs.update(
            {
                "placeholder": "Write the opening post or attach an image thread. Markdown, @mentions, and embeds work here...",
                "rows": 12,
                "data-markdown-input": "true",
            }
        )
        self.fields["tags_csv"].widget.attrs.update({"placeholder": "retro, announcements, help...", "spellcheck": "false"})
        self.fields["attachment"].widget.attrs.update({"accept": ".png,.jpg,.jpeg,.gif"})

    def clean(self):
        cleaned_data = super().clean()
        body = (cleaned_data.get("body_markdown") or "").strip()
        attachment = cleaned_data.get("attachment")
        if not body and not attachment:
            raise forms.ValidationError("Add thread text or upload an image.")
        cleaned_data["body_markdown"] = body
        return cleaned_data

    def clean_attachment(self):
        file = self.cleaned_data.get("attachment")
        if not file:
            return file
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise forms.ValidationError("Only PNG, JPG/JPEG, and GIF files are allowed.")
        if file.size > settings.MAX_UPLOAD_BYTES:
            raise forms.ValidationError(f"Max upload size is {settings.MAX_UPLOAD_MB} MB.")
        return file

    def save(self, commit=True):
        thread = super().save(commit=commit)
        tags_raw = self.cleaned_data.get("tags_csv", "")
        tags = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]
        tag_objs = []
        for name in tags[:8]:
            tag, _ = Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
            tag_objs.append(tag)
        if commit:
            thread.tags.set(tag_objs)
        else:
            self._pending_tags = tag_objs
        return thread


class PostForm(forms.ModelForm):
    attachment = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ("body_markdown",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body_markdown"].widget.attrs.update(
            {
                "placeholder": "Write a reply. Markdown, @mentions, and embeds work here...",
                "rows": 10,
                "data-markdown-input": "true",
            }
        )
        self.fields["attachment"].widget.attrs.update({"accept": ".png,.jpg,.jpeg,.gif"})

    def clean_attachment(self):
        file = self.cleaned_data.get("attachment")
        if not file:
            return file
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise forms.ValidationError("Only PNG, JPG/JPEG, and GIF files are allowed.")
        if file.size > settings.MAX_UPLOAD_BYTES:
            raise forms.ValidationError(f"Max upload size is {settings.MAX_UPLOAD_MB} MB.")
        return file
