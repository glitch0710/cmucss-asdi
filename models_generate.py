# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TbCmuoffices(models.Model):
    officeid = models.AutoField(db_column='officeID', primary_key=True)  # Field name made lowercase.
    officename = models.TextField(db_column='officeName', blank=True, null=True)  # Field name made lowercase.
    officecode = models.TextField(db_column='officeCode', blank=True, null=True)  # Field name made lowercase.
    scope = models.TextField(blank=True, null=True)

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

    class Meta:
        managed = False
        db_table = 'tb_cmuofficials'


class TbCoverage(models.Model):
    coverageid = models.AutoField(db_column='coverageID', primary_key=True)  # Field name made lowercase.
    from_field = models.DateField(db_column='from')  # Field renamed because it was a Python reserved word.
    to = models.DateField()

    class Meta:
        managed = False
        db_table = 'tb_coverage'


class TbCssrespondents(models.Model):
    respondentid = models.AutoField(db_column='respondentID', primary_key=True)  # Field name made lowercase.
    respondentname = models.TextField(db_column='respondentName', blank=True, null=True)  # Field name made lowercase.
    respondenttype = models.TextField(db_column='respondentType', blank=True, null=True)  # Field name made lowercase.
    responddate = models.DateField(db_column='respondDate', blank=True, null=True)  # Field name made lowercase.
    employee_id = models.IntegerField(blank=True, null=True)
    coverageid = models.ForeignKey(TbCoverage, models.DO_NOTHING, db_column='coverageID', blank=True, null=True)  # Field name made lowercase.
    respondedofficeid = models.ForeignKey(TbCmuoffices, models.DO_NOTHING, db_column='respondedOfficeID', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_cssrespondents'


class TbCssrespondentsDetails(models.Model):
    crid = models.AutoField(db_column='CRID', primary_key=True)  # Field name made lowercase.
    qid = models.ForeignKey('TbQuestions', models.DO_NOTHING, db_column='QID')  # Field name made lowercase.
    respondentid = models.ForeignKey(TbCssrespondents, models.DO_NOTHING, db_column='respondentID')  # Field name made lowercase.
    rating = models.CharField(max_length=10)
    date_created = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_cssrespondents_details'


class TbEmployees(models.Model):
    eid = models.AutoField(db_column='EID', primary_key=True)  # Field name made lowercase.
    office_id = models.IntegerField(blank=True, null=True)
    job_position = models.CharField(max_length=255, blank=True, null=True)
    user = models.IntegerField(blank=True, null=True)
    middlename = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_employees'


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
    display_status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_questions'
