# coding:utf-8

import os
import sys

# Setup project settings location to storage location
sys.path.append("F:\\PythonWorkplace\\track_progress")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "track_progress.settings")

'''
Django version greater than 1.7 must add the following codes
import django
django.setup()
Or will pop up exception: django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''
import django

if django.VERSION >= (1, 7):  # Identify django version
    django.setup()

from tracking_system.models import Student, List, Process
import xlrd  # excel read plugin

data = xlrd.open_workbook('student_info.xlsx')  # Open File
table = data.sheet_by_index(0)  # Fetch table
nrows = table.nrows  # Row
ncols = table.ncols  # Colomn
colnames = table.row_values(0)
x = y = z = 0
for i in range(1, nrows):
    row = table.row_values(i)  # Get value from each row
    for j in range(0, ncols):
        if type(row[j]) == float:  # convert float number into integer, or the number will be show like : 1.0
            row[j] = int(row[j])
    if row:  # Check if row value is null
        if Student.objects.filter(email=row[2]).exists():  # Check if row value is replied
            x = x + 1  # Not replied Counting
        else:
            y = y + 1  # Replied Counting
            # Create user instance in Django model
            print("student group is: "+row[4])
            student = Student.objects.create_user(first_name=row[0], last_name=row[1], username=row[2], email=row[2], password=str(row[3]), group=row[4])
            if (student.group == "Fall"):
                list = List.objects.filter(fall_due_date__isnull=False)
            else:
                list = List.objects.filter(winter_due_date__isnull=False)

            for item in list:
                Process(list=item, student=student).save()
else:
    z = z + 1  # empty line counting
# Student.objects.bulk_create(WorkList)
print('Successfully imported:' + str(y) + ', Replied: ' + str(x) + ', Line of Empty:' + str(z) + '!')
