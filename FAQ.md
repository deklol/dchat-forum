# FAQ

## Is read-only public access supported?

Yes. Guests can read public content; interaction requires signup/login.

## Is email verification required?

No by default. `EMAIL_VERIFICATION_REQUIRED=false` is the default setting.

## Which CAPTCHA is used?

dChat ships with a built-in math CAPTCHA. No external API keys are required.

## Is the first admin email public?

Yes by default. The email on user `id=1` is used as the public legal contact on the Terms, Privacy, and Cookies pages unless the operator changes it later.

## How does version tracking work?

Publishing a changelog entry in admin auto-assigns the next `+0.1` version.

## Can users upload videos?

No. Video uploads are disabled. Supported image uploads are PNG/JPEG/GIF up to 8 MB.

## Can users embed external videos?

Yes. YouTube, Twitch, and X/Twitter post links are embedded. TikTok links are preserved as rich outbound links.

## Is this secure?

Security controls are included, but you must set strong secrets, domain settings, HTTPS, backups, and monitoring in production.
