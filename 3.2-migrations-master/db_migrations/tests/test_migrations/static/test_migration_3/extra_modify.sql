UPDATE driver
SET last_name = NULL
WHERE id IN (1, 3);

UPDATE spaceship_manufacturer
SET nasdaq_code = NULL
WHERE id IN (2, 4);
