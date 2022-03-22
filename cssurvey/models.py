# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User


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
    employee_name = models.CharField(max_length=255, blank=True, null=True)
    office_id = models.IntegerField(blank=True, null=True)
    job_position = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.employee_name

    class Meta:
        managed = False
        db_table = 'tb_employees'
