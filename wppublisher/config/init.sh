echo "Starting Software installations";
apt-get update -y;
apt-get upgrade -y;
apt-get install unzip -y;
apt-get install php-mbstring -y;
apt-get install php-gd -y;
apt-get install php-imagick -y;
apt-get install automysqlbackup -y;

echo "Creating Users"
sudo adduser --disabled-password --gecos "" thrive;
echo thrive:thrive | chpasswd;

echo "Creating Folders and setting permissions";
mkdir -v /home/thrive/public_html;
mkdir -v /home/thrive/SQL;
mkdir -v /home/thrive/SSL;
chown -R --verbose thrive /home/thrive/;
chown -R --verbose thrive:www-data /home/thrive/public_html/;
chown -R --verbose thrive:www-data /home/thrive/SSL;
chmod -R --verbose 775 public_html/;

echo "Importing database";
mysql -u root -p wp_database < wp_database.sql;

echo "Setting up webserver"
rm /etc/nginx/sites-enabled/digitalocean;
/etc/init.d/nginx restart;