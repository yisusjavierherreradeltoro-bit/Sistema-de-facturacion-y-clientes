import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from billing_manager import BillingManager

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class BillingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.manager = BillingManager()
        self.last_invoice_id = None
        self.cart = [] 
        
        self.title("CRM & Billing Pro - Sistema de Gestión Comercial")
        self.geometry("1100x780")
        self.minsize(950, 700)
        
        # Contenedor Superior (Cabecera)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=15)
        
        self.title_label = ctk.CTkLabel(header_frame, text="⚡ CRM & Billing Pro", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(side="left")
        
        self.subtitle_label = ctk.CTkLabel(header_frame, text="Sistema Integral de Ventas, Clientes e Inventario", font=ctk.CTkFont(size=13), text_color="gray")
        self.subtitle_label.pack(side="left", padx=15, pady=5)
        
        # Pestañas Principales
        self.tabview = ctk.CTkTabview(self, width=1040, height=680, corner_radius=12)
        self.tabview.pack(pady=5, padx=20, fill="both", expand=True)
        
        self.tab_clients = self.tabview.add("👥 Clientes")
        self.tab_workers = self.tabview.add("👨‍💼 Empleados")
        self.tab_products = self.tabview.add("📦 Productos")
        self.tab_categories = self.tabview.add("📂 Categorías")
        self.tab_billing = self.tabview.add("🧾 Facturación")
        self.tab_history = self.tabview.add("📜 Historial")
        self.tab_charts = self.tabview.add("📊 Analíticas")
        
        self.setup_clients_tab()
        self.setup_workers_tab()
        self.setup_products_tab()
        self.setup_categories_tab()
        self.setup_billing_tab()
        self.setup_history_tab()
        self.setup_charts_tab()
        
        self.refresh_all()

    def setup_clients_tab(self):
        card = ctk.CTkFrame(self.tab_clients, corner_radius=10)
        card.pack(pady=15, padx=15, fill="x")
        
        ctk.CTkLabel(card, text="Registrar Nuevo Cliente", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(12, 5))
        
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(fill="x", padx=15, pady=10)
        
        self.c_name = ctk.CTkEntry(form, placeholder_text="Nombre completo...", width=200, height=35)
        self.c_name.pack(side="left", padx=5)
        
        self.c_email = ctk.CTkEntry(form, placeholder_text="Correo electrónico", width=180, height=35)
        self.c_email.pack(side="left", padx=5)
        
        self.c_phone = ctk.CTkEntry(form, placeholder_text="Teléfono", width=130, height=35)
        self.c_phone.pack(side="left", padx=5)
        
        self.c_address = ctk.CTkEntry(form, placeholder_text="Dirección", width=200, height=35)
        self.c_address.pack(side="left", padx=5)
        
        btn_add = ctk.CTkButton(form, text="Guardar", fg_color="#2fa572", hover_color="#248f5e", command=self.add_client_gui, width=110, height=35)
        btn_add.pack(side="left", padx=10)
        
        # Tabla de visualización
        table_card = ctk.CTkFrame(self.tab_clients, corner_radius=10)
        table_card.pack(pady=5, padx=15, fill="both", expand=True)
        
        ctk.CTkLabel(table_card, text="Directorio de Clientes", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.tb_clients = ctk.CTkTextbox(table_card, width=960, height=390, font=ctk.CTkFont(family="Consolas", size=12))
        self.tb_clients.pack(pady=10, padx=15, fill="both", expand=True)
        self.tb_clients.configure(state="disabled")

    def setup_workers_tab(self):
        card = ctk.CTkFrame(self.tab_workers, corner_radius=10)
        card.pack(pady=15, padx=15, fill="x")
        
        ctk.CTkLabel(card, text="Gestión de Empleados / Vendedores", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(12, 5))
        
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(fill="x", padx=15, pady=10)

        self.w_id_edit = ctk.CTkEntry(form, placeholder_text="ID (Editar)", width=100, height=35)
        self.w_id_edit.pack(side="left", padx=5)

        self.w_name = ctk.CTkEntry(form, placeholder_text="Nombre del empleado...", width=320, height=35)
        self.w_name.pack(side="left", padx=5)
        
        btn_add = ctk.CTkButton(form, text="Registrar", fg_color="#3498db", hover_color="#2980b9", command=self.add_worker_gui, width=120, height=35)
        btn_add.pack(side="left", padx=10)

        btn_edit = ctk.CTkButton(form, text="Actualizar ID", fg_color="#e67e22", hover_color="#d35400", command=self.update_worker_gui, width=120, height=35)
        btn_edit.pack(side="left", padx=5)
        
        table_card = ctk.CTkFrame(self.tab_workers, corner_radius=10)
        table_card.pack(pady=5, padx=15, fill="both", expand=True)
        
        ctk.CTkLabel(table_card, text="Personal Activo", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.tb_workers = ctk.CTkTextbox(table_card, width=960, height=390, font=ctk.CTkFont(family="Consolas", size=12))
        self.tb_workers.pack(pady=10, padx=15, fill="both", expand=True)
        self.tb_workers.configure(state="disabled")

    def setup_products_tab(self):
        card = ctk.CTkFrame(self.tab_products, corner_radius=10)
        card.pack(pady=15, padx=15, fill="x")

        ctk.CTkLabel(card, text="Control de Inventario y Productos", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(12, 5))

        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(fill="x", padx=15, pady=10)

        self.p_id_edit = ctk.CTkEntry(form, placeholder_text="ID", width=70, height=35)
        self.p_id_edit.pack(side="left", padx=3)

        self.p_name = ctk.CTkEntry(form, placeholder_text="Producto...", width=160, height=35)
        self.p_name.pack(side="left", padx=3)
        
        self.p_company = ctk.CTkEntry(form, placeholder_text="Marca/Empresa...", width=140, height=35)
        self.p_company.pack(side="left", padx=3)

        self.p_category = ctk.CTkEntry(form, placeholder_text="Categoría...", width=130, height=35)
        self.p_category.pack(side="left", padx=3)
        
        self.p_price = ctk.CTkEntry(form, placeholder_text="Precio ($)", width=90, height=35)
        self.p_price.pack(side="left", padx=3)
        
        self.p_stock = ctk.CTkEntry(form, placeholder_text="Stock", width=70, height=35)
        self.p_stock.pack(side="left", padx=3)
        
        btn_add = ctk.CTkButton(form, text="Añadir", fg_color="#2fa572", hover_color="#248f5e", command=self.add_product_gui, width=85, height=35)
        btn_add.pack(side="left", padx=5)

        btn_edit = ctk.CTkButton(form, text="Editar", fg_color="#e67e22", hover_color="#d35400", command=self.update_product_gui, width=85, height=35)
        btn_edit.pack(side="left", padx=5)
        
        table_card = ctk.CTkFrame(self.tab_products, corner_radius=10)
        table_card.pack(pady=5, padx=15, fill="both", expand=True)
        
        ctk.CTkLabel(table_card, text="Listado General de Inventario", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        self.tb_products = ctk.CTkTextbox(table_card, width=960, height=350, font=ctk.CTkFont(family="Consolas", size=12))
        self.tb_products.pack(pady=10, padx=15, fill="both", expand=True)
        self.tb_products.configure(state="disabled")

    def setup_categories_tab(self):
        card = ctk.CTkFrame(self.tab_categories, corner_radius=10)
        card.pack(pady=15, padx=15, fill="both", expand=True)
        
        top_row = ctk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(top_row, text="Catálogo Organizado por Categorías", font=ctk.CTkFont(size=15, weight="bold")).pack(side="left")
        btn_refresh = ctk.CTkButton(top_row, text="Actualizar Catálogo 🔄", command=self.refresh_categories_view, fg_color="#3498db", width=160, height=32)
        btn_refresh.pack(side="right")
        
        self.tb_categories = ctk.CTkTextbox(card, width=940, height=450, font=ctk.CTkFont(family="Consolas", size=13))
        self.tb_categories.pack(pady=10, padx=15, fill="both", expand=True)
        self.tb_categories.configure(state="disabled")

    def setup_billing_tab(self):
        card = ctk.CTkFrame(self.tab_billing, corner_radius=10)
        card.pack(pady=10, padx=15, fill="x")
        
        ctk.CTkLabel(card, text="Punto de Venta - Carrito Multiproducto", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))
        
        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(fill="x", padx=10, pady=5)
        
        top_row = ctk.CTkFrame(form, fg_color="transparent")
        top_row.pack(fill="x", padx=5, pady=5)

        w_frame = ctk.CTkFrame(top_row, fg_color="transparent")
        w_frame.pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkLabel(w_frame, text="Vendedor Asignado:").pack(anchor="w")
        self.bill_worker_combo = ctk.CTkComboBox(w_frame, values=["Sin empleados"], width=300, height=32)
        self.bill_worker_combo.pack(anchor="w", pady=2)

        c_frame = ctk.CTkFrame(top_row, fg_color="transparent")
        c_frame.pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkLabel(c_frame, text="Cliente CRM:").pack(anchor="w")
        self.bill_client_combo = ctk.CTkComboBox(c_frame, values=["Sin clientes"], width=300, height=32)
        self.bill_client_combo.pack(anchor="w", pady=2)

        prod_row = ctk.CTkFrame(form, fg_color="transparent")
        prod_row.pack(fill="x", padx=5, pady=8)

        p_frame = ctk.CTkFrame(prod_row, fg_color="transparent")
        p_frame.pack(side="left", padx=5, expand=True, fill="x")
        ctk.CTkLabel(p_frame, text="Seleccionar Producto:").pack(anchor="w")
        self.bill_prod_combo = ctk.CTkComboBox(p_frame, values=["Sin productos"], width=380, height=32)
        self.bill_prod_combo.pack(anchor="w", pady=2)

        q_frame = ctk.CTkFrame(prod_row, fg_color="transparent")
        q_frame.pack(side="left", padx=5)
        ctk.CTkLabel(q_frame, text="Cantidad:").pack(anchor="w")
        self.bill_qty = ctk.CTkEntry(q_frame, placeholder_text="1", width=90, height=32)
        self.bill_qty.pack(anchor="w", pady=2)

        btn_add_cart = ctk.CTkButton(prod_row, text="➕ Agregar al Carrito", fg_color="#3498db", hover_color="#2980b9", command=self.add_to_cart, width=150, height=32)
        btn_add_cart.pack(side="left", padx=10, pady=18)

        # Visualizador del Carrito
        cart_card = ctk.CTkFrame(self.tab_billing, corner_radius=10)
        cart_card.pack(pady=5, padx=15, fill="both", expand=True)

        self.tb_cart = ctk.CTkTextbox(cart_card, width=940, height=190, font=ctk.CTkFont(family="Consolas", size=12))
        self.tb_cart.pack(pady=10, padx=15, fill="both", expand=True)
        self.tb_cart.configure(state="disabled")

        action_row = ctk.CTkFrame(self.tab_billing, fg_color="transparent")
        action_row.pack(pady=8)

        btn_clear_cart = ctk.CTkButton(action_row, text="🗑️ Vaciar Carrito", fg_color="#e74c3c", hover_color="#c0392b", command=self.clear_cart, width=140, height=35)
        btn_clear_cart.pack(side="left", padx=8)

        btn_facturar = ctk.CTkButton(action_row, text="💰 Procesar y Emitir Factura", fg_color="#2fa572", hover_color="#248f5e", command=self.create_invoice_gui, width=190, height=35)
        btn_facturar.pack(side="left", padx=8)

        self.btn_pdf = ctk.CTkButton(action_row, text="📄 Descargar PDF Última Factura", fg_color="#e67e22", hover_color="#d35400", command=self.download_pdf_gui, width=220, height=35, state="disabled")
        self.btn_pdf.pack(side="left", padx=8)
        
        self.bill_status = ctk.CTkLabel(self.tab_billing, text="", font=ctk.CTkFont(size=13, weight="bold"))
        self.bill_status.pack(pady=2)

    def setup_history_tab(self):
        card = ctk.CTkFrame(self.tab_history, corner_radius=10)
        card.pack(pady=15, padx=15, fill="both", expand=True)
        
        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(top_frame, text="Historial General de Transacciones", font=ctk.CTkFont(size=15, weight="bold")).pack(side="left")
        
        btn_refresh = ctk.CTkButton(top_frame, text="Actualizar 🔄", command=self.refresh_history, fg_color="#3498db", width=120, height=32)
        btn_refresh.pack(side="right", padx=5)
        
        search_frame = ctk.CTkFrame(card, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=5)
        
        self.inv_id_entry = ctk.CTkEntry(search_frame, placeholder_text="ID de Factura...", width=140, height=32)
        self.inv_id_entry.pack(side="left", padx=5)
        
        btn_dl = ctk.CTkButton(search_frame, text="Descargar PDF de esta Factura 📄", command=self.download_specific_pdf, fg_color="#e67e22", hover_color="#d35400", height=32)
        btn_dl.pack(side="left", padx=10)
        
        self.history_status = ctk.CTkLabel(search_frame, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.history_status.pack(side="left", padx=15)

        self.tb_history = ctk.CTkTextbox(card, width=940, height=380, font=ctk.CTkFont(family="Consolas", size=12))
        self.tb_history.pack(pady=10, padx=15, fill="both", expand=True)
        self.tb_history.configure(state="disabled")

    def setup_charts_tab(self):
        card = ctk.CTkFrame(self.tab_charts, corner_radius=10)
        card.pack(pady=15, padx=15, fill="both", expand=True)
        
        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(top_frame, text="Estadísticas de Salida de Productos", font=ctk.CTkFont(size=15, weight="bold")).pack(side="left")
        btn_refresh_chart = ctk.CTkButton(top_frame, text="Actualizar Gráfico 🔄", command=self.render_chart, fg_color="#3498db", width=140, height=32)
        btn_refresh_chart.pack(side="right")
        
        self.chart_frame = ctk.CTkFrame(card, fg_color="transparent")
        self.chart_frame.pack(pady=10, padx=15, fill="both", expand=True)
        
        self.render_chart()

    def render_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        data = self.manager.get_sales_chart_data()
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
        
        if not data:
            ax.text(0.5, 0.5, "Sin datos de ventas registrados", horizontalalignment='center', verticalalignment='center', fontsize=12)
            ax.axis('off')
        else:
            products = [row[0] for row in data]
            quantities = [row[1] for row in data]
            bars = ax.bar(products, quantities, color="#1f6aa5")
            ax.set_title("Unidades Vendidas por Producto", fontsize=12, fontweight='bold', color="#333333")
            ax.set_ylabel("Cantidad", fontsize=10)
            plt.xticks(rotation=15, ha='right')
            
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)
                                
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_all(self):
        clients = self.manager.get_clients()
        self.tb_clients.configure(state="normal")
        self.tb_clients.delete("1.0", "end")
        if not clients:
            self.tb_clients.insert("end", "📭 No hay clientes registrados en el CRM.\n")
            self.bill_client_combo.configure(values=["Sin clientes"])
        else:
            self.tb_clients.insert("end", f"{'ID':<4} | {'NOMBRE':<25} | {'CORREO':<25} | {'TELÉFONO':<15} | {'DIRECCIÓN'}\n")
            self.tb_clients.insert("end", "-" * 95 + "\n")
            c_vals = []
            for cid, name, email, phone, addr in clients:
                self.tb_clients.insert("end", f"{cid:<4} | {name:<25} | {email:<25} | {phone:<15} | {addr}\n")
                c_vals.append(f"{cid}: {name}")
            self.bill_client_combo.configure(values=c_vals)
            self.bill_client_combo.set(c_vals[0])
        self.tb_clients.configure(state="disabled")

        workers = self.manager.get_workers()
        self.tb_workers.configure(state="normal")
        self.tb_workers.delete("1.0", "end")
        if not workers:
            self.tb_workers.insert("end", "📭 No hay empleados registrados.\n")
            self.bill_worker_combo.configure(values=["Sin empleados"])
        else:
            self.tb_workers.insert("end", f"{'ID':<4} | {'NOMBRE DEL EMPLEADO / VENDEDOR'}\n")
            self.tb_workers.insert("end", "-" * 40 + "\n")
            w_vals = []
            for wid, wname in workers:
                self.tb_workers.insert("end", f"{wid:<4} | {wname}\n")
                w_vals.append(f"{wid}: {wname}")
            self.bill_worker_combo.configure(values=w_vals)
            self.bill_worker_combo.set(w_vals[0])
        self.tb_workers.configure(state="disabled")

        products = self.manager.get_products()
        self.tb_products.configure(state="normal")
        self.tb_products.delete("1.0", "end")
        if not products:
            self.tb_products.insert("end", "📭 No hay productos registrados en el inventario.\n")
            self.bill_prod_combo.configure(values=["Sin productos"])
        else:
            self.tb_products.insert("end", f"{'ID':<4} | {'PRODUCTO':<20} | {'EMPRESA':<15} | {'CATEGORÍA':<15} | {'PRECIO':<10} | {'STOCK'}\n")
            self.tb_products.insert("end", "-" * 85 + "\n")
            p_vals = []
            for pid, name, company, category, price, stock in products:
                comp_str = company if company else 'N/A'
                cat_str = category if category else 'General'
                self.tb_products.insert("end", f"{pid:<4} | {name:<20} | {comp_str:<15} | {cat_str:<15} | ${price:<9.2f} | {stock}\n")
                p_vals.append(f"{pid}: {name} ({cat_str}) - Stock: {stock}")
            self.bill_prod_combo.configure(values=p_vals)
            self.bill_prod_combo.set(p_vals[0])
        self.tb_products.configure(state="disabled")
        
        self.refresh_categories_view()
        self.refresh_history()
        self.render_chart()

    def refresh_categories_view(self):
        products = self.manager.get_products()
        self.tb_categories.configure(state="normal")
        self.tb_categories.delete("1.0", "end")
        
        if not products:
            self.tb_categories.insert("end", "📭 No hay productos ni categorías registradas.\n")
        else:
            cats = {}
            for pid, name, company, category, price, stock in products:
                cat_name = category.strip() if category else "General"
                if cat_name not in cats:
                    cats[cat_name] = []
                cats[cat_name].append((pid, name, company, price, stock))

            for cat, prods in cats.items():
                self.tb_categories.insert("end", f"📂 CATEGORÍA: {cat.upper()}\n")
                self.tb_categories.insert("end", f"   {'ID':<4} | {'PRODUCTO':<22} | {'EMPRESA':<18} | {'PRECIO':<10} | {'STOCK'}\n")
                self.tb_categories.insert("end", "   " + "-" * 70 + "\n")
                for pid, name, company, price, stock in prods:
                    comp_str = company if company else 'N/A'
                    self.tb_categories.insert("end", f"   {pid:<4} | {name:<22} | {comp_str:<18} | ${price:<9.2f} | {stock}\n")
                self.tb_categories.insert("end", "\n")
                
        self.tb_categories.configure(state="disabled")

    def refresh_history(self):
        invoices = self.manager.get_all_invoices()
        self.tb_history.configure(state="normal")
        self.tb_history.delete("1.0", "end")
        
        if not invoices:
            self.tb_history.insert("end", "📭 No hay facturas emitidas en el historial.\n")
        else:
            self.tb_history.insert("end", f"{'ID':<6} | {'FECHA Y HORA':<20} | {'CLIENTE':<25} | {'VENDEDOR':<20} | {'TOTAL'}\n")
            self.tb_history.insert("end", "-" * 88 + "\n")
            for inv_id, date, total, client, worker in invoices:
                c_str = client if client else "N/A"
                w_str = worker if worker else "N/A"
                self.tb_history.insert("end", f"{inv_id:<6} | {date:<20} | {c_str:<25} | {w_str:<20} | ${total:.2f}\n")
                
        self.tb_history.configure(state="disabled")

    def download_specific_pdf(self):
        try:
            inv_id = int(self.inv_id_entry.get())
            success, msg = self.manager.generate_invoice_pdf(inv_id)
            self.history_status.configure(text=msg, text_color="#2fa572" if success else "#e74c3c")
            if success:
                self.inv_id_entry.delete(0, "end")
        except ValueError:
            self.history_status.configure(text="⚠️ Ingresa un ID numérico válido.", text_color="#e74c3c")

    def add_client_gui(self):
        success, msg = self.manager.add_client(
            self.c_name.get(), self.c_email.get(), self.c_phone.get(), self.c_address.get()
        )
        if success:
            self.c_name.delete(0, "end")
            self.c_email.delete(0, "end")
            self.c_phone.delete(0, "end")
            self.c_address.delete(0, "end")
            self.refresh_all()

    def add_worker_gui(self):
        success, msg = self.manager.add_worker(self.w_name.get())
        if success:
            self.w_name.delete(0, "end")
            self.refresh_all()

    def update_worker_gui(self):
        try:
            w_id = int(self.w_id_edit.get())
            success, msg = self.manager.update_worker(w_id, self.w_name.get())
            if success:
                self.w_id_edit.delete(0, "end")
                self.w_name.delete(0, "end")
                self.refresh_all()
        except ValueError:
            pass

    def add_product_gui(self):
        try:
            success, msg = self.manager.add_product(
                self.p_name.get(), self.p_company.get(), self.p_category.get(), float(self.p_price.get()), int(self.p_stock.get())
            )
            if success:
                self.p_name.delete(0, "end")
                self.p_company.delete(0, "end")
                self.p_category.delete(0, "end")
                self.p_price.delete(0, "end")
                self.p_stock.delete(0, "end")
                self.refresh_all()
        except ValueError:
            pass

    def update_product_gui(self):
        try:
            p_id = int(self.p_id_edit.get())
            success, msg = self.manager.update_product(
                p_id, self.p_name.get(), self.p_company.get(), self.p_category.get(), float(self.p_price.get()), int(self.p_stock.get())
            )
            if success:
                self.p_id_edit.delete(0, "end")
                self.p_name.delete(0, "end")
                self.p_company.delete(0, "end")
                self.p_category.delete(0, "end")
                self.p_price.delete(0, "end")
                self.p_stock.delete(0, "end")
                self.refresh_all()
        except ValueError:
            pass

    def add_to_cart(self):
        p_str = self.bill_prod_combo.get()
        if "Sin" in p_str:
            return
        try:
            prod_id = int(p_str.split(":")[0])
            qty = int(self.bill_qty.get())
            if qty <= 0:
                return
            
            products = self.manager.get_products()
            prod_info = next((p for p in products if p[0] == prod_id), None)
            if not prod_info:
                return
            
            name, price = prod_info[1], prod_info[4]
            subtotal = price * qty

            self.cart.append({'id': prod_id, 'name': name, 'price': price, 'qty': qty, 'subtotal': subtotal})
            self.update_cart_display()
            self.bill_qty.delete(0, "end")
        except ValueError:
            pass

    def update_cart_display(self):
        self.tb_cart.configure(state="normal")
        self.tb_cart.delete("1.0", "end")
        self.tb_cart.insert("end", f"🛒 CARRITO DE COMPRAS ACTUAL:\n")
        self.tb_cart.insert("end", f"{'PRODUCTO':<28} | {'CANT':<6} | {'PRECIO UNIT':<12} | {'SUBTOTAL'}\n")
        self.tb_cart.insert("end", "-" * 68 + "\n")
        
        total = 0.0
        for item in self.cart:
            self.tb_cart.insert("end", f"{item['name']:<28} | {item['qty']:<6} | ${item['price']:<11.2f} | ${item['subtotal']:.2f}\n")
            total += item['subtotal']
            
        self.tb_cart.insert("end", "-" * 68 + "\n")
        self.tb_cart.insert("end", f"TOTAL ESTIMADO DEL CARRITO: ${total:.2f}\n")
        self.tb_cart.configure(state="disabled")

    def clear_cart(self):
        self.cart = []
        self.update_cart_display()

    def create_invoice_gui(self):
        w_str = self.bill_worker_combo.get()
        c_str = self.bill_client_combo.get()
        
        if "Sin" in w_str or "Sin" in c_str:
            self.bill_status.configure(text="⚠️ Selecciona un empleado y un cliente válidos.", text_color="#e74c3c")
            return
        if not self.cart:
            self.bill_status.configure(text="⚠️ El carrito de compras está vacío.", text_color="#e74c3c")
            return
            
        try:
            worker_id = int(w_str.split(":")[0])
            client_id = int(c_str.split(":")[0])
            
            items_to_bill = [(item['id'], item['qty']) for item in self.cart]
            
            success, msg, inv_id = self.manager.create_invoice(client_id, worker_id, items_to_bill)
            self.bill_status.configure(text=msg, text_color="#2fa572" if success else "#e74c3c")
            if success:
                self.last_invoice_id = inv_id
                self.btn_pdf.configure(state="normal")
                self.clear_cart()
                self.refresh_all()
        except ValueError as e:
            self.bill_status.configure(text=f"⚠️ Error: {e}", text_color="#e74c3c")

    def download_pdf_gui(self):
        if self.last_invoice_id:
            success, msg = self.manager.generate_invoice_pdf(self.last_invoice_id)
            self.bill_status.configure(text=msg, text_color="#2fa572" if success else "#e74c3c")

if __name__ == "__main__":
    app = BillingApp()
    app.mainloop()