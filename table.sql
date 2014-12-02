CREATE TABLE sensors (
  value int,
  created timestamp default now(),
  sensor tinyint
);
create index created_index on sensors(created);
