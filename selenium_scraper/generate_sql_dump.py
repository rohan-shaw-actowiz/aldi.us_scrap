import json
from models import Grocery

# Load the full JSON structure
with open("groceries.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Flatten all items from all categories
all_items = []
for items in raw_data.values():  
    all_items.extend(items)

# Parse and validate with Pydantic model
grocery_items = [Grocery(**item) for item in all_items]

# SQL type mapping
type_map = {
    str: "TEXT",
    int: "INTEGER",
    float: "REAL"
}

# Generate CREATE TABLE statement
def generate_create_table(model, table_name="groceries"):
    columns = []
    for field_name, field_type in model.__annotations__.items():
        base_type = field_type
        if hasattr(base_type, "__origin__"):  # Handle Optional[]
            base_type = base_type.__args__[0]
        sql_type = type_map.get(base_type, "TEXT")
        columns.append(f"{field_name} {sql_type}")
    joined_columns = ",\n  ".join(columns)
    return f"CREATE TABLE {table_name} (\n  {joined_columns}\n);"

# Generate INSERT statements
def generate_insert(table_name: str, item: dict) -> str:
    keys = ', '.join(item.keys())
    values = []
    for v in item.values():
        if v is None:
            values.append("NULL")
        elif isinstance(v, str):
            escaped = v.replace("'", "''")
            values.append(f"'{escaped}'")
        else:
            values.append(str(v))
    values_str = ', '.join(values)
    return f"INSERT INTO {table_name} ({keys}) VALUES ({values_str});"


# Write to file
with open("grocery_dump.sql", "w", encoding="utf-8") as f:
    f.write(generate_create_table(Grocery) + "\n\n")
    for item in grocery_items:
        # Convert Pydantic model to dict
        item_dict = item.dict()
        insert_stmt = generate_insert("groceries", item_dict)
        f.write(insert_stmt + "\n")

print("SQL dump generated successfully.")