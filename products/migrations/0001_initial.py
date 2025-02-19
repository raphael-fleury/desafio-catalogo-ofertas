# Generated by Django 5.1.5 on 2025-02-08 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('link', models.URLField()),
                ('image', models.URLField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('installment_options', models.CharField(blank=True, max_length=100)),
                ('delivery_type', models.CharField(choices=[('Full', 'Full'), ('Normal', 'Normal')], max_length=50)),
                ('free_shipping', models.BooleanField(default=False)),
            ],
        ),
    ]
