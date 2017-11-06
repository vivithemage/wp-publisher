#!/usr/bin/env bash
# variables: ssh_username, database_name, mysql_password
echo "Starting Software installations";
apt-get install unzip -y;
apt-get install php-mbstring -y;
apt-get install php-gd -y;
apt-get install php-imagick -y;
echo "Creating Users";
sudo adduser --disabled-password --gecos "" thrive;
echo thrive:thrive | chpasswd;
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