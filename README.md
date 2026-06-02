ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root1024';
FLUSH PRIVILEGES;
SELECT user, host, plugin FROM mysql.user WHERE user='root';
