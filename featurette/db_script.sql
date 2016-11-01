USE featurette;

DROP TABLE IF EXISTS `feature_requests`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `clients`;
DROP TABLE IF EXISTS `product_areas`;

CREATE TABLE `users`(id int auto_increment primary key, username
    varchar(64),email varchar(100), password varchar(255), authenticated boolean,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP, updated_at timestamp DEFAULT
    CURRENT_TIMESTAMP);

CREATE TABLE `clients`(id int auto_increment primary key, name
    varchar(100),created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE `product_areas`(id int auto_increment primary key, name
    varchar(100),created_at timestamp  DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE `feature_requests`(id int auto_increment primary key,
    title varchar(100), description varchar(200), client_id int,
    client_priority int, product_area_id int, target_date timestamp DEFAULT
    CURRENT_TIMESTAMP, user_id int, ticket_url varchar(100),date_finished
    timestamp null, created_at timestamp DEFAULT CURRENT_TIMESTAMP, updated_at
    timestamp DEFAULT CURRENT_TIMESTAMP, foreign key(client_id) references
    clients(id), foreign key(product_area_id) references product_areas(id),
    foreign key(user_id) references users(id));

INSERT INTO `users`(username, email, password, authenticated, created_at, updated_at)
    VALUES('user1', 'user1@foo.com', PASSWORD('123456'), false, NOW(), NOW()),
    ('user2', 'user2@foo.com', PASSWORD('123456'), false, NOW(), NOW()),
    ('user3', 'user3@foo.com', PASSWORD('123456'), false, NOW(), NOW()),
    ('user4', 'user4@foo.com', PASSWORD('123456'), false, NOW(), NOW());

INSERT INTO `clients`(name, created_at, updated_at) VALUES ('Client A',
    NOW(), NOW()), ('Client B', NOW(), NOW()), ('Client C', NOW(),
    NOW()), ('Client D', NOW(), NOW()), ('Client E', NOW(), NOW()),
    ('Client F', NOW(), NOW());

INSERT INTO `product_areas`(name, created_at, updated_at) VALUES
    ('Claims', NOW(), NOW()), ('Policies', NOW(), NOW()), ('Accounting',
    NOW(), NOW()), ('Billing', NOW(), NOW()), ('IT', NOW(), NOW()),
    ('Buisness Intelligence', NOW(), NOW());

INSERT INTO `feature_requests`(title, description, client_id,
    client_priority, product_area_id, target_date, user_id, ticket_url, date_finished,
    created_at, updated_at) VALUES ('Request 1', 'Change document templates',
    1, 1, 2, '2016-12-12', 1, 'www.google.com', null, NOW(), NOW()), ('Request 2',
    'Change chart library to modernize app look', 2, 1, 3, '2016-11-08', 4,
    'www.twitter.com', null, NOW(), NOW()), ('Request 3',
    'Use new datepicker in billing document', 3, 1, 1, '2017-03-02', 3,
    'www.nytimes.com', null, NOW(), NOW()), ('Request 4', 'Update claims form',
    4, 1, 4, '2017-01-09', 1, 'www.wired.com', null, NOW(), NOW()),('Request 5',
    'Change landing page to infinite scroll', 4, 1, 2, '2017-06-08', 2,
    'www.thenextweb.com',null, NOW(), NOW());
