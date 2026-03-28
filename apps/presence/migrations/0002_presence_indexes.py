from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("presence", "0001_initial"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="userpresence",
            index=models.Index(fields=["is_online", "last_seen_at"], name="presence_online_idx"),
        ),
    ]
