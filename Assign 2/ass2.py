import MySQLdb

db = MySQLdb.connect("localhost","14CS10061","btech14","14CS10061" )
cursor = db.cursor()




print "All  courses taught by PPC"
cursor.execute("SELECT COURSENAME FROM COURSE,TEACHES,TEACHER WHERE TEACHER.TEACHER_NAME='PPC'  AND  COURSE.COURSEID=TEACHES.COURSEID AND TEACHES.TEACHERID=TEACHER.TEACHERID;")
results = cursor.fetchall()

widths = []
columns = []
tavnit = '|'
separator = '+' 

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in results:
    print(tavnit % row)
print(separator)
print "\n"

print "All students registered in the courses taught by PPC"
cursor.execute("SELECT DISTINCT STUDENT.ROLLNUMBER,NAME FROM STUDENT,REGISTRATION,COURSE,TEACHES,TEACHER WHERE TEACHER.TEACHER_NAME='PPC'  AND  COURSE.COURSEID=TEACHES.COURSEID AND TEACHES.TEACHERID=TEACHER.TEACHERID  AND STUDENT.ROLLNUMBER=REGISTRATION.ROLLNUMBER AND REGISTRATION.COURSEID=COURSE.COURSEID;")
results = cursor.fetchall()

widths = []
columns = []
tavnit = '|'
separator = '+' 

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in results:
    print(tavnit % row)
print(separator)
print "\n"

print "The timings of all courses in Class-Room NC142."


cursor.execute("SELECT DISTINCT COURSE.COURSEID,COURSENAME,START_TIME,END_TIME,DAY FROM TIMING,TEACHES,CLASSROOM,COURSE WHERE CLASSROOM.ROOMNO='NC142' AND CLASSROOM.ROOMNO=TEACHES.ROOMNO AND TEACHES.SLOTID=TIMING.SLOTID AND TEACHES.COURSEID=COURSE.COURSEID;")
results = cursor.fetchall()

widths = []
columns = []
tavnit = '|'
separator = '+' 

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in results:
    print(tavnit % row)
print(separator)
print "\n"

print " The name of the students who received the highest marks in the courses taught by PPC"
cursor.execute("SELECT DISTINCT NAME FROM((SELECT NAME,GRADECARD.ROLLNUMBER FROM(SELECT COURSE.COURSEID,MAX(MARKS) AS MAXMARKS FROM STUDENT,REGISTRATION,COURSE,TEACHES,TEACHER,GRADECARD WHERE TEACHER.TEACHER_NAME='PPC' AND GRADECARD.ROLLNUMBER=REGISTRATION.ROLLNUMBER AND  COURSE.COURSEID=TEACHES.COURSEID AND TEACHES.TEACHERID=TEACHER.TEACHERID AND STUDENT.ROLLNUMBER=REGISTRATION.ROLLNUMBER AND REGISTRATION.COURSEID=COURSE.COURSEID AND COURSE.COURSEID=GRADECARD.COURSEID GROUP BY COURSE.COURSEID ) AS T,REGISTRATION,GRADECARD,STUDENT  WHERE T.COURSEID=REGISTRATION.COURSEID AND T.MAXMARKS=GRADECARD.MARKS AND GRADECARD.ROLLNUMBER=REGISTRATION.ROLLNUMBER AND STUDENT.ROLLNUMBER=REGISTRATION.ROLLNUMBER) AS T1);")
results = cursor.fetchall()

widths = []
columns = []
tavnit = '|'
separator = '+' 

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in results:
    print(tavnit % row)
print(separator)
print "\n"

print "The students who have received a grade of EX in the largest number of course"
cursor.execute("SELECT NAME,STUDENT.ROLLNUMBER FROM (SELECT MAX(NO_OF_EX) AS MAX_EX FROM (SELECT COUNT(*)AS NO_OF_EX,GRADECARD.ROLLNUMBER AS ROLLNO FROM GRADECARD WHERE GRADE='EX'GROUP BY GRADECARD.ROLLNUMBER ) AS T,STUDENT WHERE T.ROLLNO=STUDENT.ROLLNUMBER) AS T1,(SELECT COUNT(DISTINCT COURSEID)AS NO_OF_EX,GRADECARD.ROLLNUMBER AS ROLLNO FROM GRADECARD WHERE GRADE='EX' GROUP BY GRADECARD.ROLLNUMBER ) AS T2,STUDENT WHERE STUDENT.ROLLNUMBER=T2.ROLLNO AND T2.NO_OF_EX=T1.MAX_EX;")
results = cursor.fetchall()

widths = []
columns = []
tavnit = '|'
separator = '+' 

for cd in cursor.description:
    widths.append(max(cd[2], len(cd[0])))
    columns.append(cd[0])

for w in widths:
    tavnit += " %-"+"%ss |" % (w,)
    separator += '-'*w + '--+'

print(separator)
print(tavnit % tuple(columns))
print(separator)
for row in results:
    print(tavnit % row)
print(separator)
print "\n\n\n"
# disconnect from server
db.close()







