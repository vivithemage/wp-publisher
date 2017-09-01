apt-get update -y;
apt-get upgrade -y;
sudo adduser --disabled-password --gecos "" thrive;
echo thrive:thrive | chpasswd;
mkdir -v /home/thrive/public_html;
mkdir -v /home/thrive/SQL;
mkdir -v /home/thrive/SSL;
chown -R --verbose thrive /home/thrive/;
chown -R --verbose thrive:www-data /home/thrive/public_html/;
chown -R --verbose thrive:www-data /home/thrive/SSL;
chmod -R --verbose 775 public_html/;
mysql -u root -p three_counties < three_counties.sql;
cp --verbose /etc/nginx/sites-enabled/digitalocean /etc/nginx/sites-enabled/three_counties;
/etc/init.d/nginx restart;

