# Return all students with their notes (INNER JOIN).

select(Student, Note).join(Note)

# Return all students, even those without notes (LEFT OUTER JOIN).

select(Student, Note).outerjoin(Note)

# Return only student names and note titles.

select(Student.name , Note.title).join(Note)

# Return all notes belonging to the student named "Yadnyesh".

select(Student, Note).join(Note).where(Student.name == "Yadnyesh")