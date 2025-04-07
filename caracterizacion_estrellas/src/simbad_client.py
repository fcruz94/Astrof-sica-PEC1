from astroquery.simbad import Simbad
import numpy as np
import warnings
from astropy.utils.exceptions import AstropyWarning

def configure_simbad():
    """Configuración optimizada para obtener todos los datos necesarios"""
    custom_simbad = Simbad()
    
    # Campos específicos que sabemos que funcionan
    custom_simbad.add_votable_fields(
        'rvz_radvel',  # Velocidad radial en km/s
        'plx_value',   # Paralaje en miliarcosegundos
        'B',     # Magnitud B
        'V'      # Magnitud V
    )
    
    # Ajustes adicionales para mejor recuperación de datos
    custom_simbad.TIMEOUT = 60
    custom_simbad.ROW_LIMIT = 1
    return custom_simbad

def query_simbad(star_name):
    """Consulta optimizada para SIMBAD"""
    warnings.simplefilter('ignore', AstropyWarning)
    
    try:
        simbad = configure_simbad()
        result = simbad.query_object(star_name)
        
        if result is None or len(result) == 0:
            print(f"No se encontraron resultados para {star_name}")
            return None
        
        # Extracción robusta de datos
        data = {
            'name': star_name,
            'radial_velocity_km_s': _safe_extract(result, 'rvz_radvel'),
            'parallax_arcsec': _safe_extract_parallax(result),
            'mag_B': _safe_extract(result, 'B'),
            'mag_V': _safe_extract(result, 'V')
        }
        
        # Depuración: Mostrar los datos crudos obtenidos
        # print("\nDatos crudos de SIMBAD:")
        # print(result['main_id'][0])         # Nombre del objeto
        # print(result['plx_value'][0])       # Paralaje en mas
        # print(result['rvz_radvel'][0])      # Velocidad radial en km/s
        # print(result['B'][0])          # Magnitud B
        # print(result['V'][0])          # Magnitud V
        print(data['name'])
        print(data['radial_velocity_km_s'])
        print(data['parallax_arcsec'])
        print(data['mag_B'])
        print(data['mag_V'])
        return data
        
    except Exception as e:
        print(f"Error consultando SIMBAD: {str(e)}")
        return None

def _safe_extract(result, field):
    """Extrae un campo de manera segura"""
    if field not in result.colnames:
        return None
    value = result[field][0]
    return float(value) if value is not np.ma.masked else None

def _safe_extract_parallax(result):
    """Extrae y convierte la paralaje de mas a arcsec"""
    if 'plx_value' not in result.colnames:
        return None
    value = result['plx_value'][0]
    if value is np.ma.masked:
        return None
    return float(value) / 1000  # Convertir de mas a arcsec# -*- coding: utf-8 -*-

