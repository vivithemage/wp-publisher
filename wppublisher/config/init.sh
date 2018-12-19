#!/usr/bin/env bash
# variables: ssh_username, database_name, mysql_password
echo "Starting Software installations";
apt-get install unzip -y;
apt-get install php-mbstring -y;
apt-get install php-gd -y;
apt-get install php-imagick -y;
apt-get install php-xml -y;
apt-get install vsftpd -y
echo "Extracting Uploaded Site to user directory";
cd /root;
unzip '*.zip' -d /home/thrive/;
echo "Creating Folders and setting permissions";
mkdir -v /home/thrive/public_html;
mkdir -v /home/thrive/SQL;
mkdir -v /home/thrive/SSL;
chown -R --verbose thrive /home/thrive/;
chown -R --verbose thrive:www-data /home/thrive/public_html/;
chown -R --verbose thrive:www-data /home/thrive/SSL;
chmod -R --verbose 775  /home/thrive/public_html/;
echo "Importing database";
mysql --user="root" --password="{mysql_password}" --execute="CREATE DATABASE {database_name};";
mysql --user="root" --password="{mysql_password}" {database_name} < /home/thrive/SQL/{database_name}.sql;
echo "Setting up webserver";
rm /etc/nginx/sites-enabled/digitalocean;
/etc/init.d/nginx restart;
echo "Adding swap space"
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
cp /etc/fstab /etc/fstab.bak
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

#apt-get update
#APP_PASS="{mysql_password}"
#ROOT_PASS="{mysql_password}"
#APP_DB_PASS="{mysql_password}"
## Install phpmyadmin
#export DEBIAN_FRONTEND=noninteractive;
#echo "phpmyadmin phpmyadmin/dbconfig-install boolean true" | debconf-set-selections;
#echo "phpmyadmin phpmyadmin/app-password-confirm password $APP_PASS" | debconf-set-selections;
#echo "phpmyadmin phpmyadmin/mysql/admin-pass password $ROOT_PASS" | debconf-set-selections;
#echo "phpmyadmin phpmyadmin/mysql/app-pass password $APP_DB_PASS" | debconf-set-selections;
#echo "phpmyadmin phpmyadmin/reconfigure-webserver multiselect nginx" | debconf-set-selections;

#apt-get install -y phpmyadmin;
#ln -s /usr/share/phpmyadmin /home/thrive/public_html/;
