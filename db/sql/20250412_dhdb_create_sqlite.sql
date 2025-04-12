-- Table `user`
CREATE TABLE IF NOT EXISTS "user" (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

-- Table `shop`
CREATE TABLE IF NOT EXISTS shop (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  site TEXT
);

-- Table `food_category`
CREATE TABLE IF NOT EXISTS food_category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  name_slo TEXT NOT NULL,
  kcal INTEGER
);

-- Table `discount`
CREATE TABLE IF NOT EXISTS discount (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  "from_date" DATE NOT NULL,
  "to_date" DATE NOT NULL,
  item_id INTEGER NOT NULL,
  value REAL NOT NULL
);

-- Table `item`
CREATE TABLE IF NOT EXISTS item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  price REAL NOT NULL,
  grams INTEGER NOT NULL,
  vendor_id TEXT NOT NULL,
  src TEXT,
  food_category_id INTEGER NOT NULL,
  shop_id INTEGER NOT NULL
);

-- Table `storage`
CREATE TABLE IF NOT EXISTS storage (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grams INTEGER NOT NULL,
  expiry DATE,
  user_id INTEGER NOT NULL,
  food_category_id INTEGER NOT NULL
);

-- Table `recipe`
CREATE TABLE IF NOT EXISTS recipe (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  text TEXT NOT NULL
);

-- Table `menu`
CREATE TABLE IF NOT EXISTS menu (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  year INTEGER NOT NULL,
  week_number INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  mon_id INTEGER NOT NULL,
  tue_id INTEGER NOT NULL,
  wed_id INTEGER NOT NULL,
  thu_id INTEGER NOT NULL,
  fri_id INTEGER NOT NULL,
  sat_id INTEGER NOT NULL,
  sun_id INTEGER NOT NULL
);

-- Table `recipe_item`
CREATE TABLE IF NOT EXISTS recipe_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  food_category_id INTEGER NOT NULL,
  grams INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS shopping_list (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  item_id INTEGER NOT NULL,
  is_active INTEGER NOT NULL DEFAULT 1
  );

CREATE TABLE IF NOT EXISTS scraped (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  shop_id INTEGER NOT NULL,
  store TEXT ,
  category TEXT ,
  mid_category TEXT ,
  product_id TEXT ,
  name TEXT ,
  price TEXT ,
  discount TEXT ,
  url TEXT 
);