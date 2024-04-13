-- ourforum.`data` definition

CREATE TABLE `data`
(
    `id`       int unsigned NOT NULL AUTO_INCREMENT,
    `sender`   varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `content`  longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
    `datetime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci  NOT NULL,
    `ip`       text,
    `address`  text,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=175 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;