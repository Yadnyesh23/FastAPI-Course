# 1.Get all active students.

select(Student).where(Student.is_active == True)


# 2.Get students whose age is between 18 and 25.

select(Student).where(Student.age.between(18, 25))

# 3.Get students whose names start with "A".
select(Student).where(Student.name.like("A%"))

# 4.Return the 10 youngest students.
select(Student).order_by(Student.age)

# 5.Count total students.
select(func.count(Student.id))