# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 22, 22, 40, 46, 225675, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
