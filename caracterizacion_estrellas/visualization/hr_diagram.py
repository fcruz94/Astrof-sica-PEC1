import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from adjustText import adjust_text

def plot_hr_diagram(standard_stars, analyzed_stars, save_path= 'imagenes/hr_diagram_<fecha>.png'):
    """
    Genera el diagrama HR con línea para estrellas estándar y opción de guardado
    Args:
        standard_stars: Lista de tuplas (tipo_espectral, B-V, Mv)
        analyzed_stars: Lista de diccionarios con datos de estrellas analizadas
        save_path: Ruta opcional para guardar el gráfico (ej. 'resultados/diagrama_hr.png')
    Returns:
        fig: Figura de matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Preparar datos estrellas estándar
    bv_std = [star[1] for star in standard_stars]
    mv_std = [star[2] for star in standard_stars]
    types_std = [star[0] for star in standard_stars]
    
    # Dibujar línea de secuencia principal (ordenamos los puntos por B-V)
    sorted_indices = np.argsort(bv_std)
    bv_sorted = np.array(bv_std)[sorted_indices]
    mv_sorted = np.array(mv_std)[sorted_indices]
    ax.plot(bv_sorted, mv_sorted, 'b-', alpha=0.5, linewidth=2, label='Secuencia Principal')
    
    # Estrellas estándar (puntos azules)
    ax.scatter(bv_std, mv_std, c='blue', marker='o', s=100, edgecolors='black', label='Estrellas Estándar')
    
    # Etiquetas para estrellas estándar
    for i, txt in enumerate(types_std):
        ax.annotate(txt, (bv_std[i], mv_std[i]), textcoords="offset points",
                   xytext=(0,10), ha='center', fontsize=8, color='blue')
    
    # # Estrellas analizadas (puntos rojos)

    if analyzed_stars:
        bv_ana = [star['B-V'] for star in analyzed_stars]
        mv_ana = [star['Mv'] for star in analyzed_stars]
        names_ana = [star['Nombre'] for star in analyzed_stars]
    
        # Puntos de datos
        ax.scatter(
            bv_ana, mv_ana,
            c='red',
            marker='s',
            s=100,
            edgecolors='black',
            label='Estrellas Analizadas',
            zorder=3
        )
    
        # Lista para almacenar las anotaciones
    #     texts = []
    
    #     for x, y, name in zip(bv_ana, mv_ana, names_ana):
    #         text = ax.annotate(
    #             name,
    #             color='red',
    #             xy=(x, y),
    #             xytext=(x -0.5, y),  # posición inicial
    #             #textcoords='offset points',
    #             ha='center',
    #             va='center',
    #             #bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7),
    #             arrowprops=dict(
    #                 arrowstyle='->',
    #                 color='red',
    #                 lw=1.5,
    #                 alpha=1,
    #                 shrinkA=4,
    #                 shrinkB=4
    #             ),
    #             zorder=3
    #         )
    #         texts.append(text)

    # # Ajuste automático de las posiciones
    # adjust_text(
    #     texts,
    #     ax=ax,
    #     expand_points=(1.2, 1.4),
    #     expand_text=(1.2, 1.4),
    #     force_text=0.8,
    #     force_points=0.8,
    #    # arrowprops=dict(arrowstyle='-', color='gray', lw=1),
    #     zorder=3
    # )

    # if analyzed_stars:
    #      bv_ana = [star['B-V'] for star in analyzed_stars]
    #      mv_ana = [star['Mv'] for star in analyzed_stars]
    #      names_ana = [star['Nombre'] for star in analyzed_stars]
         
    #      # Puntos de datos (asegurando que estén en primer plano)
    #      ax.scatter(bv_ana, mv_ana, c='red', marker='s', s=100, 
    #                edgecolors='black', label='Estrellas Analizadas', zorder=3)
         
    #      # Etiquetas desplazadas
    #      for x, y, name in zip(bv_ana, mv_ana, names_ana):
    #          ax.annotate(
    #              name,
    #              c='red',
    #              xy=(x, y),
    #              xytext=(30, 12),
    #              textcoords='offset points',
    #              ha='center',
    #              va='center',
    #              bbox=dict(boxstyle='round,pad=0.3', border=0, facecolor='white', alpha=0.7),
    #              arrowprops=dict(             
    #                 arrowstyle='fancy',          
    #                 color='gray',              
    #                 lw=1,
    #                 alpha=1,
    #                 shrinkA=2,                 # Separación en el punto de origen
    #                 shrinkB=2                  # Pequeña separación en el texto (opcional)
    #             ),
    #              zorder=3
    #          )
    # if analyzed_stars:
    #     bv_ana = [star['B-V'] for star in analyzed_stars]
    #     mv_ana = [star['Mv'] for star in analyzed_stars]
    #     names_ana = [star['Nombre'] for star in analyzed_stars]
        
    #     ax.scatter(bv_ana, mv_ana, c='red', marker='s', s=100, edgecolors='black', label='Estrellas Analizadas')
    # for i, (x, y, name) in enumerate(zip(bv_ana, mv_ana, names_ana)):
    #     angle = 45 * (i % 8)  # 8 posiciones angulares diferentes
    #     offset = 15  # Pixeles de desplazamiento
    #     ax.annotate(name, 
    #                (x, y),
    #                xytext=(offset*np.cos(np.radians(angle)), 
    #                         offset*np.sin(np.radians(angle))),
    #                textcoords='offset points',
    #                ha='center',
    #                va='center',
    #                bbox=dict(facecolor='white', alpha=0.7),
    #                arrowprops=dict(arrowstyle='->'))
        
        # Lista para almacenar textos y ajustar posiciones
        # texts = []
        # star_points = []
        # for i, (x, y, name) in enumerate(zip(bv_ana, mv_ana, names_ana)):
        #     texts.append(ax.text(x, y, name, 
        #                        fontsize=10, 
        #                        color='red',
        #                        ha='center',
        #                        va='center',
        #                        bbox=dict(boxstyle='round,pad=0.3',  # Añade fondo blanco
        #                                facecolor='white',
        #                                edgecolor='none',
        #                                alpha=0.7)))
        #     # Añadir un punto "invisible" como referencia de colisión
        #     star_points.append(ax.plot(x, y, 'o',color='black', markersize=1, alpha=0, zorder=0)[0])
        
        # # Ajuste avanzado con parámetros optimizados
        # adjust_text(texts,
        #            objects=star_points,
        #            arrowprops=dict(arrowstyle='-',  # Flecha más sutil
        #                          color='gray',
        #                          lw=0.3,
        #                          alpha=1),
        #            expand_points=(2, 2),  # Mayor separación de los puntos
        #            only_move={'text': 'xy'},  # Mueve solo las etiquetas
        #            ensure_inside_axes=True,
        #            va='center',
        #            ha='center',
        #            expand_text=(1.2, 1.4),  # Separación adicional entre textos
        #            force_text=(1.8, 1.8),  # Mayor fuerza de repulsión
        #            force_points=(0.5, 0.5),  # Menor fuerza sobre los puntos
        #            lim=200,  # Límite de iteraciones
        #            precision=0.5,
        #            ax=ax)
        
        # texts = []
        # for i, (x, y, name) in enumerate(zip(bv_ana, mv_ana, names_ana)):
        #     texts.append(ax.text(x, y, name, 
        #                        fontsize=10, 
        #                        color='red',
        #                        ha='center',
        #                        va='center'))
        
        # # Ajuste automático para evitar superposiciones
        # adjust_text(texts, 
        #            arrowprops=dict(arrowstyle='->', color='gray', lw=0.5),
        #            expand_points=(2.2, 2.5),  # Ajusta estos valores según necesidad
        #            force_text=(1.5, 1.5),
        #            ax=ax)
        
        # for i, txt in enumerate(names_ana):
        #     ax.annotate(txt, (bv_ana[i], mv_ana[i]), textcoords="offset points",
        #                xytext=(0,-15), ha='center', fontsize=8, color='red')
    
    # Configuración del gráfico
    ax.invert_yaxis()
    ax.set_xlabel('Índice de Color (B-V)', fontsize=12)
    ax.set_ylabel('Magnitud Absoluta (Mv)', fontsize=12)
    ax.set_title('Diagrama Hertzsprung-Russell', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', fontsize=10)
    
    # Guardar el gráfico si se especifica una ruta
    if save_path:
        try:
            # Asegurarse que el directorio existe
            import os
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Guardar en alta resolución (300 dpi)
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Diagrama HR guardado en: {save_path}")
        except Exception as e:
            print(f"Error al guardar el gráfico: {str(e)}")
    
    return fig# -*- coding: utf-8 -*-

