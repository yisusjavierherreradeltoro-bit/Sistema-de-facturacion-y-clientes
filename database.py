import sqlite3

class Database:
    def __init__(self, db_name="billing_system.db"):
        self.db_name = db_name
        self.init_database()

    def connect(self):
        """Retorna una conexión activa a la base de datos SQLite."""
        return sqlite3.connect(self.db_name)

    def init_database(self):
        """Crea las tablas relacionales y asegura la compatibilidad de esquemas."""
        conn = self.connect()
        cursor = conn.cursor()
        
        # 1. Tabla de Clientes (CRM)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT
            )
        """)
        
        # 2. Tabla de Empleados / Vendedores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        
        # 3. Tabla de Productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                company TEXT,
                category TEXT,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)
        
        # Migraciones automáticas seguras
        try:
            cursor.execute("ALTER TABLE products ADD COLUMN company TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE products ADD COLUMN category TEXT")
        except sqlite3.OperationalError:
            pass

        # 4. Tabla de Facturas (Cabecera)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                worker_id INTEGER,
                total_amount REAL NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE SET NULL,
                FOREIGN KEY (worker_id) REFERENCES workers (id) ON DELETE SET NULL
            )
        """)
        
        try:
            cursor.execute("ALTER TABLE invoices ADD COLUMN worker_id INTEGER")
        except sqlite3.OperationalError:
            pass

        # 5. Tabla de Detalle de Factura
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (invoice_id) REFERENCES invoices (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE SET NULL
            )
        """)
        
        conn.commit()
        conn.close()