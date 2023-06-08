CREATE TABLE `follows` (
  `following_user_id` integer,
  `followed_user_id` integer,
  `created_at` timestamp
);

CREATE TABLE `users` (
  `id` integer PRIMARY KEY,
  `username` varchar(255),
  `rejected` boolean,
  `created_at` timestamp,
  `folowed_date` timestamp,
  `unfolowed_date` timestamp
);

CREATE TABLE `posts` (
  `id` integer PRIMARY KEY,
  `body` text COMMENT 'Content of the post',
  `user_id` integer,
  `updated_at` timestamp
);

CREATE TABLE `interactions` (
  `liked_user_id` integer,
  `commented_user_id` integer
);

ALTER TABLE `posts` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `follows` ADD FOREIGN KEY (`following_user_id`) REFERENCES `users` (`id`);

ALTER TABLE `follows` ADD FOREIGN KEY (`followed_user_id`) REFERENCES `users` (`id`);

ALTER TABLE `interactions` ADD FOREIGN KEY (`liked_user_id`) REFERENCES `posts` (`id`);

ALTER TABLE `interactions` ADD FOREIGN KEY (`commented_user_id`) REFERENCES `posts` (`id`);
