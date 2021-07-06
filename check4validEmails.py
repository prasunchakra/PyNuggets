# -*- coding: utf-8 -*-
"""
@author: prasunchakra
Based on RFC 2822 Section 3.4.1 (http://tools.ietf.org/html/rfc2822#section-3.4.1)
with the help of http://www.regular-expressions.info/email.html
"""
import re

def is_valid_email(email):
    """
    (?: ... ): Non-capturing group.
    [a-z0-9!#$%&'*+/=?^_{|}~-]+: Matches one or more lowercase letters, digits, or special characters from the set a-z0-9!#$%&'*+/=?^_{|}~-
    (?:\.[a-z0-9!#$%&'*+/=?^_{|}~-]+)*: Matches zero or more occurrences of a period (.`) followed by one or more lowercase letters, digits, or special characters.
    |: Alternation, matches either the previous pattern or the pattern that follows.
    "(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*": Matches a quoted string enclosed in double quotes ("). It allows certain special characters within the quotes, including control characters and escaped characters.
    (?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+: Matches one or more occurrences of a domain name component, separated by periods. Each component starts with a lowercase letter or digit and can contain zero or more lowercase letters, digits, or hyphens.
    [a-z0-9](?:[a-z0-9-]*[a-z0-9])?: Matches a domain name component, similar to the previous pattern.
    |: Alternation, matches either the previous pattern or the pattern that follows.
    \[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\]: Matches an IP address enclosed in square brackets ([ ]). It allows for IPv4 addresses in dotted decimal notation, IPv6 addresses, and IP addresses with domain names.
    :param email:
    :return:
    """
    pattern = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
    return re.match(pattern, email) is not None

if __name__ == '__main__':
    exampleEmails = ["test@example.com",
                        "john.doe@example.co.uk",
                        "user1234@domain-1234.net",
                        "first.last+label123@example.org",
                        '"user.name"@example.com',
                        "email@[192.168.0.1]",
                        "admin@[2001:db8::1]",
                        '"John Doe"@example.com',
                        "jdoe12345@subdomain.domain.co",
                        "user@localhost"]

    for email in exampleEmails:
        is_valid = is_valid_email(email)
        print(is_valid)


