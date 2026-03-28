import re
from urllib.parse import parse_qs, quote, urlparse

import bleach
import markdown
from django.conf import settings
from django import template
from django.utils.safestring import mark_safe

from apps.forum.models import MENTION_PATTERN

register = template.Library()

ALLOWED_TAGS = [
    "p",
    "br",
    "blockquote",
    "code",
    "pre",
    "em",
    "strong",
    "a",
    "ul",
    "ol",
    "li",
    "h1",
    "h2",
    "h3",
]
ALLOWED_ATTRIBUTES = {"a": ["href", "title", "target", "rel", "class", "data-user-card"]}
ALLOWED_PROTOCOLS = ["http", "https"]


def group_names(user) -> set[str]:
    prefetched = getattr(user, "_prefetched_objects_cache", {}).get("groups")
    if prefetched is not None:
        return {group.name for group in prefetched}
    return set(user.groups.values_list("name", flat=True))


@register.filter(name="user_role")
def user_role(user) -> str:
    if not user:
        return "member"
    if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
        return "admin"
    names = group_names(user)
    if "Admin" in names:
        return "admin"
    if "Moderator" in names:
        return "moderator"
    return "member"


def link_mentions(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        username = match.group(1)
        return f'<a href="/accounts/u/{username}/" class="mention" data-user-card="{username}">@{username}</a>'

    return MENTION_PATTERN.sub(repl, text or "")


def rewrite_external_links(attrs, new=False):
    href = attrs.get((None, "href"))
    if not href:
        return attrs
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        attrs[(None, "href")] = f"/out/?u={quote(href, safe='')}"
        attrs[(None, "rel")] = "noopener noreferrer"
        attrs[(None, "target")] = "_self"
    return attrs


def extract_embed_urls(text: str) -> list[str]:
    return re.findall(r"(https?://[^\s]+)", text or "")


def to_embed_html(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")
    path = parsed.path.strip("/")
    if "youtube.com" in host:
        vid = parse_qs(parsed.query).get("v", [""])[0]
        if vid:
            return iframe(f"https://www.youtube.com/embed/{vid}")
    if "youtu.be" in host and path:
        return iframe(f"https://www.youtube.com/embed/{path.split('/')[0]}")
    if "twitch.tv" in host:
        if "/videos/" in parsed.path:
            vid = path.split("/")[-1]
            return iframe(f"https://player.twitch.tv/?video=v{vid}&parent={settings.EMBED_PARENT_DOMAIN}")
        if path:
            channel = path.split("/")[0]
            return iframe(f"https://player.twitch.tv/?channel={channel}&parent={settings.EMBED_PARENT_DOMAIN}")
    if "tiktok.com" in host:
        return f'<a href="{bleach.clean(url)}" target="_blank" rel="noopener">View TikTok video</a>'
    if host in {"x.com", "twitter.com"} and "/status/" in parsed.path:
        safe_url = bleach.clean(url, protocols=ALLOWED_PROTOCOLS, strip=True)
        return (
            '<blockquote class="twitter-tweet" data-theme="dark">'
            f'<a href="{safe_url}">{safe_url}</a>'
            "</blockquote>"
        )
    return link_card(url)


def iframe(src: str) -> str:
    safe_src = bleach.clean(src, protocols=ALLOWED_PROTOCOLS, strip=True)
    return (
        '<div class="embed-wrap">'
        f'<iframe src="{safe_src}" loading="lazy" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>'
        "</div>"
    )


def link_card(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.replace("www.", "")
    path = parsed.path or "/"
    safe_display = bleach.clean(f"{host}{path}", strip=True)
    outbound = f"/out/?u={quote(url, safe='')}"
    return (
        '<a class="link-card" href="'
        + outbound
        + '">'
        + '<span class="link-card-label">External Link</span>'
        + "<strong>"
        + safe_display
        + "</strong>"
        + "</a>"
    )


def render_markdown_html(value: str, *, enable_mentions: bool = True) -> str:
    source = value or ""
    linked = link_mentions(source) if enable_mentions else source
    html = markdown.markdown(linked, extensions=["fenced_code", "sane_lists", "nl2br"])
    cleaned = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    linker = bleach.linkifier.Linker(callbacks=[rewrite_external_links], skip_tags=["pre", "code"])
    cleaned = linker.linkify(cleaned)
    embeds = [to_embed_html(url) for url in extract_embed_urls(source)]
    embed_markup = "".join([chunk for chunk in embeds if chunk])
    return mark_safe(cleaned + embed_markup)


@register.filter(name="render_markdown")
def render_markdown(value: str) -> str:
    return render_markdown_html(value, enable_mentions=True)


@register.filter(name="render_markdown_plain")
def render_markdown_plain(value: str) -> str:
    return render_markdown_html(value, enable_mentions=False)
