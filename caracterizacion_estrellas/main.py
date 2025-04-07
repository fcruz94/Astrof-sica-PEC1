import tkinter as tk
from gui.main_window import StarInputForm
from gui.results_window import ResultsWindow
from src.star_data import *

def main():
    root = tk.Tk()
    
    def process_stars_data(stars_data):
        # Realizar cálculos
        calculated_results = []
        for star in stars_data:
            delta_time = (star['date2'] - star['date1']).days / 365.25
            
            # Cálculos
            mov_propio = calculate_proper_motion(star['angular_displacement'], delta_time)
            distancia = calculate_distance(star['parallax'])
            b_v = calculate_spectral_index(star['B'], star['V'])
            mv = calculate_absolute_magnitude(star['V'], distancia)
            vt = calculate_tangential_velocity(mov_propio, distancia)
            v_total = calculate_total_velocity(star['vr'], vt)
            
            calculated_results.append({
                'Nombre': star['name'],
                'Mov_propio': mov_propio,
                'Distancia': distancia,
                'B-V': b_v,
                'Mv': mv,
                'Vt': vt,
                'V_total': v_total
            })
        
        # Mostrar ventana de resultados
        results_window = tk.Toplevel(root)
        ResultsWindow(results_window, stars_data, calculated_results)
    
    # Mostrar formulario principal
    app = StarInputForm(root, process_stars_data)
    root.mainloop()

if __name__ == "__main__":
    main()