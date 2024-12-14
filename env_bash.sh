#!/bin/bash

# Export environment variables
export SECRET_KEY='my_secret_key'
export DATABASE_URL='sqlite:///site.db'
export DEBUG='True'
export WEB_ENV='dev'
export WEB_MYSQL_USER='web_admin'
export WEB_MYSQL_PWD='Testpassword6.'
export WEB_MYSQL_HOST='localhost'
export WEB_MYSQL_DB='web_db'


# Print the variables to verify
echo "SECRET_KEY: $SECRET_KEY"
echo "DATABASE_URL: $DATABASE_URL"
echo "DEBUG: $DEBUG"
echo "WEB_ENV: $WEB_ENV"
echo "WEB_MYSQL_USER: $WEB_MYSQL_USER"
echo "WEB_MYSQL_PWD: $WEB_MYSQL_PWD"
echo "WEB_MYSQL_HOST: $WEB_MYSQL_HOST"
echo "WEB_MYSQL_DB: $WEB_MYSQL_DB"