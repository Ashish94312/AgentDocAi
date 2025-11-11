from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mcp_manager", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="GeneratedDocument",
        ),
        migrations.DeleteModel(
            name="GitHubRepository",
        ),
    ]
