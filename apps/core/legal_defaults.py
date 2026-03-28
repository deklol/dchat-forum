from textwrap import dedent

PRIMARY_CONTACT_EMAIL_PLACEHOLDER = "{{PRIMARY_CONTACT_EMAIL}}"


def legal_document_defaults(site_name: str, contact_email: str) -> dict[str, dict[str, str]]:
    site = (site_name or "dChat Community").strip()
    contact = PRIMARY_CONTACT_EMAIL_PLACEHOLDER

    terms = dedent(
        f"""
        # Terms of Service

        Last updated: {{version_label}}

        These Terms of Service govern access to and use of **{site}**. In these terms, **"Service"** means this website, community, and related features made available through dChat. **"Operator"**, **"we"**, **"us"**, and **"our"** mean the person or organization running this deployment of the Service. The primary contact for this Service is **{contact}** unless the Operator publishes a different contact point.

        ## 1. Acceptance and scope

        By accessing or using the Service, you agree to these terms. If you do not agree, do not use the Service.

        The Service is forum software operated by an independent site operator. Some features may be public, while others require an account. These terms apply to all visitors, registered users, moderators, and administrators.

        ## 2. Eligibility and accounts

        You must be at least 13 years old, or the minimum age required in your jurisdiction, to use the Service.

        If you create an account, you must:

        - provide accurate registration information;
        - keep your login credentials confidential;
        - remain responsible for activity under your account; and
        - notify the Operator promptly if you believe your account has been compromised.

        You may not impersonate another person or create accounts for abusive, deceptive, or unlawful purposes.

        ## 3. Public and private areas of the Service

        Threads, replies, profile details, usernames, uploaded images, votes, and similar community activity may be visible to the public unless the Operator configures the Service differently.

        Direct messages are intended to be private between participants, but they are not end-to-end encrypted. The software stores direct messages in encrypted form at rest. The Operator may still be able to access direct messages where reasonably necessary for security, abuse prevention, legal compliance, maintenance, backup recovery, or when a participant reports a message for moderation.

        ## 4. Acceptable use

        You agree not to use the Service to:

        - break the law or encourage unlawful conduct;
        - harass, threaten, stalk, defraud, or exploit others;
        - post or share defamatory, hateful, sexually exploitative, or otherwise unlawful content;
        - upload malware, malicious code, phishing content, or harmful files;
        - attempt unauthorized access, scraping in breach of published rules, or disruption of the Service;
        - interfere with security, rate limits, moderation tools, or abuse-prevention systems;
        - infringe intellectual property, privacy, publicity, or other rights; or
        - use automation in a way that unreasonably burdens the Service.

        The Operator may set additional community rules, topic rules, or moderation standards. Those rules form part of these terms.

        ## 5. User content

        You retain ownership of content you submit, including posts, replies, profile text, messages, and uploads.

        By submitting content, you grant the Operator a non-exclusive, worldwide, royalty-free license to host, store, reproduce, display, distribute, reformat, back up, moderate, and otherwise process that content as necessary to operate, secure, improve, and provide the Service.

        You represent that you have the rights needed to submit the content and grant this license.

        ## 6. Moderation and enforcement

        The Service may include reports, moderation queues, content flags, soft deletion, restoration, account controls, and other moderation tools. The Operator may investigate misuse and may remove content, restrict accounts, disable features, or terminate access where reasonably necessary to enforce these terms, comply with law, protect users, or protect the Service.

        Moderation decisions may be made with or without prior notice where the Operator considers this necessary.

        ## 7. Uploaded files, embeds, and external links

        The Service may allow uploads and may support embedded or linked content from third-party services such as YouTube, Twitch, TikTok, or X/Twitter. The Operator does not control third-party services and is not responsible for their availability, terms, privacy practices, or content.

        External links and embeds are used at your own risk. The Service may show a warning before opening external links.

        ## 8. Intellectual property

        The Service software, design, branding chosen by the Operator, and Operator-created content are protected by applicable intellectual property laws.

        Except as allowed by law or by the Operator in writing, you may not copy, reverse engineer, redistribute, or exploit the Service or Operator content beyond normal personal use of the community.

        ## 9. Service availability and changes

        The Service is provided on an **"as is"** and **"as available"** basis. The Operator may change, suspend, or discontinue any part of the Service at any time.

        The Operator does not guarantee uninterrupted availability, error-free operation, or that the Service will always be secure or free of harmful components.

        ## 10. Privacy and cookies

        Your use of the Service is also subject to the Privacy Policy and Cookie Policy published on the Service. Those documents explain how personal data and cookies are handled.

        ## 11. Termination

        You may stop using the Service at any time. The Operator may suspend or terminate your access, or remove or restrict content, if reasonably necessary to enforce these terms, comply with legal obligations, or protect the Service, users, or third parties.

        Clauses that by their nature should survive termination will continue to apply, including provisions on licenses, liability, disputes, and enforcement.

        ## 12. Disclaimers

        Community content is created by users. The Operator does not guarantee that user content is accurate, safe, lawful, or suitable for any purpose.

        Nothing on the Service constitutes professional advice unless the Operator clearly states otherwise.

        ## 13. Limitation of liability

        To the maximum extent permitted by law, the Operator will not be liable for indirect, incidental, special, consequential, exemplary, or punitive damages, or for loss of data, profits, goodwill, or business interruption arising out of or related to the Service.

        To the maximum extent permitted by law, the Operator's aggregate liability for claims arising out of or relating to the Service will not exceed the greater of:

        - the amount you paid to the Operator for the Service in the 12 months before the claim; or
        - GBP 100 or the equivalent amount in the Operator's local currency.

        Some jurisdictions do not allow certain exclusions or limitations. In those cases, the above limits apply only to the extent permitted by law.

        ## 14. Governing law and disputes

        Unless the Operator publishes a site-specific legal notice stating otherwise, these terms are governed by the laws applicable where the Operator is established, excluding conflict-of-law rules.

        To the extent permitted by law, disputes should be brought in the courts with jurisdiction over the Operator or as otherwise required by mandatory consumer law.

        ## 15. Changes to these terms

        The Operator may update these terms from time to time. The current version will be published on the Service with an updated version number or date. Continued use of the Service after changes take effect means you accept the revised terms, unless applicable law requires a different form of notice or consent.

        ## 16. Contact

        Questions about these terms should be sent to **{contact}** or to any updated legal contact published by the Operator on the Service.
        """
    ).strip()

    privacy = dedent(
        f"""
        # Privacy Policy

        Last updated: {{version_label}}

        This Privacy Policy explains how the Operator of **{site}** handles personal data when you visit or use the Service. The primary privacy contact for this deployment is **{contact}** unless the Operator publishes a different privacy contact.

        ## 1. Who controls your data

        The Operator of this deployment of the Service is the data controller for personal data processed through the Service, unless the Operator clearly states otherwise.

        dChat is software. Each site operator is responsible for how they configure and use the software, including any optional third-party services they enable.

        ## 2. Personal data we process

        Depending on how the Service is configured and how you use it, the Operator may process:

        ### Account and identity data

        - username;
        - email address;
        - password hash;
        - account status and role or permissions;
        - legal consent records; and
        - direct-message preferences.

        ### Profile data

        - avatar image;
        - bio;
        - website URL;
        - social profile links or handles; and
        - profile customization choices.

        ### Community content

        - thread titles and bodies;
        - replies, quotes, mentions, votes, tags, and notifications;
        - uploaded files or images;
        - moderation reports and related notes; and
        - change history such as edit timestamps.

        ### Direct messages

        - conversation metadata;
        - sender and recipient details;
        - encrypted message bodies stored by the software; and
        - report or moderation information if a message is reported.

        ### Technical and usage data

        - IP address and device or browser information contained in server, security, or application logs;
        - timestamps and request metadata;
        - authentication and session data;
        - rate-limit and anti-abuse data; and
        - presence data such as recent activity or online status indicators.

        ### Cookie and similar technology data

        - essential cookie choices and session identifiers;
        - CSRF/security tokens; and
        - if enabled by the Operator, analytics or third-party embed related data.

        ## 3. How we collect personal data

        We collect personal data:

        - directly from you when you register, post, edit your profile, upload content, send direct messages, or contact the Operator;
        - automatically when you use the Service, through logs, sessions, security controls, and cookies; and
        - from other users when they mention you, message you, report content, or otherwise interact with your account or content.

        ## 4. Why we process personal data and legal bases

        Depending on your location and the applicable law, the Operator may rely on one or more of the following legal bases:

        ### Contract

        We process personal data where necessary to provide the Service you request, including account login, hosting posts, showing profiles, delivering direct messages, and maintaining core forum functionality.

        ### Legitimate interests

        We may process data where necessary for legitimate interests such as:

        - operating, securing, and improving the Service;
        - preventing fraud, spam, abuse, and unauthorized access;
        - moderating content and enforcing community rules;
        - maintaining backups, logs, and system integrity;
        - handling user support and complaints; and
        - understanding feature reliability and performance.

        Where required, the Operator should balance these interests against users' rights and freedoms.

        ### Consent

        We may rely on consent where required, such as for optional non-essential cookies, optional email digests, or optional third-party services. You can withdraw consent at any time, but this does not affect processing already carried out lawfully before withdrawal.

        ### Legal obligation

        We may process personal data where necessary to comply with legal obligations, lawful requests, court orders, or obligations relating to safety, record keeping, or regulatory compliance.

        ## 5. Public nature of community content

        Unless the Operator configures the Service differently, your username, profile details, threads, replies, uploads, votes, and other public interactions may be visible to other users, visitors, search engines, and archive tools.

        Please do not post personal data or confidential material that you do not want to be public.

        ## 6. Direct messages

        Direct messages are intended to be private between participants. The software stores message bodies in encrypted form at rest, but direct messages are **not** end-to-end encrypted.

        The Operator may access, review, preserve, or disclose direct messages where reasonably necessary to:

        - investigate abuse or security incidents;
        - handle reported messages;
        - comply with law or lawful requests;
        - restore systems or backups; or
        - maintain or secure the Service.

        ## 7. Who personal data may be shared with

        Personal data may be shared with:

        - hosting providers, infrastructure providers, and backup providers;
        - email or notification providers, if the Operator enables those features;
        - analytics or monitoring providers, if the Operator enables them;
        - third-party content providers when you load external embeds or links;
        - moderators and administrators where necessary for community management, security, and abuse handling; and
        - courts, regulators, law enforcement, or advisors where legally required or reasonably necessary to protect rights, safety, or the Service.

        We do not describe every possible processor in this default policy. Operators should add site-specific provider details where required by law.

        ## 8. International transfers

        The Service may be hosted or administered from countries outside your own. Where personal data is transferred internationally, the Operator should use an appropriate transfer mechanism where required by applicable law.

        ## 9. Data retention

        The Operator may retain personal data for as long as reasonably necessary for the purposes described above, including to operate the Service, enforce rules, resolve disputes, maintain backups, and comply with legal obligations.

        By default, retention may include:

        - account data: for as long as the account remains active, and for a reasonable period afterwards for security, abuse prevention, or compliance;
        - public posts and uploads: until deleted by the user, removed by the Operator, or the Service is shut down, subject to backups and legal obligations;
        - direct messages: until deleted, removed under policy, or no longer needed for service operation, backup, dispute handling, or abuse investigation;
        - moderation records and reports: as long as reasonably necessary for safety, enforcement, and compliance; and
        - logs and rate-limit records: for as long as reasonably necessary for security, troubleshooting, and abuse prevention.

        Operators should customize retention periods if they adopt fixed schedules.

        ## 10. Your rights

        Depending on your jurisdiction, you may have rights to:

        - access your personal data;
        - correct inaccurate data;
        - delete certain data;
        - restrict certain processing;
        - object to certain processing;
        - receive a portable copy of certain data;
        - withdraw consent where processing is based on consent; and
        - complain to a supervisory authority or regulator.

        The Service includes account export and deletion tools, but some requests may still require manual review by the Operator.

        If you are in the UK, you may have rights under UK GDPR and may complain to the Information Commissioner's Office. If you are in the EEA, you may complain to your local supervisory authority. Users elsewhere may have additional rights under local law, including some US state privacy laws.

        ## 11. Security

        The Operator uses administrative, technical, and organizational measures intended to protect personal data. No method of transmission, storage, or security control is completely secure, and the Operator cannot guarantee absolute security.

        ## 12. Children

        The Service is not intended for children below the minimum age allowed by applicable law. If you believe a child has provided personal data unlawfully, contact the Operator so the data can be reviewed and, where appropriate, removed.

        ## 13. Changes to this policy

        The Operator may update this Privacy Policy from time to time. The current version will be published on the Service with an updated version number or date.

        ## 14. Contact

        Privacy questions, rights requests, and complaints should be sent to **{contact}** or to any updated privacy contact published by the Operator.
        """
    ).strip()

    cookies = dedent(
        f"""
        # Cookie Policy

        Last updated: {{version_label}}

        This Cookie Policy explains how **{site}** uses cookies and similar technologies. The primary contact for cookie-related questions is **{contact}** unless the Operator publishes a different contact.

        ## 1. What cookies are

        Cookies are small text files stored on your device. Similar technologies may include local storage, pixels, scripts, SDKs, or embedded third-party content that stores or accesses information on your device.

        ## 2. Cookies used by the software by default

        A standard dChat deployment may use the following **essential** cookies:

        - **`sessionid`**: keeps you signed in and maintains your session;
        - **`csrftoken`**: helps protect forms and requests against CSRF attacks; and
        - **`cookie_consent`**: remembers your cookie banner choice.

        These cookies are generally necessary for security, authentication, and core site operation.

        ## 3. Optional cookies and similar technologies

        Depending on how the Operator configures the Service, the Service may also use or load:

        - analytics or performance tools;
        - email, notification, or support integrations;
        - third-party embeds or widgets, including services such as YouTube, Twitch, TikTok, or X/Twitter; and
        - other third-party services chosen by the Operator.

        Those technologies may place their own cookies or collect data directly from your browser or device.

        ## 4. Legal basis and consent

        Essential cookies may be used where they are necessary to provide the Service, maintain security, or remember basic preferences.

        Where law requires consent for **non-essential** cookies or similar technologies, the Operator should obtain that consent before loading them. This is particularly relevant for analytics, advertising technologies, and many third-party embeds or widgets.

        This default software policy does not guarantee that every deployment is configured the same way. Operators should review their actual integrations and update this policy and consent flow if they enable additional technologies.

        ## 5. Why cookies and similar technologies are used

        Cookies and similar technologies may be used to:

        - authenticate users and maintain sessions;
        - protect forms and prevent abuse;
        - remember cookie choices or basic preferences;
        - improve performance and reliability;
        - understand feature usage where analytics are enabled; and
        - display embedded media or third-party content.

        ## 6. How to manage cookies

        You can usually control cookies through your browser settings, including blocking or deleting existing cookies. Blocking essential cookies may cause login, security, messaging, or other core parts of the Service to stop working correctly.

        If the Operator enables non-essential cookies, additional consent choices may be provided on the Service as required by law.

        ## 7. Third-party services

        When you view or interact with embedded third-party content, those providers may set cookies or collect information in line with their own policies. The Operator does not control those providers.

        You should review the privacy and cookie policies of any third-party service you interact with through the Service.

        ## 8. Changes to this policy

        The Operator may update this Cookie Policy from time to time. The current version will be published on the Service with an updated version number or date.

        ## 9. Contact

        Questions about this Cookie Policy should be sent to **{contact}** or to any updated contact published by the Operator.
        """
    ).strip()

    return {
        "terms": {
            "title": "Terms of Service",
            "version": "v2",
            "body_markdown": terms.replace("{version_label}", "v2"),
        },
        "privacy": {
            "title": "Privacy Policy",
            "version": "v2",
            "body_markdown": privacy.replace("{version_label}", "v2"),
        },
        "cookies": {
            "title": "Cookie Policy",
            "version": "v2",
            "body_markdown": cookies.replace("{version_label}", "v2"),
        },
    }
