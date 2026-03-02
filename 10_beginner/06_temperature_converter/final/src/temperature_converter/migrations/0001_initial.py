from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_in', models.DecimalField(decimal_places=4, max_digits=10)),
                ('unit_in', models.CharField(choices=[('C', 'Celsius'), ('F', 'Fahrenheit'), ('K', 'Kelvin')], max_length=10)),
                ('value_out', models.DecimalField(decimal_places=4, max_digits=10)),
                ('unit_out', models.CharField(choices=[('C', 'Celsius'), ('F', 'Fahrenheit'), ('K', 'Kelvin')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
