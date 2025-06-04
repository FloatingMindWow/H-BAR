import sqlite3
import os
from datetime import datetime

DB_NAME = 'hbar.db'

class HBar:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        photo TEXT,
                        in_test INTEGER DEFAULT 0,
                        avg_rating REAL DEFAULT 0,
                        ratings_count INTEGER DEFAULT 0
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ratings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INTEGER NOT NULL,
                        score INTEGER NOT NULL,
                        timestamp TEXT NOT NULL,
                        FOREIGN KEY(product_id) REFERENCES products(id)
                    )''')
        self.conn.commit()

    def add_product(self, name, photo=None, in_test=False):
        c = self.conn.cursor()
        c.execute('INSERT INTO products (name, photo, in_test) VALUES (?,?,?)',
                  (name, photo, int(in_test)))
        self.conn.commit()
        print(f"Added product '{name}'")

    def list_products(self):
        c = self.conn.cursor()
        c.execute('SELECT id, name, in_test, avg_rating, ratings_count FROM products ORDER BY in_test DESC, name')
        rows = c.fetchall()
        for row in rows:
            print(f"[{row[0]}] {row[1]} - In test: {'yes' if row[2] else 'no'} - Rating: {row[3]:.2f} ({row[4]} votes)")

    def search_products(self, term):
        c = self.conn.cursor()
        c.execute("SELECT id, name FROM products WHERE name LIKE ? ORDER BY in_test DESC, name", (f"%{term}%",))
        rows = c.fetchall()
        for row in rows:
            print(f"[{row[0]}] {row[1]}")

    def mark_in_test(self, product_id, in_test=True):
        c = self.conn.cursor()
        c.execute('UPDATE products SET in_test=? WHERE id=?', (int(in_test), product_id))
        self.conn.commit()
        print(f"Product {product_id} marked as {'in test' if in_test else 'regular'}")

    def add_rating(self, product_id, score):
        if score < 0 or score > 10:
            print('Score must be between 0 and 10')
            return
        c = self.conn.cursor()
        c.execute('INSERT INTO ratings (product_id, score, timestamp) VALUES (?,?,?)',
                  (product_id, score, datetime.utcnow().isoformat()))
        # Update average and count
        c.execute('SELECT avg_rating, ratings_count FROM products WHERE id=?', (product_id,))
        row = c.fetchone()
        if row:
            avg, count = row
            new_count = count + 1
            new_avg = (avg * count + score) / new_count
            c.execute('UPDATE products SET avg_rating=?, ratings_count=? WHERE id=?',
                      (new_avg, new_count, product_id))
            self.conn.commit()
            print(f"Saved rating {score} for product {product_id}")
        else:
            print('Product not found')

    def get_products(self, term=None):
        c = self.conn.cursor()
        query = 'SELECT id, name, photo, in_test, avg_rating, ratings_count FROM products'
        params = ()
        if term:
            query += ' WHERE name LIKE ?'
            params = (f'%{term}%',)
        query += ' ORDER BY in_test DESC, name'
        c.execute(query, params)
        rows = c.fetchall()
        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'name': row[1],
                'photo': row[2],
                'in_test': bool(row[3]),
                'avg_rating': row[4],
                'ratings_count': row[5]
            })
        return result

    def get_product(self, product_id):
        c = self.conn.cursor()
        c.execute('SELECT id, name, photo, in_test, avg_rating, ratings_count FROM products WHERE id=?', (product_id,))
        row = c.fetchone()
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'photo': row[2],
                'in_test': bool(row[3]),
                'avg_rating': row[4],
                'ratings_count': row[5]
            }
        return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description='H-BAR management tool')
    subparsers = parser.add_subparsers(dest='command')

    add_p = subparsers.add_parser('add', help='Add a new product')
    add_p.add_argument('name', help='Product name')
    add_p.add_argument('--photo', help='Path to product photo')
    add_p.add_argument('--in-test', action='store_true', help='Mark product as in testing')

    list_p = subparsers.add_parser('list', help='List products')

    search_p = subparsers.add_parser('search', help='Search product by name')
    search_p.add_argument('term')

    mark_p = subparsers.add_parser('mark', help='Mark/unmark product as in test')
    mark_p.add_argument('product_id', type=int)
    mark_p.add_argument('--off', action='store_true', help='Unmark as in test')

    rate_p = subparsers.add_parser('rate', help='Rate a product')
    rate_p.add_argument('product_id', type=int)
    rate_p.add_argument('score', type=int, help='Score from 0 to 10')

    args = parser.parse_args()
    hb = HBar()

    if args.command == 'add':
        hb.add_product(args.name, args.photo, args.in_test)
    elif args.command == 'list':
        hb.list_products()
    elif args.command == 'search':
        hb.search_products(args.term)
    elif args.command == 'mark':
        hb.mark_in_test(args.product_id, not args.off)
    elif args.command == 'rate':
        hb.add_rating(args.product_id, args.score)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
