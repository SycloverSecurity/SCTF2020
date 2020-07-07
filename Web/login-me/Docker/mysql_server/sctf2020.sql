#创建cas数据库
CREATE DATABASE cas;
USE cas;
CREATE TABLE `sso_t_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_name` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
INSERT INTO `sso_t_user` VALUES (1,'04bbbbcb-39e7-466c-8d3a-4c716e8802fd','55f21708c44caa0574e049521940bdfc');

#添加cas用户
CREATE USER 'cas'@'172.19.0.3' IDENTIFIED BY '8trR3Qxp';
GRANT SELECT ON cas.sso_t_user TO 'cas'@'172.19.0.3';

#刷新权限
FLUSH PRIVILEGES;




