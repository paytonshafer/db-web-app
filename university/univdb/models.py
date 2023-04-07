# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=25, blank=True, null=True)
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    total_credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Student'


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=60, blank=True, null=True)
    dept = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept', blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'


class Department(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    building = models.CharField(max_length=10, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'


class Instructor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    dept = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept', blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor'

'''
class Prereq(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, related_name='course')
    prereq = models.ForeignKey(Course, models.DO_NOTHING, related_name='prereq')

    class Meta:
        managed = False
        db_table = 'prereq'
        unique_together = (('course', 'prereq'),)


class Section(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, related_name='course')
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    building = models.CharField(max_length=10, blank=True, null=True)
    room = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section'
        unique_together = (('course', 'sec_id', 'semester', 'year'),)


class Takes(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING)
    course = models.ForeignKey(Section, models.DO_NOTHING)
    sec = models.ForeignKey(Section, models.DO_NOTHING)
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year')
    grade = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'takes'
        unique_together = (('student', 'course', 'sec', 'semester', 'year'),)


class Teaches(models.Model):
    course = models.ForeignKey(Section, models.DO_NOTHING)
    sec = models.ForeignKey(Section, models.DO_NOTHING)
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year')
    teacher = models.ForeignKey(Instructor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'teaches'
        unique_together = (('course', 'sec', 'semester', 'year', 'teacher'),)
'''