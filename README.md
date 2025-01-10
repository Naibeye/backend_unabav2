# service_provider
pip install git+https://github.com/idoshr/flask-mongoengine.git@1.0.1



#
sudo mkdir /var/www/service.netkrypto
sudo chown -R $USER:$USER /var/www/service.netkrypto
sudo chmod -R 755 /var/www/registration.netkrypto

sudo nano /etc/apache2/sites-available/service.netkrypto.conf
```
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName service.netkrypto.net
    ServerAlias www.service.netkrypto.net
    DocumentRoot /var/www/service.netkrypto
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

</VirtualHost>
```
sudo a2ensite service.netkrypto.conf
sudo systemctl restart apache2

sudo certbot --apache
sudo certbot renew --dry-run