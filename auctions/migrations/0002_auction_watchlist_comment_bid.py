# Generated by Django 4.1.3 on 2022-11-17 06:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('current_bid', models.DecimalField(decimal_places=2, default=1.0, max_digits=12, validators=[django.core.validators.MinValueValidator(0.1)])),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('FSH', 'fashion'), ('OUT', 'outdoors'), ('TOY', 'toys'), ('BOK', 'books'), ('TOL', 'tools'), ('DEC', 'decorations'), ('SRV', 'services'), ('ELC', 'electronics'), ('NSP', 'unspecified')], default='NSP', max_length=3)),
                ('closed', models.BooleanField(default=False)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(help_text='Please be respectful in your comment and try to be helpful.')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]