# Generated by Django 4.0.6 on 2023-02-07 19:10

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
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_banned', models.BooleanField(default=False)),
                ('ban_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(blank=True, max_length=100, null=True)),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=500, null=True)),
                ('marks', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(blank=True, max_length=100, null=True)),
                ('test_duration', models.CharField(blank=True, max_length=100, null=True)),
                ('is_ongoing', models.BooleanField(default=False)),
                ('is_register_allowed', models.BooleanField(default=False)),
                ('pass_percentage', models.CharField(blank=True, default=70, max_length=100, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('started_at', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='StudentMarking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.option')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(blank=True, max_length=100, null=True)),
                ('outcome', models.BooleanField(default=False)),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/q_images')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='test_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.test'),
        ),
        migrations.AddField(
            model_name='option',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.question'),
        ),
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ban_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('ban_count', models.CharField(blank=True, default='0', max_length=100, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('test_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.customuser')),
            ],
        ),
    ]
