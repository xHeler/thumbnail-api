# Generated by Django 4.1.7 on 2023-03-08 15:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("memberships", "0003_alter_membership_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="membership",
            options={
                "permissions": [
                    ("can_do_custom_smth", "Can do sdfs"),
                    ("can_custom_dP_smth", "Can sdfsdf sdfs"),
                ]
            },
        ),
    ]