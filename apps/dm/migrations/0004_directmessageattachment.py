from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dm", "0003_indexes_and_ordering"),
    ]

    operations = [
        migrations.CreateModel(
            name="DirectMessageAttachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="dm-attachments/%Y/%m/")),
                ("original_name", models.CharField(max_length=255)),
                ("mime_type", models.CharField(max_length=120)),
                ("size_bytes", models.PositiveIntegerField()),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "message",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="attachments", to="dm.directmessage"),
                ),
            ],
            options={
                "ordering": ["uploaded_at"],
            },
        ),
        migrations.AddIndex(
            model_name="directmessageattachment",
            index=models.Index(fields=["message", "uploaded_at"], name="dm_attach_message_idx"),
        ),
    ]
