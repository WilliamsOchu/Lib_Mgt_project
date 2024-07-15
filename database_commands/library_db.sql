CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(64) NOT NULL,
  `role` enum('admin','librarian','member') DEFAULT 'admin'
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn varchar(30) NOT NULL,
	  genre VARCHAR(255) NOT NULL,
	  publication_date int(11) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    no_of_copy int(5) NOT NULL,
    categoryid int(11) NOT NULL,
    rackid int(11) NOT NULL,
    added_on int(11) NOT NULL,
    updated_on datetime NOT NULL DEFAULT current_timestamp()
  
);

CREATE TABLE borrowed (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    no_of_copy int(5) NOT NULL
);

CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    rating int(2) NOT NULL,
    review VARCHAR(255) NOT NULL
);