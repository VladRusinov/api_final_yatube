# Generated by Django 3.2.16 on 2023-08-28 13:17

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_follow_unique_following'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(('user', django.db.models.expressions.F('following')), _negated=True), name='posts_follow_prevent_self_follow'),
        ),
    ]
