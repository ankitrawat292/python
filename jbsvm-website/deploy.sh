#!/usr/bin/env bash
# Run this ON THE VPS (as root) from inside the jbsvm-website folder:
#   bash deploy.sh
set -e
mkdir -p /var/www/jbsvm
cp index.html /var/www/jbsvm/index.html
cp nginx-jbsvm.conf /etc/nginx/sites-available/jbsvm
ln -sf /etc/nginx/sites-available/jbsvm /etc/nginx/sites-enabled/jbsvm
nginx -t
systemctl reload nginx
echo "Live at: http://jbsvm.187-127-155-250.sslip.io"
# Optional HTTPS:
#   apt install -y certbot python3-certbot-nginx
#   certbot --nginx -d jbsvm.187-127-155-250.sslip.io
