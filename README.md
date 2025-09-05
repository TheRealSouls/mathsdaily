# DailyMATHS.ie
#### Video Demo:  <URL HERE>
#### Description:

##### DailyMATHS.ie is, at its core, a website offering daily maths challenges. These are based on the Leaving Certificate curriculum, which is the traditional one in the Irish education system. However, people from many countries can still participate in its challenges. I created the website out of my passion for mathematics and particularly mathematics education. I believe that everyone can intrinsically love math.

##### Knowing that design was my strong point, I made sure to use this. However, with almost 10 webpages/external links, it was a lot to manage. I cleverly used Jinja to create two templates: one for auth and one for dashboard. The difference between the two is that auth is when you logged in, and dashboard is before it.

##### I debated between a white-blue colour scheme and a dark-red colour scheme. In the end, I chose the dark-red colour scheme as it is more easy on the eyes (white is like a flashbang nowadays!) and red is one of my favourite colours. I knew I had made the right choice, as maths as a subject is red, not blue!

##### The website's log-in system was implemented using Flask and SQL, as taught in CS50. First, you register and then you log in. Through much server-side form validation, your data is then stored in the Flask Session.

##### The contact page is fully functional, and all pages are sent to my email. This was done using Formspreee, woven into the form of my contact.html page.

##### Once you are fully logged in, you are presented with a homepage. This contains your statistics, such as your solved challenges and accuracy - these are fetched from SQL databases. It also contains the daily challenge, as well as a daily quote which can be further improved by implementing a quote database and alternating between the quotes; for now it is a static quote by Albert Einstein himself. If you have not solved it, you are allowed to solve it, otherwise, you are completely blocked from solving it. I even added back-end validation for this.

##### I created SQL tables (in dailymaths.db) to manage users, the challenges and the solved problems. I used relations between all these tables with their common properties, such as ID. How daily challenges work is that I have a date column for the challenges, and I check if the date is equal to today.

#### I have not implemented this as I would like to come back to this and deploy it as a full-stack web application later on. For now, this is the whole structure of my beta application though.

##### I used JavaScript mainly to fetch items from the database using AJAX, such is the case with the leaderboard to avoid browser refreshes. I also used it for animations, for example the math logos at the unauthenticated homepage.

##### To display any error messages, I used Flask's fetch function.

##### Once you solve a challenge, you send a query to the database to add to your points, accuracy and total solved problems. Then you wait for tomorrow!

##### Finally, I used some external CSS libraries like MathJax to import LaTeX and FontAwesome for icons.

##### In the future, if this becomes a full-scaled web app, I may have to implement a privacy policy and other meta into the website. The website lacks these at the moment.

##### This was DailyMATHS. See you next time!
