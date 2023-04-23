# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Dept(models.Model):
    dept_name = models.CharField(primary_key=True, max_length=50)
    building = models.CharField(max_length=20, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'

    def __str__(self):
        return self.dept_name


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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


class Instructor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    dept_name = models.ForeignKey(Dept, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor'


class Teaches(models.Model):
    course_id = models.CharField(primary_key=True, max_length=8)
    sec_id = models.CharField(max_length=8, null=False)
    semester = models.IntegerField(null=False)
    year = models.IntegerField(null=False)
    teacher_id = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course_id', 'sec_id', 'semester', 'year', 'teacher_id'], name='teaches_primary_key'
            )
        ]
        managed = False
        db_table = 'teaches'


class Takes(models.Model):
    student_id = models.IntegerField(primary_key=True)
    course_id = models.CharField(max_length=8, null=False)
    sec_id = models.CharField(max_length=8, null=False)
    semester = models.IntegerField(null=False)
    year = models.IntegerField(null=False)
    grade = models.CharField(max_length=8, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student_id', 'course_id', 'sec_id', 'semester', 'year'], name='takes_primary_key'
            )
        ]
        managed = False
        db_table = 'takes'


class ResearchFunds(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20, null=False)
    funds = models.IntegerField(null=False)
    agency = models.CharField(max_length=20)
    beg_date = models.DateField()
    end_date = models.DateField()
    manager_approval = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id', 'title'], name='researchfunds_primary_key'
            )
        ]
        managed = False
        db_table = 'researchfunds'


class Published(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20, null=False)
    published = models.IntegerField(null=False)
    year = models.IntegerField()
    publication_venue = models.CharField(max_length=20)
    publication_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id', 'title'], name='published_primary_key'
            )
        ]
        managed = False
        db_table = 'published'


class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    dept_name = models.ForeignKey(Dept, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    total_credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'
