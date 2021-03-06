# Generated by Django 2.2.4 on 2019-08-06 14:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queryKey', models.CharField(max_length=2000)),
                ('queryValue', models.CharField(max_length=2000)),
                ('overall_score', models.FloatField(default=0)),
                ('explanation', models.CharField(default='', max_length=200)),
                ('suggestion', models.CharField(max_length=2000)),
                ('status', models.CharField(default='New', max_length=100)),
                ('date_opened', models.DateTimeField(default=django.utils.timezone.now)),
                ('context', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queryName', models.CharField(max_length=200)),
                ('querySql', models.CharField(max_length=10000)),
                ('mostRecentRevision', models.IntegerField(default=-1)),
                ('auto_update_revision', models.BooleanField(default=True)),
                ('key_length', models.IntegerField(default=-1)),
                ('scoreThreshold', models.FloatField(default=0)),
                ('suggestion', models.BooleanField(default=True)),
                ('database_server', models.CharField(default='', max_length=2000)),
                ('database', models.CharField(default='', max_length=2000)),
                ('context_query', models.CharField(default='', max_length=10000)),
                ('use_neural_network', models.BooleanField(default=False)),
                ('most_recent_run_time', models.FloatField(default=0)),
                ('avg_run_time', models.FloatField(default=0)),
                ('num_recorded_runs', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='StatTechnique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statTechnique', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='StaticWeight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(default=0)),
                ('enabled', models.BooleanField(default=False)),
                ('queryID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Query')),
                ('statTechnique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.StatTechnique')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(default=0)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Issue')),
                ('statTechnique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.StatTechnique')),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='queryID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Query'),
        ),
        migrations.CreateModel(
            name='FreqMapEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tupleKey', models.CharField(max_length=2000)),
                ('tupleBucket', models.CharField(max_length=2000)),
                ('tupleValue', models.IntegerField(default=0)),
                ('queryID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Query')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='issue',
            unique_together={('queryID', 'queryValue')},
        ),
    ]
