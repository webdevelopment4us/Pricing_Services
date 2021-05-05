# Pricing Services

This is an application built to allow the periodic scanning of online webstores, to notify users of changes in prices of items they select.

This application is developed as a part of the "Web developer Bootcamp with Flask and Python. 

It allows administrators (defined via src/config.py) to add, remove, and edit online stores.

You will need a Mailgun account and API details for the e-mailing to work. E-mails are sent via executing the src/alert_updater.py file. In order to check e.g. every 10 minutes, the file must be executed every 10 minutes. This can be done with a cron job or a Windows service (Not Implemented)

It parses the store websites using requests and BeautifulSoup.

It does not work with Stores that dynamically inject content using JavaScript.

It allows users to register, log in, and create and modify their alerts.

Technology stack: MongoDB, Python (Flask & Jinja2), HTML/CSS/Bootstrap, Mailgun.# Pricing_Services
