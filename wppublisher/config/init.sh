#!/usr/bin/env bash
# variables: ssh_username, database_name, mysql_password
echo "Starting Software installations";
apt-get install unzip -y;
apt-get install php-mbstring -y;
apt-get install php-gd -y;
apt-get install php-imagick -y;
apt-get install php-xml -y;
apt-get install proftpd -y;
apt-get install git -y;
echo "Extracting Uploaded Site to user directory";
cd /root;
unzip -o '*.zip' -d /home/thrive/;
echo "Creating Folders and setting permissions";
mkdir -v /home/thrive/public_html;
mkdir -v /home/thrive/SQL;
mkdir -v /home/thrive/SSL;
chown -R --verbose thrive /home/thrive/;
chown -R --verbose thrive:www-data /home/thrive/public_html/;
chown -R --verbose thrive:www-data /home/thrive/SSL;
chmod -R --verbose 775  /home/thrive/public_html/;
echo "editing SQL file to use the correct URL";
sed -i 's+localhost:8888+{site_url}+g' /home/thrive/SQL/{database_name}.sql;
sed -i 's+localhost%3A8888+{site_url}+g' /home/thrive/SQL/{database_name}.sql;
sed -i 's+localhost+{site_url}+g' /home/thrive/SQL/{database_name}.sql;
echo "Importing database";
mysql --user="root" --password="{mysql_password}" --execute="CREATE DATABASE {database_name};";
mysql --user="root" --password="{mysql_password}" {database_name} < /home/thrive/SQL/{database_name}.sql;
mysql --user="root" --password="{mysql_password}" --execute="ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{mysql_password}'";
echo "Restarting database server";
/etc/init.d/mysql restart;
echo "Setting up webserver";
rm /etc/nginx/sites-enabled/digitalocean;
/etc/init.d/nginx restart;
echo "Adding swap space";
fallocate -l 4G /swapfile;
chmod 600 /swapfile;
mkswap /swapfile;
swapon /swapfile;
cp /etc/fstab /etc/fstab.bak;
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab;
apt remove apache2 -y;

apt-get update
APP_PASS="{mysql_password}"
ROOT_PASS="{mysql_password}"
APP_DB_PASS="{mysql_password}"
echo "Installing phpmyadmin";
export DEBIAN_FRONTEND=noninteractive;
echo "phpmyadmin phpmyadmin/dbconfig-install boolean true" | debconf-set-selections;
echo "phpmyadmin phpmyadmin/app-password-confirm password $APP_PASS" | debconf-set-selections;
echo "phpmyadmin phpmyadmin/mysql/admin-pass password $ROOT_PASS" | debconf-set-selections;
echo "phpmyadmin phpmyadmin/mysql/app-pass password $APP_DB_PASS" | debconf-set-selections;
echo "phpmyadmin phpmyadmin/reconfigure-webserver multiselect nginx" | debconf-set-selections;

apt-get install -y phpmyadmin;
ln -s /usr/share/phpmyadmin /home/thrive/public_html/;
sed -i "s/|\s*\((count(\$analyzed_sql_results\['select_expr'\]\)/| (\1)/g" /home/thrive/public_html/phpmyadmin/libraries/sql.lib.php # fix stupid phpmyadmin syntax error

service nginx restart;

echo "Adding user dotfiles";
git clone https://github.com/vivithemage/dotfiles.git; 
cd dotfiles; 
bash install.sh 
chown -R thrive /home/thrive/dotfiles;
chmod -R 775 /home/thrive/dotfiles;

echo "Adding defibrillator";
cd /home/thrive;
git clone https://github.com/vivithemage/defibrillator.git;
cd defibrillator;
python install.py {site_url};

echo "DO Adding analytics"
curl -sSL https://repos.insights.digitalocean.com/install.sh | sudo bash

echo "Removing Snapd daemon due to it sometimes crashing and basically not being used (we use apt at the moment)"
systemctl stop snapd
apt-get remove snapd -y

echo "Installing advanced terminal for DO"
wget -qO- https://repos-droplet.digitalocean.com/install.sh | sudo bash
