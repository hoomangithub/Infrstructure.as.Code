#!/bin/bash -xe
sudo yum update -y
sudo yum install -y httpd
# sudo yum -y install httpd php mysql
IP=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
echo "<html><head><title>Modern Web App</title><style>body {margin-top: 40px;background-color: #333;}</style></head><body><div style=color:white;text-align:center><h1 style='font-size:7vw;'>Modern Web App</h1><p>Congratulations! Your Web Server is Online.</p><small>Pages served from $IP</small></div></body></html>" >> /var/www/html/index.html
sudo chkconfig httpd on
sudo service httpd start

# To Connect to DB
# mysql -u {User_name} -p -h {RDS_End_Point} {DB_NAME}