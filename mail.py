#使用email_validator
from email_validator import validate_email, EmailNotValidError

def check(email):
    try:
        v = validate_email(email)
        email = v["email"]
        return 1
    except EmailNotValidError as e:
        return 0

