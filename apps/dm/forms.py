from django import forms


class DirectMessageForm(forms.Form):
    body = forms.CharField(
        max_length=4000,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Write a direct message...",
            }
        ),
    )

    def clean_body(self) -> str:
        body = (self.cleaned_data.get("body") or "").strip()
        if not body:
            raise forms.ValidationError("Message cannot be empty.")
        return body


class QuickDirectMessageForm(forms.Form):
    body = forms.CharField(
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
            }
        ),
    )

    def clean_body(self) -> str:
        body = (self.cleaned_data.get("body") or "").strip()
        if not body:
            raise forms.ValidationError("Message cannot be empty.")
        return body


class StartDirectMessageForm(forms.Form):
    username = forms.CharField(max_length=150)
    body = forms.CharField(
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
            }
        ),
    )

    def clean_username(self) -> str:
        username = (self.cleaned_data.get("username") or "").strip().lstrip("@")
        if not username:
            raise forms.ValidationError("Username is required.")
        return username

    def clean_body(self) -> str:
        body = (self.cleaned_data.get("body") or "").strip()
        if not body:
            raise forms.ValidationError("Message cannot be empty.")
        return body


class DirectMessagePreferenceForm(forms.Form):
    allow_incoming = forms.BooleanField(
        required=False,
        label="Allow incoming DMs from other users",
    )


class ReportDirectMessageForm(forms.Form):
    reason = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Optional report reason...",
            }
        ),
    )
