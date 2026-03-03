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
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('author_name', models.CharField(max_length=200)),
                ('isbn', models.CharField(blank=True, max_length=13)),
                ('genre', models.CharField(blank=True, max_length=100)),
                ('published_year', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
