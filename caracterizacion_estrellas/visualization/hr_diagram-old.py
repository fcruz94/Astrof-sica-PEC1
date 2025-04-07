# hr_diagram.py
import matplotlib.pyplot as plt
import numpy as np

def plot_hr_diagram(standard_stars, analyzed_stars):
    """Genera el diagrama HR"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Estrellas estándar
    bv_std = [star[1] for star in standard_stars]
    mv_std = [star[2] for star in standard_stars]
    types_std = [star[0] for star in standard_stars]
    
    ax.scatter(bv_std, mv_std, c='blue', label='Secuencia Principal', marker='o')
    for i, txt in enumerate(types_std):
        ax.annotate(txt, (bv_std[i], mv_std[i]), textcoords="offset points", 
                   xytext=(0,5), ha='center', fontsize=8)
    
    # Estrellas analizadas
    if analyzed_stars:
        bv_ana = [star['B-V'] for star in analyzed_stars]
        mv_ana = [star['Mv'] for star in analyzed_stars]
        names_ana = [star['Nombre'] for star in analyzed_stars]
        
        ax.scatter(bv_ana, mv_ana, c='red', label='Estrellas Analizadas', marker='s')
        for i, txt in enumerate(names_ana):
            ax.annotate(txt, (bv_ana[i], mv_ana[i]), textcoords="offset points", 
                       xytext=(0,-10), ha='center', fontsize=8)
    
    ax.invert_yaxis()
    ax.set_xlabel('Índice de Color (B-V)')
    ax.set_ylabel('Magnitud Absoluta (Mv)')
    ax.set_title('Diagrama Hertzsprung-Russell')
    ax.grid(True)
    ax.legend()
    
    return fig