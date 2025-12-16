DROP DATABASE IF EXISTS trivia;
CREATE DATABASE IF NOT EXISTS trivia;

USE trivia;

CREATE TABLE Users (
	user_name           VARCHAR(320)  NOT NULL,
	correct_answers INT NOT NULL,
	PRIMARY KEY (user_name)
);

CREATE TABLE Questions (
	id INT NOT NULL auto_increment,
	question           VARCHAR(320)  NOT NULL,
	correct_answer   VARCHAR(320)  NOT NULL,
	wrong_answer1    VARCHAR(320)  NOT NULL,
	wrong_answer2    VARCHAR(320)  NOT NULL,
	PRIMARY KEY (id),
    UNIQUE KEY unique_question (question)
);


CREATE TABLE User_question_answers (
	user_name VARCHAR(320)  NOT NULL,
	id INT NOT NULL,
	PRIMARY KEY (user_name, id)
);

CREATE TABLE Meta (
	key_ VARCHAR(64) PRIMARY KEY,
	value_ VARCHAR(64) NOT NULL
);

INSERT INTO Meta VALUES ("phase", "idle");