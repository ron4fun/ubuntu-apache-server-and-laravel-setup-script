#!/usr/bin/python

import shutil, os, sys, getopt, subprocess, shlex, re
from cmd import processCommand, command_line_query
   
# Validator
def validate_dir(answer):
    if os.path.isdir(answer):
    	return answer
    else:
    	raise ValueError("Please enter a correct directory.")

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def validate_url(answer):
    if regex.match(answer):
    	return answer
    else:
    	raise ValueError("Please enter a valid url.")
    

if __name__ == "__main__":
	# Get general path
	path_to_save_repo = command_line_query("Enter path location", validate=validate_dir, default="/var/www/")


	# Get git repo url
	url_git_repo = command_line_query("Enter url for the repo", validate=validate_url)
	repo_name = url_git_repo.rstrip('/').split('/')[-1].split('.')[0]
	app_path = os.path.join(path_to_save_repo, repo_name)
	

	# Change path to path_to_save_repo
	command = "cd %s" % path_to_save_repo
	processCommand(command)
	

	# Run git clone command
	command = "git clone " + url_git_repo
	print "[+] Cloning repo at %s to %s" % (url_git_repo, app_path)
	processCommand(command)
	

	# Update packages via composer
	command = "composer --working-dir=" + app_path + " update"
	print "[+] Updating repo package manager"
	processCommand(command)


	# Set Privilages to folders
	commands=[]
	
	commands.append("sudo chgrp -R www-data " + app_path)
	commands.append("sudo chmod -R 777 " + os.path.join(app_path, "storage"))
	commands.append("sudo chmod -R 777 " + os.path.join(app_path, "bootstrap/cache"))
	
	print "[+] Setting required privilages"
	processCommand(commands)


	# Set app config
	filename = "/etc/apache2/sites-available/%s.conf" % repo_name 

	with open(filename, 'w') as outfile:
		ServerName = command_line_query("Enter ServerName", default="localhost")
		ServerAdmin = command_line_query("Enter ServerAdmin", default="webmaster@localhost")
		ServerAlias = command_line_query("Enter ServerAlias", default="localhost")

		print "[+] Creating %s" % filename

		text = """\
		<VirtualHost *:80>
			ServerAlias %s
		    ServerName %s

		    ServerAdmin %s
		    DocumentRoot %s

		    <Directory %s>
		        Options Indexes FollowSymLinks MultiViews
		        AllowOverride all
		        Order allow,deny
		        allow from all
		        Require all granted
		    </Directory>

		    ErrorLog ${APACHE_LOG_DIR}/error.log
		    CustomLog ${APACHE_LOG_DIR}/access.log combined
		</VirtualHost>
		""" % (ServerAlias, ServerName, ServerAdmin, os.path.join(app_path, "public"), app_path)

		outfile.write(text)    

	

	# Finalize
	commands=[]
	apache2_path = "/etc/apache2/sites-available/"
	commands.append("cd %s" % apache2_path)
	commands.append("sudo a2dissite 000-default.conf")
	commands.append("sudo a2ensite %s.conf" % repo_name)
	commands.append("sudo a2enmod rewrite")
	commands.append("sudo service apache2 restart")

	print "[+] Finalizing..."
	processCommand(commands)
   
	# Finishing checks
	if not os.path.exists(os.path.join(app_path, ".env")):
		if os.path.exists(os.path.join(app_path, ".env.example")) :
			original_file = os.path.join(app_path, ".env.example")
			new_file_name = os.path.join(app_path, ".env")
			command = "mv %s %s" % (original_file, new_file_name)
			print "[+] Renaming repo '.env.example' to '.env'"
			processCommand(command)








