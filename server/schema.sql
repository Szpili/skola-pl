-- Skola votes. One anonymous tap = one row. Pool comes from the lesson URL
-- (?p=3a-matematyka-gv2-0827). No student id — that is the K-8 anonymity contract.
-- Import in phpMyAdmin: select the database, Import, this file.

CREATE TABLE IF NOT EXISTS votes (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pool VARCHAR(80) NOT NULL,
  gx TINYINT UNSIGNED NOT NULL,
  gy TINYINT UNSIGNED NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY pool_created (pool, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
