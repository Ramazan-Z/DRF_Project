# Generated by Django 5.1.3 on 2024-12-02 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0004_alter_user_groups_alter_user_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="pyment",
            name="payment_url",
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name="Ссылка на платеж"),
        ),
        migrations.AddField(
            model_name="pyment",
            name="session_id",
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name="Идентификатор платежа"),
        ),
        migrations.AlterField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Designates whether this user should be treated as active.",
                verbose_name="active",
            ),
        ),
    ]
