from database import Database
import sqlite3
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class BillingManager:
    """Gestiona la lógica de negocio, transacciones, base de datos y generación de reportes PDF."""
    def __init__(self):
        self.db = Database()

    # --- CLIENTES ---
    def add_client(self, name, email, phone, address):
        clean_name = name.strip().title()
        if not clean_name:
            return False, "⚠️ El nombre del cliente no puede estar vacío."
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clients (name, email, phone, address) VALUES (?, ?, ?, ?)",
                (clean_name, email.strip(), phone.strip(), address.strip())
            )
            conn.commit()
            conn.close()
            return True, f"✅ Cliente '{clean_name}' registrado con éxito."
        except Exception as e:
            return False, f"❌ Error al registrar cliente: {e}"

    def get_clients(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone, address FROM clients")
        data = cursor.fetchall()
        conn.close()
        return data

    # --- EMPLEADOS ---
    def add_worker(self, name):
        clean_name = name.strip().title()
        if not clean_name:
            return False, "⚠️ El nombre del empleado no puede estar vacío."
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO workers (name) VALUES (?)", (clean_name,))
            conn.commit()
            conn.close()
            return True, f"✅ Empleado '{clean_name}' registrado con éxito."
        except sqlite3.IntegrityError:
            return False, "⚠️ Este empleado ya está registrado."

    def get_workers(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM workers")
        data = cursor.fetchall()
        conn.close()
        return data

    def update_worker(self, worker_id, new_name):
        clean_name = new_name.strip().title()
        if not clean_name:
            return False, "⚠️ El nombre no puede estar vacío."
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE workers SET name = ? WHERE id = ?", (clean_name, worker_id))
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            if affected > 0:
                return True, "✅ Empleado actualizado con éxito."
            return False, "❌ Empleado no encontrado con ese ID."
        except Exception as e:
            return False, f"❌ Error al actualizar: {e}"

    # --- PRODUCTOS Y CATEGORÍAS ---
    def add_product(self, name, company, category, price, stock):
        clean_name = name.strip()
        clean_comp = company.strip().title()
        clean_cat = category.strip().title()
        if not clean_name:
            return False, "⚠️ El nombre del producto es obligatorio."
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, company, category, price, stock) VALUES (?, ?, ?, ?, ?)",
                (clean_name, clean_comp, clean_cat, float(price), int(stock))
            )
            conn.commit()
            conn.close()
            return True, "✅ Producto agregado correctamente."
        except Exception as e:
            return False, f"❌ Error: {e}"

    def get_products(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, company, category, price, stock FROM products")
        data = cursor.fetchall()
        conn.close()
        return data

    def update_product(self, product_id, name, company, category, price, stock):
        clean_name = name.strip()
        clean_comp = company.strip().title()
        clean_cat = category.strip().title()
        if not clean_name:
            return False, "⚠️ El nombre del producto es obligatorio."
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name = ?, company = ?, category = ?, price = ?, stock = ? WHERE id = ?",
                (clean_name, clean_comp, clean_cat, float(price), int(stock), product_id)
            )
            conn.commit()
            affected = cursor.rowcount
            conn.close()
            if affected > 0:
                return True, "✅ Producto actualizado con éxito."
            return False, "❌ Producto no encontrado con ese ID."
        except Exception as e:
            return False, f"❌ Error al actualizar: {e}"

    # --- FACTURACIÓN MÚLTIPLE ---
    def create_invoice(self, client_id, worker_id, items):
        if not items:
            return False, "⚠️ El carrito de compras está vacío.", None

        conn = self.db.connect()
        cursor = conn.cursor()
        
        try:
            total_invoice = 0.0
            validated_items = []

            for prod_id, qty in items:
                cursor.execute("SELECT price, stock FROM products WHERE id = ?", (prod_id,))
                prod = cursor.fetchone()
                if not prod:
                    raise Exception(f"Producto con ID {prod_id} no encontrado.")
                
                price, stock = prod
                if stock < qty:
                    raise Exception(f"Stock insuficiente para el producto ID {prod_id}. Disponibles: {stock}")
                
                subtotal = price * qty
                total_invoice += subtotal
                validated_items.append((prod_id, qty, subtotal))

            cursor.execute(
                "INSERT INTO invoices (client_id, worker_id, total_amount) VALUES (?, ?, ?)",
                (client_id, worker_id, total_invoice)
            )
            invoice_id = cursor.lastrowid

            for prod_id, qty, subtotal in validated_items:
                cursor.execute(
                    "INSERT INTO invoice_items (invoice_id, product_id, quantity, subtotal) VALUES (?, ?, ?, ?)",
                    (invoice_id, prod_id, qty, subtotal)
                )
                cursor.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ?",
                    (qty, prod_id)
                )

            conn.commit()
            conn.close()
            return True, f"✅ Factura #{invoice_id} emitida con éxito. Total: ${total_invoice:.2f}", invoice_id

        except Exception as e:
            conn.rollback()
            conn.close()
            return False, f"❌ Error en la transacción de venta: {e}", None

    def get_all_invoices(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id, i.date, i.total_amount, c.name, w.name
            FROM invoices i
            LEFT JOIN clients c ON i.client_id = c.id
            LEFT JOIN workers w ON i.worker_id = w.id
            ORDER BY i.id DESC
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    def get_sales_chart_data(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, SUM(ii.quantity) 
            FROM invoice_items ii
            JOIN products p ON ii.product_id = p.id
            GROUP BY p.id
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    def get_invoice_details(self, invoice_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.id, i.date, i.total_amount, c.name, c.email, c.phone, c.address, w.name
            FROM invoices i
            LEFT JOIN clients c ON i.client_id = c.id
            LEFT JOIN workers w ON i.worker_id = w.id
            WHERE i.id = ?
        """, (invoice_id,))
        invoice = cursor.fetchone()
        
        cursor.execute("""
            SELECT p.name, p.company, p.category, ii.quantity, ii.subtotal, (ii.subtotal / ii.quantity) as unit_price
            FROM invoice_items ii
            JOIN products p ON ii.product_id = p.id
            WHERE ii.invoice_id = ?
        """, (invoice_id,))
        items = cursor.fetchall()
        conn.close()
        return invoice, items

    def generate_invoice_pdf(self, invoice_id):
        invoice, items = self.get_invoice_details(invoice_id)
        if not invoice:
            return False, "❌ Factura no encontrada."
        
        folder_name = "facturas_pdf"
        os.makedirs(folder_name, exist_ok=True)
        
        filename = os.path.join(folder_name, f"Factura_{invoice_id}.pdf")
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph(f"<b>FACTURA COMERCIAL #{invoice[0]}</b>", styles['Title']))
        story.append(Spacer(1, 12))
        
        worker_name = invoice[7] if invoice[7] else 'No asignado'
        info_text = f"""
        <b>Fecha de emisión:</b> {invoice[1]}<br/>
        <b>Vendedor / Empleado:</b> {worker_name}<br/>
        <b>Cliente:</b> {invoice[3]}<br/>
        <b>Correo:</b> {invoice[4] if invoice[4] else 'N/A'}<br/>
        <b>Teléfono:</b> {invoice[5] if invoice[5] else 'N/A'}<br/>
        <b>Dirección:</b> {invoice[6] if invoice[6] else 'N/A'}
        """
        story.append(Paragraph(info_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        table_data = [["Producto", "Empresa", "Categoría", "Cant.", "Precio Unit.", "Subtotal"]]
        for prod_name, company, category, qty, subtotal, unit_price in items:
            comp_str = company if company else 'N/A'
            cat_str = category if category else 'General'
            table_data.append([prod_name, comp_str, cat_str, str(qty), f"${unit_price:.2f}", f"${subtotal:.2f}"])
            
        t = Table(table_data, colWidths=[130, 90, 90, 50, 85, 85])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1f6aa5")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f8f9fa")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ]))
        story.append(t)
        story.append(Spacer(1, 15))
        
        story.append(Paragraph(f"<b>TOTAL A PAGAR: ${invoice[2]:.2f}</b>", styles['Heading2']))
        
        doc.build(story)
        return True, f"📄 Factura PDF guardada en '{folder_name}/Factura_{invoice_id}.pdf'"