# dChat

Open source Discord/forum hybrid built for public-readable communities and member-only interaction.

Current release baseline: `v1.3`

Live example:

- `https://forum.dek.cx/`

## What dChat is

dChat is designed as a 2026-style forum shell with Discord-familiar navigation, live chatroom behavior, and classic thread depth. Guests can read the whole community. Signed-up users can post, reply, react, chat in real time, customize profiles, and use direct messages without the interface turning into a cluttered admin maze.

## Core feature set

### Forum and thread features

- Public-readable categories, topics, threads, and replies
- Member-only posting, replying, editing, voting, and profile customization
- Nested forum replies with connected conversation flow
- Thread tags, sticky threads, announcements, and thread locking
- Direct post permalinks for linking to a specific reply inside a thread
- `@mentions` with mention notifications and unread highlighting
- Image-led threads and inline image previews
- Markdown composer with formatting tools
- Search across the forum surface

### Live category chatrooms

- Every category can act as a live chatroom
- Real-time chatroom updates for new messages
- Latest three related topics pinned at the top of each room
- Chained message layout so uninterrupted conversation reads naturally
- Quote reply and direct reply actions on chat messages
- Image uploads inside chatrooms
- Optional KLIPY GIF picker integration
- Participant rail for active room members

### Profiles, identity, and community

- Clickable Discord-style user popup cards
- Avatars, bios, social links, and richer profile pages
- Live forum stats including posts, topics, and reputation
- Recent topics and replies on profile surfaces
- Online/offline presence indicators
- Role badges for member, moderator, and admin users

### Direct messages and notifications

- User-to-user direct messages
- Merged inbox for DMs, mentions, and notification activity
- Live unread badge updates without a full page refresh
- Markdown, embeds, and multiple image uploads in DMs
- Per-conversation DM icons in the guild rail
- Per-user DM privacy controls

### Moderation and admin tools

- Admin and moderator role permissions
- Reports queue and moderation logs
- Soft delete and restore flows
- Warn actions with reputation penalties
- Permanent thread nuking for admins
- Attachment review and removal tools
- Branding, theme, footer link, and color controls from admin

### Safety, privacy, and legal

- Built-in math CAPTCHA with no external dependency
- Optional email verification, off by default
- Sanitized markdown and controlled embed handling
- Restricted image upload types and file size limits
- External link warning gate
- GDPR export and account/content deletion flows
- Terms, privacy, and cookie policy pages included by default

### Setup and deployment

- First-run setup wizard
- First registered account becomes the initial admin
- User `id=1` email becomes the default public legal contact
- Minimal default stack with no required worker process
- Docker Compose support for Linux, macOS, and Windows
- Optional Redis and Caddy profile for fuller production setups

## Default stack

The default install is intentionally small:

- Django
- PostgreSQL
- WhiteNoise for static assets
- Docker Compose

Optional full profile:

- Redis for shared cache
- Caddy for reverse proxy and TLS termination

There is no required worker process in the default release.

Tracked source footprint:

- `134` tracked files
- about `0.49 MB` before dependencies, media, and generated static output

## Why it stays lightweight

- Django handles the full app surface instead of splitting the product into multiple services
- WhiteNoise serves static assets in the default setup
- Redis is optional, not required
- GIF search is optional, not hard-wired
- The default install path stays close to `app + database`, which makes self-hosting simpler

## Quick start

Linux/macOS:

```bash
cp .env.example .env
docker compose up -d --build
```

PowerShell:

```powershell
Copy-Item .env.example .env
docker compose up -d --build
```

Open `http://localhost:8000` and complete `/setup`.

Optional full profile:

```bash
docker compose --profile full up -d --build
```

That adds Redis and Caddy. With the full profile, the app is served on `http://localhost` and `https://localhost`.

## First-run behavior

- If no users exist, dChat redirects to `/setup`
- The first created account becomes the initial admin
- The first created account is also user `id=1`
- The email on user `id=1` is used as the default public legal contact on the Terms, Privacy, and Cookies pages

Choose that first email accordingly.

## Docs

Runtime pages:

- Changelog: `/changelog/`
- Docs: `/docs/readme/`, `/docs/install/`, `/docs/faq/`

## Notes

- Guest users can read but cannot interact
- Uploads are limited to PNG, JPEG, and GIF up to 8 MB
- Markdown is sanitized
- Video upload is disabled
- Redis cache and metrics are opt-in
- KLIPY GIF search stays disabled until the operator adds an API key in Site Branding

## License

MIT. See `LICENSE`.
