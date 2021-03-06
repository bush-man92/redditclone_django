# Generated by Django 3.0.3 on 2020-02-11 13:30

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_comments', '0003_add_submit_date_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='MPTTComment',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_comments.Comment')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='redditclone.MPTTComment')),
                ('tread', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='redditclone.Tread')),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
            },
            bases=('django_comments.comment', models.Model),
        ),
    ]
