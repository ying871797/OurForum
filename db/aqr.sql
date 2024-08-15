CREATE TABLE ourforum.aqr (
                              id INTEGER UNSIGNED auto_increment NOT NULL,
                              `date` DATETIME NOT NULL,
                              count INTEGER UNSIGNED NOT NULL,
                              CONSTRAINT aqr_pk PRIMARY KEY (id)
)
    ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;