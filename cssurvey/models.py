from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TbCmuoffices(models.Model):
    officeid = models.AutoField(db_column='officeID', primary_key=True)  # Field name made lowercase.
    officename = models.TextField(db_column='officeName', blank=True, null=True)  # Field name made lowercase.
    officecode = models.TextField(db_column='officeCode', blank=True, null=True)  # Field name made lowercase.
    scope = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.officename

    class Meta:
        managed = False
        db_table = 'tb_cmuoffices'


class TbCmuofficials(models.Model):
    officerid = models.AutoField(db_column='officerID', primary_key=True)  # Field name made lowercase.
    fname = models.TextField(blank=True, null=True)
    minitial = models.TextField(blank=True, null=True)
    lname = models.TextField(blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    officeunder = models.ForeignKey(TbCmuoffices, models.DO_NOTHING, db_column='officeUnder', blank=True, null=True)  # Field name made lowercase.
    signatories = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fname

    class Meta:
        managed = False
        db_table = 'tb_cmuofficials'


class TbCoverage(models.Model):
    coverageid = models.AutoField(db_column='coverageID', primary_key=True)  # Field name made lowercase.
    from_field = models.DateField(db_column='from')  # Field renamed because it was a Python reserved word.
    to = models.DateField()

    def __str__(self):
        return self.coverageid

    class Meta:
        managed = False
        db_table = 'tb_coverage'


class TbCssrespondents(models.Model):
    respondentid = models.AutoField(db_column='respondentID', primary_key=True)  # Field name made lowercase.
    respondentname = models.TextField(db_column='respondentName', blank=True, null=True)  # Field name made lowercase.
    respondenttype = models.TextField(db_column='respondentType', blank=True, null=True)  # Field name made lowercase.
    responddate = models.DateField(db_column='respondDate', blank=True, null=True, auto_now_add=True)  # Field name made lowercase.
    employee_id = models.IntegerField(blank=True, null=True)
    coverageid = models.ForeignKey(TbCoverage, models.DO_NOTHING, db_column='coverageID', blank=True, null=True)  # Field name made lowercase.
    respondedofficeid = models.ForeignKey(TbCmuoffices, models.DO_NOTHING, db_column='respondedOfficeID', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.respondentname

    class Meta:
        managed = False
        db_table = 'tb_cssrespondents'


class TbCssrespondentsDetails(models.Model):
    crid = models.AutoField(db_column='CRID', primary_key=True)  # Field name made lowercase.
    qid = models.ForeignKey('TbQuestions', models.DO_NOTHING, db_column='QID')  # Field name made lowercase.
    respondentid = models.ForeignKey(TbCssrespondents, models.DO_NOTHING, db_column='respondentID')  # Field name made lowercase.
    rating = models.CharField(max_length=10)
    date_created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    def __str__(self):
        return self.respondentid

    class Meta:
        managed = False
        db_table = 'tb_cssrespondents_details'


class TbLogs(models.Model):
    logid = models.AutoField(db_column='logID', primary_key=True)  # Field name made lowercase.
    accountid = models.IntegerField(db_column='accountID')  # Field name made lowercase.
    activity = models.TextField()
    datetime = models.TextField()

    class Meta:
        managed = False
        db_table = 'tb_logs'


class TbQuestions(models.Model):
    qid = models.AutoField(db_column='QID', primary_key=True)  # Field name made lowercase.
    survey_question = models.CharField(max_length=255, blank=True, null=True)
    datecreated = models.DateTimeField(db_column='dateCreated', blank=True, null=True)  # Field name made lowercase.
    display_status = models.BooleanField(default=False)  # This field type is a guess.

    def __str__(self):
        return self.survey_question

    class Meta:
        managed = False
        db_table = 'tb_questions'


class TbEmployees(models.Model):
    eid = models.AutoField(db_column='EID', primary_key=True)  # Field name made lowercase.
    office_id = models.ForeignKey('TbCmuoffices', models.DO_NOTHING, db_column='officeID')
    job_position = models.CharField(max_length=255, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='cssurvey/images/')

    def __str__(self):
        return self.user

    class Meta:
        managed = False
        db_table = 'tb_employees'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        TbEmployees.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



