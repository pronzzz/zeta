from faker import Faker
import random
from db import get_connection, init_db

fake = Faker()

def seed_data(num_items=50):
    init_db()
    conn = get_connection()
    c = conn.cursor()
    
    stores = ["Belconnen", "Civic", "Woden", "Tuggeranong"]
    categories = ["Electronics", "Computers", "Gaming", "Appliances"]
    
    # clear existing data
    c.execute('DELETE FROM inventory')
    
    for i in range(num_items):
        sku = f"{random.randint(1000, 9999)}"
        name = fake.company() + " " + fake.word().capitalize()
        store = random.choice(stores)
        on_hand_qty = random.randint(0, 100)
        reorder_point = random.randint(10, 30)
        sell_through_rate = round(random.uniform(0.1, 0.9), 2)
        category = random.choice(categories)
        
        c.execute('''
            INSERT INTO inventory (sku, name, store, on_hand_qty, reorder_point, sell_through_rate, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (sku, name, store, on_hand_qty, reorder_point, sell_through_rate, category))
        
    # Inject a specific SKU for testing (SKU 4471 at Belconnen)
    c.execute("DELETE FROM inventory WHERE sku='4471' AND store='Belconnen'")
    c.execute('''
        INSERT INTO inventory (sku, name, store, on_hand_qty, reorder_point, sell_through_rate, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ('4471', 'Test Monitor', 'Belconnen', 5, 20, 0.15, 'Computers'))
    
    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
