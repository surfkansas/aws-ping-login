# AWS Ping Login

This is just a simple tool I wrote to avoid havng to constantly scrape a web sessions to get my temporary AWS log-in credentials when logging into AWS via PING SSO.  It is installed as a pip package as follows:

```
pip install aws-ping-login
```

A sample execution is here:

```
aws-ping-login --sso-url https://sso.surfkansas.com/idp/startSSO.ping?PartnerSpId=urn:amazon:webservices --saml-provider PingFed --account 1234567890 --role surfking --region us-east-1 --session-duration 60 --profile surfkansas
```