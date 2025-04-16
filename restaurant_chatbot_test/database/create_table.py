from supabase import create_client, Client
from config import url, key


supabase: Client = create_client(url, key)

# replace table name from 'menu' other to create new table
create_table_query = """
CREATE TABLE IF NOT EXISTS menu (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_code INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
);
ALTER TABLE menu ENABLE ROW LEVEL SECURITY;  
"""
# change ENABLE to DISABLE for row level security



try:
    
    response = supabase.rpc('sql', {'query': create_table_query}).execute() 

    if response.data:
        print("Table created successfully.")
    else:
        print("Failed to create table:", response)

except Exception as e:
    print("Error:", e)
