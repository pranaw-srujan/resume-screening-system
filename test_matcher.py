from modules.matcher import calculate_match_score

job_description = """
We are looking for a skilled Python Developer with experience in Flask and Django
frameworks. The ideal candidate should have strong knowledge of MySQL databases,
REST APIs, and Git version control. Experience with machine learning libraries like
Scikit-learn and Pandas is a plus. Strong communication and teamwork skills required.
"""

resume_aditi = """
Final year Computer Science student with hands-on experience in building web
applications using Python and Flask. Skills: Python, Flask, Django, MySQL, HTML,
CSS, JavaScript, Git, Scikit-learn, Pandas, NumPy, Machine Learning, Data Analysis.
"""

resume_rohit = """
Java, Spring Boot, React, Node.js, MongoDB, AWS, Docker, REST APIs, Agile, JIRA.
Backend Developer Intern with experience building backend services using Java
and Spring Boot, deployed on AWS EC2.
"""

resume_sneha = """
SQL, Python, Excel, Power BI, Tableau, Data Visualization, Statistics, Pandas,
NumPy, Communication, Teamwork. Data Analyst Intern experience creating dashboards
and automating reports using Python scripts.
"""

print("Aditi's match score: ", calculate_match_score(resume_aditi, job_description))
print("Rohit's match score: ", calculate_match_score(resume_rohit, job_description))
print("Sneha's match score: ", calculate_match_score(resume_sneha, job_description))