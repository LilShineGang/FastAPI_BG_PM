-- Aqui va a estar el contenido del schema.sql

CREATE TABLE USERS(
  id_user INT PRIMARY KEY AUTO_INCREMENT,
  nickname VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  image VARCHAR(255),
  UNIQUE()

)
