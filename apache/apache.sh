#!/usr/bin/env sh
#
# Start httpd
# Note:  If certif.pem is present in /opt/certificate, add HTTPS Redirection before starting httpd
#

APP=/usr/sbin/httpd
LOCAL_CERTIFICATE=/opt/certificate
CERTIF=certif.pem
REP_CONF=/home/apps/apache
REP_HTTP=/etc/httpd/conf
REP_SSL=/etc/httpd/conf.d

if test -d ${LOCAL_CERTIFICATE} -a -f ${LOCAL_CERTIFICATE}/$CERTIF; then {
	echo "Certificat present => HTTPS"
	sed "/<\/VirtualHost>/i# HTTPS Redirection\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteCond %{HTTP_HOST} !localhost\nRewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}" $REP_HTTP/httpd.conf > /tmp/httpd.conf
	cp -pf /tmp/httpd.conf $REP_HTTP/httpd.conf
}
else {
	echo "Certificat non present => HTTP"
}
fi

exec $APP
