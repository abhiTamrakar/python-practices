#!/bin/bash

# script to configure apache

# defaults
header='\n%s\t%s'
success_code=0
failed_code=1
WORK_DIR=/tmp

# run as root
# functions


info()
{
printf $header "info:" "$@" 
}

error()
{
printf $header "error:" "$@"
exit $failed_code
}

# checks
## check to see if root
[ $(whoami) = "root" ] || error "Non root user!!!"

# check files in work dir
for file in localhost.crt localhost.key index.html app.py app.wsgi
	do
	if [[ -f ${WORK_DIR}/$file ]]; then
	info "File ${WORK_DIR}/$file FOUND"
		case ${file##*.} in
		crt ) cp -p ${WORK_DIR}/$file /etc/ssl/certs/$file
		;;
		key ) cp -p ${WORK_DIR}/$file /etc/ssl/private/$file
		;;
		html ) [[ -d /var/www/app ]] || mkdir -p /var/www/app
		       cp -p ${WORK_DIR}/$file /var/www/app/$file
		;;
		py ) [[ -d /var/www/app/templates ]] || mkdir -p /var/www/app/templates
			cp -p ${WORK_DIR}/$file /var/www/app/$file
			cp -p ${WORK_DIR}/*.html /var/www/app/templates/
		;;
		wsgi ) cp -p ${WORK_DIR}/$file /var/www/app/$file
		;;
		esac
	else
	error "${WORK_DIR}/$file not found!!"
	fi
done
#main
if [[ -f /etc/os-release ]]
	then
	. /etc/os-release \
		&& info "Finished reading version information" \
		|| error "Cannor read version inforamtion"
fi

case ${ID,,} in
ubuntu ) 
# enable modules
a2enmod wsgi && info "Enabled wsgi module" ||  error "enabling module wsgi failed"
a2enmod proxy && info "Enabled proxy module" ||  error "enabling module proxy failed"
a2enmod rewrite && info "Enabled r/w module" || error "enabling module rw failed"
a2enmod ssl && info "Enabled ssl module" || error "enabling module ssl failed"

# enable website
a2ensite app && info "Enabled site"
;;
* )
ln -s /etc/httpd/sites-available/app.conf  /etc/httpd/sites-enabled/app.conf
;;
esac

service apache2 restart \
	&& info "Service running" \
	|| error "Cant start service"

if [[ "$(curl -sI http://localhost| awk '/HTTP\/1.1/ {print $2}')" -eq 200 ]]; then 
	info "Success"
else
	error "Failed Deployment"
fi
