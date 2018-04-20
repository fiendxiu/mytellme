#!/bin/bash
set -e

# 初始化环境目录
main_dir="/var/www/"
tellme_dir="$main_dir/django"
logs_dir="$main_dir/logs"
cd "$( dirname "$0"  )"
cd .. && cd ..
cur_dir=$(pwd)
mkdir -p $tellme_dir
mkdir -p $logs_dir
mkdir -p $main_dir/pid

# 关闭selinux
se_status=$(getenforce)
if [ $se_status != Enforcing ]
then
    echo "selinux is diabled, install progress is running"
    sleep 1
else
    echo "Please attention, Your system selinux is enforcing"
    read -p "Do you want to disabled selinux?[yes/no]": shut
    case $shut in
        yes|y|Y|YES)
            setenforce 0
            sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/sysconfig/selinux
            ;;
        no|n|N|NO)
            echo "please manual enable nginx access localhost 8000 port"
            echo "if not, when you open Tellme web you will receive a 502 error!"
            sleep 3
            ;;
        *)
            exit 1
            ;;
    esac
fi


# 安装依赖并升级到python3.6.3
echo "####install depandencies and update to python3####"
yum -y groupinstall 'Development Tools'
yum -y install zlib-devel bzip2-devel openssl-devel ncurese-devel wget deltarpm
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
tar xf Python-3.6.3.tar.xz && cd Python-3.6.3
./configure --prefix=/usr/local/python3
make && make install
rm -f /usr/bin/python
sed -i "s/\/usr\/bin\/python/\/usr\/bin\/python2.7/" /usr/bin/yum
sed -i "s/\/usr\/bin\/python/\/usr\/bin\/python2.7/" /usr/libexec/urlgrabber-ext-down
pip install gnureadline
ln -s /usr/local/python3/bin/python3.6 /usr/bin/python
ln -s /usr/local/python3/bin/pip3.6 /usr/bin/pip


# 安装Django2.0
echo "####install django2.0####"
pip install django==2.0
sed -i 's/export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE HISTCONTROL/export PATH="$PATH:\/usr\/local\/python3\/bin" USER LOGNAME MAIL HOSTNAME HISTSIZE HISTCONTROL/' /etc/profile


# 分发代码
if [ ! $cur_dir ] || [ ! $tellme_dir ]
then
    echo "install directory info error, please check your system environment program exit"
    exit 1
else
    rsync --delete --progress -ra --exclude '.git' $cur_dir/ $tellme_dir
fi


#安装数据库
echo "####install database####"
read -p "do you want to create a new mysql database?[yes/no]:" db1
if [ ! $db1 ]
then
db1=yes
fi
case $db1 in
        yes|y|Y|YES)  
                echo "installing a new mariadb...."
                yum install -y mariadb-server mariadb-devel
                service mariadb start
                chkconfig mariadb on
                mysql -e "CREATE DATABASE if not exists tellme DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
                ;;
        no|n|N|NO)
                read -p "your database ip address:" db_ip
                read -p "your database port:" db_port
                read -p "your database user:" db_user
                read -p "your database password:" db_password
                [ ! $db_password ] && echo "your db_password is empty confirm please press Enter key"
                [ -f /usr/bin/mysql ]
                sleep 3
                if [ $? -eq 0 ]
                then
                        mysql -h$db_ip -P$db_port -u$db_user -p$db_password -e "CREATE DATABASE if not exists tellme DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
                else
                        yum install -y mysql
                        mysql -h$db_ip -P$db_port -u$db_user -p$db_password -e "CREATE DATABASE if not exists tellme DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
                fi
                ;;
        *) 
                exit 1                    
                ;;
esac
pip install PyMySQL
sed -i "s/raise ImproperlyConfigured(\"mysqlclient 1.3.3/\#raise ImproperlyConfigured(\"mysqlclient 1.3.3/" /usr/local/python3/lib/python3.6/site-packages/django/db/backends/mysql/base.py
sed -i "s/if version/\#if version/" /usr/local/python3/lib/python3.6/site-packages/django/db/backends/mysql/base.py


# 安装主程序
echo "####install tellme####"
cd $tellme_dir
pip install Pillow
python manage.py makemigrations
python manage.py migrate
echo "please create your tellme' super admin:"
python manage.py createsuperuser
scp $tellme_dir/install/server/tellme.service /usr/lib/systemd/system
systemctl daemon-reload
chkconfig tellme on
service tellme start
pip install gunicorn
ln -s /usr/local/python3/bin/gunicoren /usr/bin/gunicore


# 安装nginx
echo "####install nginx####"
yum -y install epel-release
yum install nginx -y
chkconfig nginx on
scp $tellme_dir/install/server/nginx/tellme.conf /etc/nginx/conf.d
scp $tellme_dir/install/server/nginx/nginx.conf /etc/nginx
service nginx start
nginx -s reload


# 完成安装
echo "##############install finished###################"
systemctl daemon-reload
service mariadb restart
service tellme restart
service sshd restart
echo "please access website http://server_ip"
echo "you have installed tellme successfully!!!"
echo "################################################"
