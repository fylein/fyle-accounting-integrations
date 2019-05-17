# Generated by Django 2.2.1 on 2019-05-07 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fyle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='code1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='code2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='code3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='costcenter',
            name='code1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='costcenter',
            name='code2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='costcenter',
            name='code3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='code1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='code2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='code3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='code1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='code2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='code3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ImportBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('min_updated_at', models.DateTimeField()),
                ('advances', models.ManyToManyField(to='fyle.Advance')),
                ('expenses', models.ManyToManyField(to='fyle.Expense')),
            ],
        ),
        migrations.CreateModel(
            name='FyleImportConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_emails', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
