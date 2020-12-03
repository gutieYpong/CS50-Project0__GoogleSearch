# Generated by Django 3.1.3 on 2020-12-02 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201202_1920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bidder',
            old_name='item_id',
            new_name='bidder_item',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user_name',
        ),
        migrations.AddField(
            model_name='comment',
            name='commet_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commentitem', to='auctions.listing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='commet_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commentname', to='auctions.user'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='comment',
            name='item_comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='item_comment',
            field=models.CharField(default='TEST COMMENT.', max_length=300),
            preserve_default=False,
        ),
    ]
