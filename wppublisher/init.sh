# site_name
# ssh_username
# database_name

apt-get update -y;
apt-get upgrade -y;
sudo adduser --disabled-password --gecos "" thrive
echo thrive:thrive | chpasswd
mkdir /home/thrive/public_html
mkdir /home/thrive/SQL
mkdir /home/thrive/SSL
chown -R thrive /home/thrive/
# pull through root login details from /root/.digitalocean_password
# upload files over sftp
chown -R thrive:www-data /home/thrive/public_html/
chown -R thrive:www-data /home/thrive/SSL
chmod -R 775 public_html/
# create database three counties
mysql -u root -p three_counties < three_counties.sql
#generate SSL - see 1.0
rm /etc/nginx/sites-enabled/digitalocean
touch /etc/nginx/sites-enabled/three_counties
# Copy nginx config file to config
/etc/init.d/nginx restart

