#!/usr/bin/python

import fileSearchReplace
from cmd import processCommand, command_line_query


if __name__ == "__main__":
    commands=[]
    
    commands.append("sudo apt-get update")
    commands.append("sudo apt-get dist-upgrade -y")
    commands.append("sudo apt-get autoremove -y")
    commands.append("sudo apt-get install -y build-essential software-properties-common python g++ make fail2ban curl git htop ntp ntpdate zip unzip nano")
    

    # Apache config file
    filename = "/etc/apache2/apache2.conf" 

    ServerName = command_line_query("Enter server_domain_or_IP", default="localhost")

    print "[+] Configuring server name..."

    text = "ServerName %s" % ServerName
    if not fileSearchReplace.SearchReplace(filename, "ServerName", text, True):
        with open(filename, 'a+') as outfile:
            outfile.write("\n" + text)


    # Customizing dir.conf file
    filename = "/etc/apache2/mods-enabled/dir.conf" 

    with open(filename, 'w') as outfile:

        print "[+] Customizing %s" % filename

        text = """\
<IfModule mod_dir.c>
    DirectoryIndex index.php index.html index.cgi index.pl index.xhtml index.htm
</IfModule>
        """

        outfile.write(text) 


    # Customizing Apache default file
    filename = "/etc/apache2/sites-available/default" 

    with open(filename, 'w') as outfile:

        print "[+] Customizing %s" % filename

        text = """\
<Directory /var/www/>
    Options Indexes FollowSymLinks
    AllowOverride All
    Order allow,deny
    allow from all
</Directory>
        """

        outfile.write(text)   
 
    # Start processing commands
    processCommand(commands)

    commands=[]
    commands.append("sudo apt-get install apache2")
    commands.append("sudo ufw app list")
    commands.append("sudo ufw allow in \"Apache Full\"")
    commands.append("sudo ufw allow in \"OpenSSH\"")
    commands.append("sudo ufw enable")
    commands.append("sudo ufw status verbose")

    commands.append("sudo apache2ctl configtest")
    commands.append("sudo systemctl restart apache2")

    commands.append("sudo a2enmod rewrite")
    commands.append("sudo systemctl restart apache2")

    # Start processing commands
    processCommand(commands)
    
    commands=[]
    commands.append("sudo apt-get install mysql-server")

    commands.append("sudo apt-get install php libapache2-mod-php php-mcrypt php-mysql")

    commands.append("sudo systemctl restart apache2")
    commands.append("sudo systemctl status apache2")

    commands.append("sudo apt-get install php-cli")

    commands.append("curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer")

    commands.append("sudo apt-get update")
    commands.append("sudo apt-get install mcrypt php7.0-mcrypt sudo apt-get upgrade sudo apt-get install php-mbstring sudo apt-get install phpunit")

    # Start processing commands
    processCommand(commands)

