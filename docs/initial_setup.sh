#!/bin/bash -e

username=$1
password=`tr -dc A-Za-z0-9 < /dev/urandom | head -c 12 | xargs`
database_extension="_wp"
database=$username$database_extension
#domain=$username'.dev.vixre.co.uk'
domain=$3

url='http://'$domain
www_url='http://www.'$domain
mysql_root_password='root'

# ip's for web2.vixre.co.uk
server_ipv4='localhost'
server_ipv6='2001:41c8:51:428:fcff:ff:fe00:4625'

webserver_group='www-data'

clear
echo "
============================================
 User, SQL and Wordpress Install Script
 Vixre 2014
============================================"

# Add user
sudo adduser --disabled-password --gecos "" $username
echo $username:$password | sudo chpasswd

# Create database, user and set password
query="CREATE DATABASE $database; CREATE USER '$username'@'localhost' IDENTIFIED BY '$password'; GRANT ALL PRIVILEGES ON $database.* TO '$username'@'localhost'; FLUSH PRIVILEGES;"

echo $query
mysql --user="root" --password="$mysql_root_password" --execute="$query"

# create the vhost
if [ $2 = "apache2" ]
then
    vhost_filepath=/etc/apache2/sites-enabled/$domain
    server="apache2"

    # create the vhost (apache)
    sudo echo "<VirtualHost *:80>
            ServerAdmin you@vixre.co.uk
            ServerName $domain
            ServerAlias www.$domain
            DocumentRoot /home/$username/public_html/
            <Directory /home/$username/public_html/>
                    Options MultiViews Indexes FollowSymLinks
                    AllowOverride all
            </Directory>
    </VirtualHost>" > $vhost_filepath

    htaccess_content="# BEGIN WordPress
    <IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.php$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.php [L]
    </IfModule>

    # END WordPress"
else
    vhost_filepath=/etc/nginx/sites-enabled/$domain
    server="nginx"

    echo "entering into nginx vhost file"
    # create the vhost (nginx)
    sudo echo "server {
            listen 80;
            listen [::]:80; ## listen for ipv6

            server_name www.$domain;
            return 301 http://$domain\$request_uri;
    }

    server {
        listen   80; ## listen for ipv4
        listen   [::]:80; ## listen for ipv6

        root /home/$username/public_html/;

        index index.php index.html index.htm;

        server_name $domain;

        location / {
                try_files \$uri \$uri/ /index.php?q=\$request_uri;
        }

        location ~ \.php$ {
                    try_files \$uri =404;
                    fastcgi_pass unix:/var/run/php5-fpm.sock;
                    fastcgi_index index.php;
                    fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
                    include fastcgi_params;

            }

        access_log /home/$username/logs/access.log;
        error_log /home/$username/logs/error.log;
    }" > $vhost_filepath

    htaccess_content=""
fi

# download and extract wordpress to user directory under public_html
sudo -H -u $username bash -c "
cd /home/$username/;
mkdir /home/$username/logs;
wget /home/$username/latest.tar.gz https://wordpress.org/latest.tar.gz;
tar xzvf /home/$username/latest.tar.gz -C /home/$username/;
mv /home/$username/wordpress /home/$username/public_html;
rm /home/$username/latest.tar.gz;
cp /home/$username/public_html/wp-config-sample.php /home/$username/public_html/wp-config.php;
sed -i 's/database_name_here/$database/' /home/$username/public_html/wp-config.php;
sed -i 's/username_here/$username/' /home/$username/public_html/wp-config.php;
sed -i 's/password_here/$password/' /home/$username/public_html/wp-config.php;
mkdir /home/$username/public_html/wp-content/uploads;
echo '$htaccess_content'> /home/$username/public_html/.htaccess"


## create the A record
#curl https://www.cloudflare.com/api_json.html \
#  -d "a=rec_new" \
#  -d "tkn=11a0c68fe346f98ee41d46229634b030287c2" \
#  -d "email=reza@vixre.co.uk" \
#  -d "z=vixre.co.uk" \
#  -d "type=A" \
#  -d "name=$domain" \
#  -d "ttl=1" \
#  -d "content=$server_ipv4"
#
## create the AAAA record
#curl https://www.cloudflare.com/api_json.html \
#  -d "a=rec_new" \
#  -d "tkn=11a0c68fe346f98ee41d46229634b030287c2" \
#  -d "email=reza@vixre.co.uk" \
#  -d "z=vixre.co.uk" \
#  -d "type=AAAA" \
#  -d "name=$domain" \
#  -d "ttl=1" \
#  -d "content=$server_ipv6"

# reload web server to take on new vhost
sudo /etc/init.d/$server reload

wp_root=/home/$username/public_html

# wp-cli resources
aw_full_path=$(pwd);
wp_cli=$aw_full_path'/wp-cli.phar';
echo $wp_cli

# Media archive to populate wp installation with some example images
tmp_dir='vixre_tmp';
media_url='http://valuestockphoto.com/freehighresimages/sample_cart.zip';
media_archive='sample_cart.zip';
media_folder='media';

# Command executed as users
sudo su - $username -c "
cd $wp_root;
$wp_cli core install --url='$url'  --title='$url' --admin_user='$username' --admin_password='$password' --admin_email='support@vixre.co.uk'
$wp_cli rewrite structure '/%postname%/';
$wp_cli plugin uninstall hello;
$wp_cli plugin delete akismet;
$wp_cli plugin install wp-spamshield;
$wp_cli plugin activate wp-spamshield;
mkdir $tmp_dir;
cd $tmp_dir;
mkdir $media_folder;
wget $media_url $media_archive;
unzip $media_archive -d $media_folder;
$wp_cli media import $media_folder/*;
cd ..
rm -rf $tmp_dir;";

# set permissions so it's writable by the user and web server
sudo chown -R $user:$webserver_group /home/$username/public_html/
sudo chmod -R 774 /home/$username/public_html/

# make the config readable
sudo -H -u $username bash -c "chmod 660 /home/$username/public_html/wp-config.php;"

base_dir=$(dirname $0)
config_path_json=$base_dir'/configs/'$username'.json'

echo "Writing config to $config_path_json"

echo "{
    \"vhost-path\": \"$vhost_filepath\",
    \"server-type\": \"$server\",
    \"content\": {
        \"database\": \"$database\",
        \"home-dir\": \"/home/$username\"
    },
    \"authentication\": {
        \"username\": \"$username\",
        \"password\": \"$password\"
    }
}" > $config_path_json

echo "
=============================
 Welcome details
=============================
Congratulations, your website has been set up.
You can access your website at: http://$domain

Your site login details:

username: $username
password: $password

Please note that this is only a temporary development URL and once you are happy with the site we can change it to your domain name. Please let us know if you have any questions.

Thanks,
Vixre Team
info@vixre.co.uk"
