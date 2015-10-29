
def respond(data):
    """Generate HTML response"""
    print("Content-type: text/html; charset=UTF-8")
    print("""
<html>
<head>
    <meta http-equiv="refresh" content="3;/">
</head>
<body>
<h1>Your response has been recorded. Thank you.</h1>
<p>Redirecting you <a href="/">back home</a> in 3 seconds…</p>
</body>
</html>
    """)
