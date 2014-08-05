# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  
  config.vm.box = "chef/ubuntu-14.04"

  config.vm.provision "shell" do |shell|
    shell.inline = "

      # ~84mb (including dependencies)
      apt-get install postgis tomcat7 unzip apache2 python-django libapache2-mod-wsgi python-psycopg2

      a2enmod headers proxy_http
      
      ln -s /vagrant /opt/herri
      ln -s /opt/herri/server/setup/conf/apache2-herri.conf /etc/apache2/sites-available/herri.conf

      mkdir /opt/herri-static
      chown www-data:www-data /opt/herri-static

      python /opt/herri/server/herri/manage.py collectstatic

      a2dissite 000-default
      a2ensite herri

      # ~52mb
      wget -O /tmp/geoserver-2.5.2.war.zip http://sourceforge.net/projects/geoserver/files/GeoServer/2.5.2/geoserver-2.5.2-war.zip
      
      unzip /tmp/geoserver-2.5.2.war.zip -d /tmp/geoserver/
      mv /tmp/geoserver/geoserver.war /var/lib/tomcat7/webapps/
      rm -r /tmp/geoserver

      service apache2 reload

    "
  end
  
  config.vm.network "forwarded_port", guest: 80, host: 10080
  config.vm.network "forwarded_port", guest: 8080, host: 18080

end
