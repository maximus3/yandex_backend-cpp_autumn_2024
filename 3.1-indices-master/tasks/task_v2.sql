-- ### Задание-2: Ускорение поиска

-- ```sql
-- SELECT 
--     "users_user"."id", 
--     "users_user"."first_name", 
--     "users_user"."second_name", 
--     "users_user"."last_name", 
--     "users_user"."email", 
--     "users_user"."address", 
--     "users_user"."phone_number", 
--     "users_user"."company_id", 
--     "users_user"."job_id" 
-- FROM 
--     "users_user" 
-- WHERE 
--     (
--         UPPER("users_user"."id"::text) = UPPER('John') 
--         OR UPPER("users_user"."first_name"::text) LIKE UPPER('%John%') 
--         OR UPPER("users_user"."last_name"::text) LIKE UPPER('%John%') 
--         OR UPPER("users_user"."phone_number"::text) LIKE UPPER('John%') 
--         OR UPPER("users_user"."email"::text) LIKE UPPER('%John%')
--     ) 
-- ORDER BY 
--     "users_user"."last_name" ASC;
-- ```

-- **Подсказки:**

-- - Использование функций, таких как `UPPER()`, в условиях фильтрации может мешать использованию индексов.
-- - Преобразование типов, такое как `::text`, также может негативно сказываться на производительности.
-- - Подумайте о создании функциональных индексов, если использование функций неизбежно.

-- **Дополнительные материалы:**

-- - Документация PostgreSQL по индексам: https://www.postgresql.org/docs/current/indexes.html
