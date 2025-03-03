# Generated by Django 5.1.2 on 2024-10-24 00:12

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('contact_primary', models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator(regex='\\d+')])),
                ('experience', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('id_code', models.CharField(max_length=10)),
                ('exp_needed', models.PositiveIntegerField(default=0)),
                ('technology', models.TextField(default='')),
                ('location', models.CharField(default='Pune', max_length=100)),
                ('j_type', models.CharField(choices=[('P', 'Permanent'), ('T', 'Temporary'), ('I', 'Intern')], default='P', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300, verbose_name='Description')),
                ('difficulty', models.CharField(choices=[('H', 'Hard'), ('M', 'Medium'), ('E', 'Easy')], default='M', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='QuestionSet', max_length=200)),
                ('times_taken', models.IntegerField(default=0, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='RatingSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('rate_min', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('rate_max', models.IntegerField(default=6, validators=[django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator(regex='\\d+')])),
                ('address', models.TextField()),
                ('v_type', models.CharField(choices=[('O', 'Online'), ('R', 'Reference'), ('RS', 'Recruitment Service'), ('OT', 'Other'), ('N', 'None')], default='N', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='resumes/')),
                ('upload_to', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Evaluator.candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('AC', 'Active'), ('CN', 'Cancelled'), ('FN', 'Finished')], default='AC', max_length=2)),
                ('result', models.CharField(choices=[('S', 'Selected'), ('R', 'Rejected'), ('J', 'Joined'), ('DNJ', 'Did Not Join'), ('TBD', 'Pending')], default='TBD', max_length=3)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Evaluator.candidate')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Evaluator.position')),
                ('question_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.questionset')),
            ],
        ),
        migrations.CreateModel(
            name='InterviewRatingSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='MySheet', max_length=200)),
                ('comment', models.TextField(default='', null=True)),
                ('interview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.interview')),
            ],
        ),
        migrations.CreateModel(
            name='JobOpening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_openings', models.PositiveIntegerField(default=1)),
                ('posted_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Evaluator.position')),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='position_applied',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Evaluator.position'),
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(max_length=128, verbose_name="Answer's text")),
                ('correct', models.BooleanField(default=True, verbose_name='Correct')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.question')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='qset',
            field=models.ManyToManyField(to='Evaluator.questionset'),
        ),
        migrations.CreateModel(
            name='HistoricalInterview',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('AC', 'Active'), ('CN', 'Cancelled'), ('FN', 'Finished')], default='AC', max_length=2)),
                ('result', models.CharField(choices=[('S', 'Selected'), ('R', 'Rejected'), ('J', 'Joined'), ('DNJ', 'Did Not Join'), ('TBD', 'Pending')], default='TBD', max_length=3)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('candidate', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Evaluator.candidate')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('position', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Evaluator.position')),
                ('question_set', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='Evaluator.questionset')),
            ],
            options={
                'verbose_name': 'historical interview',
                'verbose_name_plural': 'historical interviews',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='RatingAspect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True, default='', null=True)),
                ('points', models.PositiveIntegerField(default=0)),
                ('expected_points', models.PositiveIntegerField(default=0)),
                ('interview_rating_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Evaluator.interviewratingsheet')),
            ],
        ),
        migrations.AddField(
            model_name='position',
            name='rating_sheet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.ratingsheet'),
        ),
        migrations.CreateModel(
            name='Aspect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='', null=True)),
                ('expected_rate', models.PositiveIntegerField(default=1)),
                ('rating_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Evaluator.ratingsheet')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('contact_time', models.TimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('comments', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('round_type', models.CharField(choices=[('CV', 'CV Review'), ('U', 'Undecided'), ('F2F', 'Face to Face'), ('SKYPE', 'Skype Call'), ('TP', 'Telephonic'), ('VC', 'Client Video Call'), ('FD', 'Final Discussion'), ('HR', 'HR Discussion'), ('Other', 'Other Types')], default='U', max_length=10)),
                ('result', models.CharField(choices=[('ADV', 'Advanced'), ('RJ', 'Rejected'), ('CN', 'Cancelled'), ('DNA', 'Did Not Appear'), ('DNO', 'Did Not Accept Offer'), ('RS', 'Rescheduled'), ('W', 'Waiting'), ('S', 'Selected'), ('OH', 'On Hold')], default='W', max_length=5)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Evaluator.interview')),
                ('supporting_interviewer', models.ManyToManyField(blank=True, related_name='supporters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='interviewratingsheet',
            name='round_name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.round'),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('position', models.ManyToManyField(to='Evaluator.position')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='skill',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.skill'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='skill',
            field=models.ManyToManyField(blank=True, to='Evaluator.skill'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.vendor'),
        ),
    ]
