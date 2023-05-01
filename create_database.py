#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
from sqlite3 import Error


# ### Hacer conexión a la base de datos

# In[2]:


path = './'
connection = sqlite3.connect(path + 'mi_db.sqlite')


# ### Crear tablas 
# 
# Solo su estructura, por ahora sin valores.

# In[3]:


create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  gender TEXT,
  nationality TEXT
);
"""


# In[4]:


cursor = connection.cursor()
cursor.execute(create_users_table)
connection.commit()


# In[5]:


create_posts_table = """
CREATE TABLE IF NOT EXISTS posts(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  title TEXT NOT NULL, 
  description TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id)
);
"""


# In[6]:


cursor.execute(create_posts_table)
connection.commit()


# In[7]:


create_comments_table = """
CREATE TABLE IF NOT EXISTS comments (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  text TEXT NOT NULL, 
  user_id INTEGER NOT NULL, 
  post_id INTEGER NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
);
"""

create_likes_table = """
CREATE TABLE IF NOT EXISTS likes (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  user_id INTEGER NOT NULL, 
  post_id integer NOT NULL, 
  FOREIGN KEY (user_id) REFERENCES users (id) FOREIGN KEY (post_id) REFERENCES posts (id)
);
"""

cursor.execute(create_comments_table)
cursor.execute(create_likes_table)
connection.commit()


# ## Insertar valores

# In[8]:


create_users = """
INSERT INTO
  users (name, age, gender, nationality)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""

cursor.execute(create_users)   


# In[9]:


create_posts = """
INSERT INTO
  posts (title, description, user_id)
VALUES
  ("Happy", "I am feeling very happy today", 1),
  ("Hot Weather", "The weather is very hot today", 2),
  ("Help", "I need some help with my work", 2),
  ("Great News", "I am getting married", 1),
  ("Interesting Game", "It was a fantastic game of tennis", 5),
  ("Party", "Anyone up for a late-night party today?", 3);
"""

create_comments = """
INSERT INTO
  comments (text, user_id, post_id)
VALUES
  ('Count me in', 1, 6),
  ('What sort of help?', 5, 3),
  ('Congrats buddy', 2, 4),
  ('I was rooting for Nadal though', 4, 5),
  ('Help with your thesis?', 2, 3),
  ('Many congratulations', 5, 4);
"""

create_likes = """
INSERT INTO
  likes (user_id, post_id)
VALUES
  (1, 6),
  (2, 3),
  (1, 5),
  (5, 4),
  (2, 4),
  (4, 2),
  (3, 6);
"""

cursor.execute(create_posts) 
cursor.execute(create_comments) 
cursor.execute(create_likes) 
connection.commit()


# ## Extraer datos

# In[10]:


select_users = "SELECT * from users"
users = cursor.execute(select_users)

for user in users:
    print(user)


# In[11]:


type(users)


# In[12]:


import pandas as pd 

pd.read_sql("""SELECT * FROM users;""", connection)


# In[13]:


pd.read_sql("""SELECT * FROM posts;""", connection)


# In[14]:


pd.read_sql("""SELECT * FROM comments;""", connection)


# In[15]:


pd.read_sql("""SELECT * FROM likes;""", connection)


# ## Eliminar/Modificar registros/campos

# In[16]:


pd.read_sql("""SELECT * FROM posts;""", connection)


# #### Modificar
# 
# > UPDATE tabla \
# > SET col1 = valor, col2 = valor2, col5 = valor5 \
# > WHERE condiciones;

# In[17]:


update_posts = """
UPDATE posts
SET title = "titulo modificado", description = "campo modificado tambien"
WHERE id = 2;
"""


# In[18]:


cursor.execute(update_posts)
connection.commit()


# In[19]:


pd.read_sql("""SELECT * FROM posts;""", connection)


# In[20]:


#update_posts = """
#UPDATE posts
#SET title = "titulo modificado", description = "campo modificado tambien";
#"""
#cursor.execute(update_posts)
#connection.commit()

#pd.read_sql("""SELECT * FROM posts;""", connection)


# In[21]:


update_users = """
UPDATE users
SET age = age*10;
"""
cursor.execute(update_users)
connection.commit()


# In[22]:


pd.read_sql("""SELECT * FROM users;""", connection)


# #### Eliminar
# 
# > ALTER TABLE tabla \
# > DROP COLUMN col4
# 

# In[23]:


drop_users_age = """
ALTER TABLE users
DROP COLUMN gender;
"""

cursor.execute(drop_users_age)
connection.commit()


# In[24]:


pd.read_sql("""SELECT * FROM users;""", connection)


# ### Ejercicio: 
# 
# #### Eliminar los registros donde el nombre termina con la letra 'e'. 

# In[25]:


delete_registros = """
DELETE FROM users
WHERE name LIKE '%e';
"""

cursor.execute(delete_registros)
connection.commit()


# In[26]:


pd.read_sql("""SELECT * FROM users;""", connection)


# ### Ejercicio: 
# 
# #### Investigar como añadir dos columnas nuevas a la tabla **users** 
#  1) con valores 5*cualquier_OtraCol_numerica
#  2) valores de una columna de otra tabla

# In[27]:


# sqlite no permite añadir multiple columnas de manera simultanea
insert_cols = """
ALTER TABLE users
ADD COLUMN nueva_columna_1 INTEGER;
"""
cursor.execute(insert_cols)

insert_cols = """
ALTER TABLE users
ADD COLUMN nueva_columna_2 VARCHAR(50);
"""

cursor.execute(insert_cols)


# In[43]:


update_users = """
UPDATE users
SET nueva_columna_1 = age*5;
"""
cursor.execute(update_users)
connection.commit()

pd.read_sql("""SELECT * FROM users;""", connection)


# In[44]:


update_users = """
UPDATE users
SET nueva_columna_2 = title
FROM posts
WHERE user_id = users.id;
"""
cursor.execute(update_users)
connection.commit()

pd.read_sql("""SELECT * FROM users;""", connection)


# In[ ]:




