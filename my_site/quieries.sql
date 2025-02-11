-- 3 request all products
SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2025-01-17 19:35:20.772072'
    AND "django_session"."session_key" = 'f6xgmw8llmad798rjs7j32f5q7ftk6z9'
  )
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
WHERE
  NOT "shop_app_product"."archived"
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


-- 4 request product by id
SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
WHERE
  "shop_app_product"."id" = 5
LIMIT
  21;


SELECT
  "shop_app_productimage"."id",
  "shop_app_productimage"."product_id",
  "shop_app_productimage"."image",
  "shop_app_productimage"."description"
FROM
  "shop_app_productimage"
WHERE
  "shop_app_productimage"."product_id" IN (5);


SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2025-01-17 20:30:49.263041'
    AND "django_session"."session_key" = 'f6xgmw8llmad798rjs7j32f5q7ftk6z9'
  )
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


-- 4 request all orders
SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2025-01-17 20:48:34.323161'
    AND "django_session"."session_key" = 'f6xgmw8llmad798rjs7j32f5q7ftk6z9'
  )
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt",
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "shop_app_order"
  INNER JOIN "auth_user" ON ("shop_app_order"."user_id" = "auth_user"."id");


SELECT
  ("shop_app_order_products"."order_id") AS "_prefetch_related_val_order_id",
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" IN (1, 2, 4, 5)
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


-- 8 sql-request all orders, in queryset delete .select_related("user")
SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2025-01-17 21:06:06.167570'
    AND "django_session"."session_key" = 'f6xgmw8llmad798rjs7j32f5q7ftk6z9'
  )
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt"
FROM
  "shop_app_order";


SELECT
  ("shop_app_order_products"."order_id") AS "_prefetch_related_val_order_id",
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" IN (1, 2, 4, 5)
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 6
LIMIT
  21;


-- 11 sql-request all orders, in queryset delete .select_related("user").prefetch_related("products")
SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2025-01-17 21:18:00.447787'
    AND "django_session"."session_key" = 'f6xgmw8llmad798rjs7j32f5q7ftk6z9'
  )
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt"
FROM
  "shop_app_order";


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 1
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 2
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 4
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 6
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 5
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


-- 13 sql-request all orders, in queryset delete .select_related("user").prefetch_related("products") and create new product
SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2025-01-17 22:51:57.066493'
    AND "django_session"."session_key" = 'f6xgmw8llmad798rjs7j32f5q7ftk6z9'
  )
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt"
FROM
  "shop_app_order";


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 1
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 2
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 4
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 6
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 5
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" = 6
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


-- 4 sql-request all orders, queryset with .select_related("user").prefetch_related("products")
SELECT
  "django_session"."session_key",
  "django_session"."session_data",
  "django_session"."expire_date"
FROM
  "django_session"
WHERE
  (
    "django_session"."expire_date" > '2025-01-17 22:56:44.431228'
    AND "django_session"."session_key" = 'f6xgmw8llmad798rjs7j32f5q7ftk6z9'
  )
LIMIT
  21;


SELECT
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "auth_user"
WHERE
  "auth_user"."id" = 1
LIMIT
  21;


SELECT
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt",
  "auth_user"."id",
  "auth_user"."password",
  "auth_user"."last_login",
  "auth_user"."is_superuser",
  "auth_user"."username",
  "auth_user"."first_name",
  "auth_user"."last_name",
  "auth_user"."email",
  "auth_user"."is_staff",
  "auth_user"."is_active",
  "auth_user"."date_joined"
FROM
  "shop_app_order"
  INNER JOIN "auth_user" ON ("shop_app_order"."user_id" = "auth_user"."id");


SELECT
  ("shop_app_order_products"."order_id") AS "_prefetch_related_val_order_id",
  "shop_app_product"."id",
  "shop_app_product"."name",
  "shop_app_product"."description",
  "shop_app_product"."price",
  "shop_app_product"."discount",
  "shop_app_product"."created_at",
  "shop_app_product"."archived",
  "shop_app_product"."created_by_id",
  "shop_app_product"."preview"
FROM
  "shop_app_product"
  INNER JOIN "shop_app_order_products" ON (
    "shop_app_product"."id" = "shop_app_order_products"."product_id"
  )
WHERE
  "shop_app_order_products"."order_id" IN (1, 2, 4, 5, 6)
ORDER BY
  "shop_app_product"."name" ASC,
  "shop_app_product"."price" ASC;


-- sql-request command agg
SELECT
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt",
  (CAST(SUM("shop_app_product"."price") AS NUMERIC)) AS "total",
  COUNT("shop_app_order_products"."product_id") AS "products_count"
FROM
  "shop_app_order"
  LEFT OUTER JOIN "shop_app_order_products" ON (
    "shop_app_order"."id" = "shop_app_order_products"."order_id"
  )
  LEFT OUTER JOIN "shop_app_product" ON (
    "shop_app_order_products"."product_id" = "shop_app_product"."id"
  )
GROUP BY
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt";


-- sql-request command agg using default=0
SELECT
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt",
  (
    CAST(
      COALESCE(
        (CAST(SUM("shop_app_product"."price") AS NUMERIC)),
        (CAST('0' AS NUMERIC))
      ) AS NUMERIC
    )
  ) AS "total",
  COUNT("shop_app_order_products"."product_id") AS "products_count"
FROM
  "shop_app_order"
  LEFT OUTER JOIN "shop_app_order_products" ON (
    "shop_app_order"."id" = "shop_app_order_products"."order_id"
  )
  LEFT OUTER JOIN "shop_app_product" ON (
    "shop_app_order_products"."product_id" = "shop_app_product"."id"
  )
GROUP BY
  "shop_app_order"."id",
  "shop_app_order"."user_id",
  "shop_app_order"."promocode",
  "shop_app_order"."delivery_address",
  "shop_app_order"."created_at",
  "shop_app_order"."receipt";
