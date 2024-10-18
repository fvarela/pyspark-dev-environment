from simple_salesforce import Salesforce
import os

def sf_login(user, password, security_token):
    sf = Salesforce(
        username=user,
        password=password,
        security_token=security_token
    )
    return sf


if __name__ == '__main__':
    user = os.environ.get('SALESFORCE_USER')
    password = os.environ.get('SALESFORCE_PASSWORD')
    security_token = os.environ.get('SALESFORCE_TOKEN')
    sf = sf_login(user, password, security_token)
    pass
    