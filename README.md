# ldform
CGI form handler used for LinuxDays web forms

This is an quick and dirty hack to get the form data stored to JSON files.
Every submission has to contain key `regid` linking to an existing directory in
the data directory. All data from each submission is then saved into a JSON file
named YYYYMMDD-HHMMSS-nnn.json where nnn is random nonce.

Request handling can be extended by creating a custom handler with some special
features like sending confirmation e-mail or mailing list subscription.

For extracting data, there is a convinience script `export.py` which exports
given form fields as a CSV file. Utility `losuj.py` can be used to draw a
submission by random.
