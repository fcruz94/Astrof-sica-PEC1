import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from src.simbad_client import query_simbad  # Importamos la nueva función

class StarInputForm:
    def __init__(self, root, on_submit_callback):
        self.root = root
        self.on_submit = on_submit_callback
        self.stars_data = []
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Caracterización de Estrellas - Entrada de Datos")
        
        # Ventana principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Venatana de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Datos de la Estrella", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Configuración del grid
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Campos del formulario
        row = 0
        ttk.Label(input_frame, text="Nombre de la estrella:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=row, column=1, sticky=tk.EW, padx=5)
        row += 1
        
        # Botón de búsqueda en SIMBAD
        self.search_btn = ttk.Button(input_frame, text="Buscar en SIMBAD", 
                                   command=self.fetch_simbad_data,
                                   state='disabled')
        self.search_btn.grid(row=row, columnspan=2, pady=5)
        row += 1
        
        # Campos de datos
        ttk.Label(input_frame, text="φ Desplazamiento angular (\":").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.angular_displacement_entry = ttk.Entry(input_frame)
        self.angular_displacement_entry.grid(row=row, column=1, sticky=tk.EW, padx=5)
        row += 1
        
        ttk.Label(input_frame, text="1ª Observación:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.date1_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd')
        self.date1_entry.grid(row=row, column=1, sticky=tk.EW, padx=5)
        row += 1
        
        ttk.Label(input_frame, text="2ª Observación:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.date2_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd')
        self.date2_entry.grid(row=row, column=1, sticky=tk.EW, padx=5)
        row += 1
        
        ttk.Label(input_frame, text="Δt (años):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.delta_time_label = ttk.Label(input_frame, text="0.0000")
        self.delta_time_label.grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1
        
        ttk.Label(input_frame, text="π Paralaje (\":").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.parallax_entry = ttk.Entry(input_frame)
        self.parallax_entry.grid(row=row, column=1, sticky=tk.EW, padx=5)
        row += 1
        
        ttk.Label(input_frame, text="Velocidad radial (km/s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.vr_entry = ttk.Entry(input_frame)
        self.vr_entry.grid(row=row, column=1, sticky=tk.EW, padx=5)
        row += 1
        
        ttk.Label(input_frame, text="Magnitud B:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.b_mag_entry = ttk.Entry(input_frame)
        self.b_mag_entry.grid(row=row, column=1, sticky=tk.EW, padx=5)
        row += 1
        
        ttk.Label(input_frame, text="Magnitud V:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.v_mag_entry = ttk.Entry(input_frame)
        self.v_mag_entry.grid(row=row, column=1, sticky=tk.EW, padx=5)
        row += 1
        
        # Botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Añadir Estrella", command=self.add_star).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calcular Resultados", command=self.submit_data).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_form).pack(side=tk.RIGHT, padx=5)
        
        # Eventos
        self.name_entry.bind('<KeyRelease>', self.toggle_simbad_button)
        self.date1_entry.bind("<<DateEntrySelected>>", self.update_delta_time)
        self.date2_entry.bind("<<DateEntrySelected>>", self.update_delta_time)
    
    def toggle_simbad_button(self, event=None):
        """Habilita/deshabilita el botón de SIMBAD según haya texto"""
        self.search_btn['state'] = 'normal' if self.name_entry.get().strip() else 'disabled'
    
    def fetch_simbad_data(self):
        """Versión corregida con manejo adecuado de actualización de UI"""
        star_name = self.name_entry.get().strip()
        if not star_name:
            messagebox.showwarning("Advertencia", "Introduce un nombre de estrella primero")
            return
            
        try:
            # Configurar cursor de espera
            self.root.config(cursor='watch')
            self.root.update()  # Usar update() en lugar de update_idletasks()
            
            data = query_simbad(star_name)
            if not data:
                messagebox.showwarning("SIMBAD", f"No se encontró la estrella '{star_name}'")
                return
            
            # Actualizar solo campos con datos válidos
            updated = []
            if data['radial_velocity_km_s'] is not None:
                self.vr_entry.delete(0, tk.END)
                self.vr_entry.insert(0, f"{data['radial_velocity_km_s']:.2f}")
                updated.append("Velocidad radial")
                
            if data['parallax_arcsec'] is not None:
                self.parallax_entry.delete(0, tk.END)
                self.parallax_entry.insert(0, f"{data['parallax_arcsec']:.6f}")
                updated.append("Paralaje")
                
            if data['mag_B'] is not None:
                self.b_mag_entry.delete(0, tk.END)
                self.b_mag_entry.insert(0, f"{data['mag_B']:.3f}")
                updated.append("Magnitud B")
                
            if data['mag_V'] is not None:
                self.v_mag_entry.delete(0, tk.END)
                self.v_mag_entry.insert(0, f"{data['mag_V']:.3f}")
                updated.append("Magnitud V")
            
            if not updated:
                messagebox.showinfo("SIMBAD", 
                                 f"Se encontró '{star_name}' pero sin los datos requeridos\n"
                                 "Complete los campos manualmente")
            else:
                messagebox.showinfo("SIMBAD", 
                                 f"Datos cargados para {star_name}:\n"
                                 f"{', '.join(updated)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al consultar SIMBAD:\n{str(e)}")
        finally:
            # Restaurar cursor normal
            self.root.config(cursor='')
            self.root.update()
    
    def update_delta_time(self, event=None):
        """Calcula Δt en años cuando se seleccionan fechas"""
        try:
            date1 = self.date1_entry.get_date()
            date2 = self.date2_entry.get_date()
            
            if date1 and date2:
                delta_days = (date2 - date1).days
                if delta_days < 0:
                    raise ValueError("La segunda fecha debe ser posterior")
                delta_years = delta_days / 365.25
                self.delta_time_label.config(text=f"{delta_years:.4f}")
        except Exception as e:
            messagebox.showerror("Error", f"Error en fechas: {str(e)}")
            self.delta_time_label.config(text="0.0000")
    
    def add_star(self):
        """Añade los datos de la estrella actual a la lista"""
        try:
            # Validación básica
            star_name = self.name_entry.get().strip()
            if not star_name:
                raise ValueError("El nombre de la estrella es requerido")
                
            delta_time = float(self.delta_time_label.cget("text"))
            if delta_time <= 0:
                raise ValueError("Δt debe ser positivo (la segunda fecha debe ser posterior)")
            
            # Crear diccionario con los datos
            star_data = {
                'name': star_name,
                'angular_displacement': float(self.angular_displacement_entry.get()),
                'date1': self.date1_entry.get_date(),
                'date2': self.date2_entry.get_date(),
                'delta_time': delta_time,
                'parallax': float(self.parallax_entry.get()),
                'vr': float(self.vr_entry.get()),
                'B': float(self.b_mag_entry.get()),
                'V': float(self.v_mag_entry.get())
            }
            
            # Validaciones adicionales
            if star_data['parallax'] <= 0:
                raise ValueError("El paralaje debe ser positivo")
            if star_data['angular_displacement'] <= 0:
                raise ValueError("El desplazamiento angular debe ser positivo")
                
            self.stars_data.append(star_data)
            self.clear_form()
            messagebox.showinfo("Éxito", f"Estrella {star_name} añadida correctamente")
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error: {str(e)}")
    
    def submit_data(self):
        """Envía todos los datos para procesamiento"""
        if not self.stars_data:
            messagebox.showwarning("Advertencia", "No hay datos de estrellas para procesar")
            return
        
        self.on_submit(self.stars_data)
    
    def clear_form(self):
        """Limpia el formulario y establece valores por defecto"""
        # Limpiar campos
        for entry in [self.name_entry, self.angular_displacement_entry,
                     self.parallax_entry, self.vr_entry,
                     self.b_mag_entry, self.v_mag_entry]:
            entry.delete(0, tk.END)
        
        # Establecer fechas actuales
        today = datetime.now()
        self.date1_entry.set_date(today)
        self.date2_entry.set_date(today)
        
        # Resetear Δt
        self.delta_time_label.config(text="0.0000")
        
        # Deshabilitar botón SIMBAD
        self.search_btn['state'] = 'disabled'# -*- coding: utf-8 -*-

