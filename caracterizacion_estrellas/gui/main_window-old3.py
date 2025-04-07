import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class StarInputForm:
    def __init__(self, root, on_submit_callback):
        self.root = root
        self.on_submit = on_submit_callback
        self.stars_data = []
        
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("Entrada de Datos Estelares")
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Datos de la Estrella", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Campos del formulario
        ttk.Label(input_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(input_frame, text="φ Desplazamiento angular (\":").grid(row=1, column=0, sticky=tk.W)
        self.angular_displacement_entry = ttk.Entry(input_frame)
        self.angular_displacement_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(input_frame, text="1ª Observación:").grid(row=2, column=0, sticky=tk.W)
        self.date1_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd')
        self.date1_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(input_frame, text="2ª Observación:").grid(row=3, column=0, sticky=tk.W)
        self.date2_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd')
        self.date2_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Δt (años):").grid(row=4, column=0, sticky=tk.W)
        self.delta_time_label = ttk.Label(input_frame, text="0.00")
        self.delta_time_label.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(input_frame, text="π Paralaje (\":").grid(row=5, column=0, sticky=tk.W)
        self.parallax_entry = ttk.Entry(input_frame)
        self.parallax_entry.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Velocidad radial (km/s):").grid(row=6, column=0, sticky=tk.W)
        self.vr_entry = ttk.Entry(input_frame)
        self.vr_entry.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Magnitud B:").grid(row=7, column=0, sticky=tk.W)
        self.b_mag_entry = ttk.Entry(input_frame)
        self.b_mag_entry.grid(row=7, column=1, sticky=tk.EW, padx=5, pady=2)
        
        ttk.Label(input_frame, text="Magnitud V:").grid(row=8, column=0, sticky=tk.W)
        self.v_mag_entry = ttk.Entry(input_frame)
        self.v_mag_entry.grid(row=8, column=1, sticky=tk.EW, padx=5, pady=2)
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Añadir Estrella", command=self.add_star).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Calcular Resultados", command=self.submit_data).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_form).pack(side=tk.RIGHT, padx=5)
        
        # Bind events para actualizar Δt automáticamente
        self.date1_entry.bind("<<DateEntrySelected>>", self.update_delta_time)
        self.date2_entry.bind("<<DateEntrySelected>>", self.update_delta_time)
    
    def update_delta_time(self, event=None):
        """Calcula Δt en años cuando se seleccionan fechas"""
        try:
            date1 = self.date1_entry.get_date()
            date2 = self.date2_entry.get_date()
            
            if date1 and date2:
                delta_days = (date2 - date1).days
                delta_years = delta_days / 365.25  # Considera años bisiestos
                self.delta_time_label.config(text=f"{delta_years:.4f}")  # 4 decimales de precisión
            else:
                self.delta_time_label.config(text="0.0000")
        except Exception as e:
            print(f"Error calculando Δt: {e}")
            self.delta_time_label.config(text="0.0000")
    
    def add_star(self):
        """Añade los datos de la estrella actual a la lista"""
        try:
            # Validar y calcular Δt primero
            delta_time = float(self.delta_time_label.cget("text"))
            if delta_time <= 0:
                raise ValueError("Δt debe ser positivo (la segunda fecha debe ser posterior)")
            
            star_data = {
                'name': self.name_entry.get(),
                'angular_displacement': float(self.angular_displacement_entry.get()),
                'date1': self.date1_entry.get_date(),
                'date2': self.date2_entry.get_date(),
                'delta_time': delta_time,  # Usamos el valor ya calculado y validado
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
            messagebox.showinfo("Éxito", "Estrella añadida correctamente")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def submit_data(self):
        """Envía todos los datos para procesamiento"""
        if not self.stars_data:
            messagebox.showwarning("Advertencia", "No hay datos de estrellas para procesar")
            return
        
        self.on_submit(self.stars_data)
    
    def clear_form(self):
        """Limpia el formulario"""
        self.name_entry.delete(0, tk.END)
        self.angular_displacement_entry.delete(0, tk.END)
        self.date1_entry.set_date(datetime.now())
        self.date2_entry.set_date(datetime.now())
        self.parallax_entry.delete(0, tk.END)
        self.vr_entry.delete(0, tk.END)
        self.b_mag_entry.delete(0, tk.END)
        self.v_mag_entry.delete(0, tk.END)
        self.update_delta_time()  # Actualiza Δt después de limpiar# -*- coding: utf-8 -*-

