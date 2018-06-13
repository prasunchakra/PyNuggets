"""
Works Smoothly on python 2.7
pip install validate_email
pip install pyDNS
"""
from validate_email import validate_email
is_valid = validate_email('you@domain.com',verify=True)
if is_valid:
    print "Email Exists"
else:
    print "Email doesn't Exists"
