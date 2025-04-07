import tkinter as tk
from tkinter import ttk
from visualization.tables import create_input_table, create_results_table
from visualization.hr_diagram import plot_hr_diagram
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.star_data import STANDARD_STARS

class ResultsWindow:
    def __init__(self, root, stars_data, calculated_results):
        self.root = root
        self.root.title("Resultados del Análisis Estelar")
        
        self.stars_data = stars_data
        self.calculated_results = calculated_results
        
        self.setup_ui()
    
    def setup_ui(self):
        # Notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de datos de entrada
        input_frame = ttk.Frame(notebook)
        self.create_table(input_frame, create_input_table(self.stars_data))
        notebook.add(input_frame, text="Datos de Entrada")
        
        # Pestaña de resultados
        results_frame = ttk.Frame(notebook)
        self.create_table(results_frame, create_results_table(self.calculated_results))
        notebook.add(results_frame, text="Resultados Calculados")
        
        # Pestaña del diagrama HR
        hr_frame = ttk.Frame(notebook)
        self.create_hr_diagram(hr_frame)
        notebook.add(hr_frame, text="Diagrama HR")
    
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