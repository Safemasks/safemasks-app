#! /usr/bin/env sh
set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=./IaC/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . $PRE_START_PATH
else
    echo "There is no script $PRE_START_PATH"
fi

git clone https://github.com/letsencrypt/letsencrypt ./letsencrypt

#run the installation , nginx config for SSL has been set up in entrypoint.sh
./letsencrypt/letsencrypt-auto certonly --standalone --email samimkhassan@gmail.com --agree-tos --no-eff-email -d portal.safemasks.de


# Start Supervisor, Django
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
