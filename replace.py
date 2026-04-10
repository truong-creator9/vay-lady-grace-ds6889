import os
import sqlite3

def replace_in_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Rency variants
    content = content.replace('RENCY', 'LAMAI')
    content = content.replace('Rency', 'LAMAI')
    content = content.replace('rency', 'lamai')
    
    # Replace DVC variants
    content = content.replace('DVC', 'LAMAI')
    content = content.replace('Dvc', 'Lamai')
    content = content.replace('dvc', 'lamai')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

files_to_update = [
    'sales_script.md',
    r'data\faq\common-questions.md',
    r'data\customers\reviews.md',
    r'data\objections\handling.md',
    r'data\products\lady-grace-set.md',
    r'data\products\floral-melodie-dress.md',
    r'data\products\golden-elegance.md',
    'index.html'
]

for file in files_to_update:
    replace_in_file(file)

# Update database
try:
    conn = sqlite3.connect('brain.db')
    cursor = conn.cursor()
    tables = ['knowledge', 'business', 'brand_voice']
    for table in tables:
        try:
            cursor.execute(f"UPDATE {table} SET content = REPLACE(content, 'RENCY', 'LAMAI')")
            cursor.execute(f"UPDATE {table} SET content = REPLACE(content, 'Rency', 'LAMAI')")
            cursor.execute(f"UPDATE {table} SET content = REPLACE(content, 'rency', 'lamai')")
            cursor.execute(f"UPDATE {table} SET content = REPLACE(content, 'DVC', 'LAMAI')")
            
            cursor.execute(f"UPDATE {table} SET title = REPLACE(title, 'RENCY', 'LAMAI')")
            cursor.execute(f"UPDATE {table} SET title = REPLACE(title, 'Rency', 'LAMAI')")
            cursor.execute(f"UPDATE {table} SET title = REPLACE(title, 'DVC', 'LAMAI')")
        except sqlite3.OperationalError:
            pass  # table might not exist
    conn.commit()
    conn.close()
    print("Database updated!")
except Exception as e:
    print(f"Error updating DB: {e}")

print("All replacements done successfully!")
