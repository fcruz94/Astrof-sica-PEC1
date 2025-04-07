# tables.py
import pandas as pd

def create_input_table(stars_data):
    """Crea tabla de datos de entrada"""
    data = []
    for star in stars_data:
        delta_time = (star['date2'] - star['date1']).days / 365.25
        
        data.append([
            star['name'],
            star['date1'].strftime('%Y-%m-%d'),
            star['date2'].strftime('%Y-%m-%d'),
            f"{delta_time:.2f}",
            star['vr'],
            star['B'],
            star['V']
        ])
    
    return pd.DataFrame(data, columns=[
        'Nombre', 'Fecha 1ª obs.', 'Fecha 2ª obs.', 
        'Δt (años)', 'Vr (km/s)', 'B', 'V'
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