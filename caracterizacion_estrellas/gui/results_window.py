# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.star_data import STANDARD_STARS
from visualization.hr_diagram import plot_hr_diagram
import pandas as pd
# Para exportación de tablas
from datetime import datetime
import os
from pathlib import Path

def create_input_table(stars_data):
    """Crea tabla de datos de entrada actualizada"""
    data = []
    for star in stars_data:
        data.append([
            star['name'],
            f"{star['angular_displacement']:.4f}",  # φ
            star['date1'].strftime('%Y-%m-%d'),
            star['date2'].strftime('%Y-%m-%d'),
            f"{star['delta_time']:.2f}",
            f"{star['parallax']:.4f}",  # π
            f"{star['vr']:.2f}",
            f"{star['B']:.2f}",
            f"{star['V']:.2f}"
        ])
    
    return pd.DataFrame(data, columns=[
        'Nombre', 'φ (")', 'Fecha 1ª obs.', 'Fecha 2ª obs.', 
        'Δt (años)', 'π (")', 'Vr (km/s)', 'B', 'V'
    ])

def create_results_table(calculated_results):
    """Crea tabla de resultados calculados"""
    data = []
    for star in calculated_results:
        data.append([
            star['Nombre'],
            f"{star['Mov_propio']:.4f}",
            f"{star['Distancia']:.2f}",
            f"{star['B-V']:.2f}",
            f"{star['Mv']:.2f}",
            f"{star['Vt']:.2f}",
            f"{star['V_total']:.2f}"
        ])
    
    return pd.DataFrame(data, columns=[
        'Nombre', 'Mov. propio ("/año)', 'Distancia (pc)', 
        'Índice espectral (B-V)', 'Mv', 'Vt (km/s)', 'V total (km/s)'
    ])

class ResultsWindow:
    def __init__(self, root, stars_data, calculated_results):
        self.root = root
        self.root.title("Resultados del Análisis Estelar")
        self.stars_data = stars_data
        self.calculated_results = calculated_results
        
        self.setup_ui()
    
    # def setup_ui(self):
    #     notebook = ttk.Notebook(self.root)
    #     notebook.pack(fill=tk.BOTH, expand=True)
        
    #     # Pestaña de datos de entrada (actualizada)
    #     input_frame = ttk.Frame(notebook)
    #     self.create_table(input_frame, create_input_table(self.stars_data))
    #     notebook.add(input_frame, text="Datos de Entrada")
        
    #     # Pestaña de resultados
    #     results_frame = ttk.Frame(notebook)
    #     self.create_table(results_frame, create_results_table(self.calculated_results))
    #     notebook.add(results_frame, text="Resultados Calculados")
        
    #     # Pestaña del diagrama HR
    #     hr_frame = ttk.Frame(notebook)
    #     self.create_hr_diagram(hr_frame)
    #     notebook.add(hr_frame, text="Diagrama HR")
    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 1. Pestaña de datos de entrada
        input_frame = ttk.Frame(notebook)
        input_table = create_input_table(self.stars_data)  # Guardamos la tabla en una variable
        self.create_table(input_frame, input_table)
        notebook.add(input_frame, text="Datos de Entrada")
        
        # 2. Pestaña de resultados
        results_frame = ttk.Frame(notebook)
        results_table = create_results_table(self.calculated_results)  # Guardamos la tabla
        self.create_table(results_frame, results_table)
        notebook.add(results_frame, text="Resultados Calculados")
        
        # 3. Pestaña del diagrama HR
        hr_frame = ttk.Frame(notebook)
        self.create_hr_diagram(hr_frame)
        notebook.add(hr_frame, text="Diagrama HR")
        
        # 4. Añadimos frame para botones de exportación (debajo del notebook)
        export_frame = ttk.Frame(self.root)
        export_frame.pack(fill=tk.X, pady=10)
        
        # Botones de exportación con estilo consistente
        export_btn_style = ttk.Style()
        export_btn_style.configure('Export.TButton', foreground='blue')
        
        ttk.Button(export_frame, text="Exportar a CSV", 
                  command=lambda: self.export_tables(input_table, results_table, 'csv'),
                  style='Export.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="Exportar a Excel", 
                  command=lambda: self.export_tables(input_table, results_table, 'excel'),
                  style='Export.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(export_frame, text="Exportar a LaTeX", 
                  command=lambda: self.export_tables(input_table, results_table, 'latex'),
                  style='Export.TButton').pack(side=tk.LEFT, padx=5)
    def create_table(self, parent, dataframe):
        """Crea una tabla a partir de un DataFrame"""
        tree = ttk.Treeview(parent)
        
        # Columnas
        tree["columns"] = list(dataframe.columns)
        tree.column("#0", width=0, stretch=tk.NO)
        
        for col in dataframe.columns:
            tree.column(col, anchor=tk.W, width=100)
            tree.heading(col, text=col, anchor=tk.W)
        
        # Filas
        for i, row in dataframe.iterrows():
            tree.insert("", tk.END, values=list(row))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_hr_diagram(self, parent):
        """Crea el diagrama HR en el frame"""
        fig = plot_hr_diagram(STANDARD_STARS, self.calculated_results)
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Exportación tablas varios formatos
    def add_export_buttons(self, notebook, input_table, results_table):
        """Añade botones de exportación a cada pestaña"""
        # Frame para botones
        export_frame = ttk.Frame(notebook)
        export_frame.pack(fill=tk.X, pady=5)
        
        # Botones para exportar
        ttk.Button(export_frame, text="Exportar Tablas a CSV", 
                  command=lambda: self.export_tables(input_table, results_table, 'csv')).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Exportar a LaTeX", 
                  command=lambda: self.export_tables(input_table, results_table, 'latex')).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Exportar a Excel", 
                  command=lambda: self.export_tables(input_table, results_table, 'excel')).pack(side=tk.LEFT, padx=5)
    
    def export_tables(self, input_table, results_table, format_type):
        """Exporta ambas tablas al formato especificado"""
        try:
            # Crear directorio 'export' si no existe
            export_dir = Path(__file__).parent.parent / "export"
            export_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format_type == 'csv':
                input_table.to_csv(export_dir / f"datos_entrada_{timestamp}.csv", index=False, encoding='utf-8')
                results_table.to_csv(export_dir / f"resultados_{timestamp}.csv", index=False, encoding='utf-8')
                messagebox.showinfo("Éxito", f"Tablas exportadas a CSV en:\n{export_dir}")
                
            elif format_type == 'latex':
                with open(export_dir / f"tablas_{timestamp}.tex", 'w', encoding='utf-8') as f:
                    f.write("% Tabla de Datos de Entrada\n")
                    f.write(input_table.to_latex(index=False, escape=False))
                    f.write("\n\n% Tabla de Resultados\n")
                    f.write(results_table.to_latex(index=False, escape=False))
                messagebox.showinfo("Éxito", f"Tablas exportadas a LaTeX en:\n{export_dir}")
                
            elif format_type == 'excel':
                with pd.ExcelWriter(export_dir / f"resultados_{timestamp}.xlsx") as writer:
                    input_table.to_excel(writer, sheet_name='Datos Entrada', index=False)
                    results_table.to_excel(writer, sheet_name='Resultados', index=False)
                messagebox.showinfo("Éxito", f"Tablas exportadas a Excel en:\n{export_dir}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron exportar las tablas:\n{str(e)}")