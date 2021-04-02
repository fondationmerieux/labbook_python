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
HTTPD_CONF=$REP_HTTP/httpd.conf
SSL_CONF=/etc/httpd/conf.d/ssl.conf

if test -d ${LOCAL_CERTIFICATE} -a -f ${LOCAL_CERTIFICATE}/$CERTIF; then {
	echo "Certificat present => HTTPS"
	sed "/<\/VirtualHost>/i# HTTPS Redirection\nRewriteEngine On\nRewriteCond %{HTTPS} off\nRewriteCond %{HTTP_HOST} !localhost\nRewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}" $HTTPD_CONF > /tmp/httpd.conf
	cp -pf /tmp/httpd.conf $HTTPD_CONF
}
else {
	echo "Certificat non present => HTTP"
	# Remove ssl.conf or httpd doesn't start
	rm -f $SSL_CONF
}
fi

exec $APP
