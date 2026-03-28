from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dm", "0002_directmessagepreference"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="directconversation",
            index=models.Index(fields=["updated_at"], name="dm_convo_updated_idx"),
        ),
        migrations.AddIndex(
            model_name="directmessage",
            index=models.Index(fields=["conversation", "created_at"], name="dm_message_convo_idx"),
        ),
        migrations.AddIndex(
            model_name="directmessage",
            index=models.Index(fields=["recipient", "is_read", "created_at"], name="dm_message_recipient_idx"),
        ),
    ]
