#/usr/bin/sh

rm -rf /opt/ICM
mkdir /opt/ICM

#安装文件
cp -rf ./* /opt/ICM/

#安装服务
cp -rf ICM.service /lib/systemd/system/

#配置服务
systemctl disable ICM
systemctl enable ICM
systemctl stop ICM
systemctl start ICM


