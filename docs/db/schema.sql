-- Schema for FastAPI_BG_PM Database

-- Tabla de usuarios con todos los campos
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    image VARCHAR(255),
    role VARCHAR(20) NOT NULL DEFAULT 'user'
);

CREATE TABLE messages_instance (
    id_mi INT PRIMARY KEY AUTO_INCREMENT,
    status VARCHAR(50) NOT NULL,
    content TEXT,
    timestamp DATETIME
);

CREATE TABLE chat (
    id_chat INT PRIMARY KEY AUTO_INCREMENT,
    id_mi INT NOT NULL,
    content TEXT,
    timestamp DATETIME,
    FOREIGN KEY (id_mi) REFERENCES messages_instance(id_mi)
);

CREATE TABLE games (
    id_game INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(50) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    rating DECIMAL(3,2),
    image VARCHAR(255),
    category VARCHAR(50) NOT NULL,
    UNIQUE (name)
);

CREATE TABLE achievement (
    id_achievement INT PRIMARY KEY AUTO_INCREMENT,
    difficulty VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    id_game INT,
    FOREIGN KEY (id_game) REFERENCES games(id_game)
);

CREATE TABLE forums (
    id_forum INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    id_game INT NULL,
    id_user INT NULL,
    FOREIGN KEY (id_game) REFERENCES games(id_game) ON DELETE SET NULL,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE SET NULL
);


CREATE TABLE user_messages_instance (
    id_user INT NOT NULL,
    id_mi INT NOT NULL,
    PRIMARY KEY (id_user, id_mi),
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_mi) REFERENCES messages_instance(id_mi) ON DELETE CASCADE
);


CREATE TABLE user_forum (
    id_user INT NOT NULL,
    id_forum INT NOT NULL,
    PRIMARY KEY (id_user, id_forum),
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE CASCADE
);


CREATE TABLE user_game (
    id_user INT NOT NULL,
    id_game INT NOT NULL,
    PRIMARY KEY (id_user, id_game),
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_game) REFERENCES games(id_game) ON DELETE CASCADE
);


CREATE TABLE user_achievement (
    id_user INT NOT NULL,
    id_achievement INT NOT NULL,
    PRIMARY KEY (id_user, id_achievement),
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_achievement) REFERENCES achievement(id_achievement) ON DELETE CASCADE
);

CREATE TABLE builds (
    id_build INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    planner VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    id_forum INT NULL,
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE SET NULL
);

CREATE TABLE tier_list (
    id_tl INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    id_forum INT NULL,
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE SET NULL,
    UNIQUE (id_forum)   
);

CREATE TABLE guides (
    id_guide INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    id_forum INT NULL,
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE SET NULL
);

CREATE TABLE wiki (
    id_wiki INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    id_forum INT NULL,
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE SET NULL
);


CREATE TABLE discussion (
    id_discussion INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    comments TEXT,
    posts INT,
    rating DECIMAL(3,2),
    id_forum INT NULL,
    id_user INT NULL,
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE SET NULL,
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE SET NULL
);


CREATE TABLE groups_table (
    id_group INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    admin INT NOT NULL,
    description TEXT,
    image VARCHAR(255),
    id_forum INT NULL,
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE SET NULL,
    FOREIGN KEY (admin) REFERENCES users(id) ON DELETE RESTRICT
);


CREATE TABLE user_group (
    id_user INT NOT NULL,
    id_group INT NOT NULL,
    PRIMARY KEY (id_user, id_group),
    FOREIGN KEY (id_user) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_group) REFERENCES groups_table(id_group) ON DELETE CASCADE
);

CREATE TABLE forum_game (
    id_forum INT NOT NULL,
    id_game INT NOT NULL,
    PRIMARY KEY (id_forum, id_game),
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE CASCADE,
    FOREIGN KEY (id_game) REFERENCES games(id_game) ON DELETE CASCADE
);

CREATE TABLE forum_wiki (
    id_forum INT NOT NULL,
    id_wiki INT NOT NULL,
    PRIMARY KEY (id_forum, id_wiki),
    FOREIGN KEY (id_forum) REFERENCES forums(id_forum) ON DELETE CASCADE,
    FOREIGN KEY (id_wiki) REFERENCES wiki(id_wiki) ON DELETE CASCADE
);