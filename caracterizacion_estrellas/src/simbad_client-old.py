from astroquery.simbad import Simbad
import numpy as np
import warnings
from astropy.utils.exceptions import AstropyWarning

def configure_simbad():
    """Configuración actualizada con campos válidos confirmados"""
    custom_simbad = Simbad()
    
    # Solo campos que sabemos que existen
    custom_simbad.add_votable_fields(
        'plx_value',    # Paralaje en mas
        'rvz_radvel',   # Velocidad radial en km/s
        'B',      # Magnitud B
        'V'       # Magnitud V
    )
    
    custom_simbad.TIMEOUT = 90
    return custom_simbad

def query_simbad(star_name):
    """Consulta robusta usando solo campos disponibles"""
    warnings.simplefilter('ignore', AstropyWarning)
    
    try:
        simbad = configure_simbad()
        result = simbad.query_object(star_name)
        
        if result is None or len(result) == 0:
            print(f"No se encontraron resultados para {star_name}")
            return None
            
        # Extracción segura de datos
        data = {
            'name': star_name,
            'radial_velocity_km_s': _safe_extract_float(result, 'RVZ_RADVEL'),
            'parallax_arcsec': _safe_extract_parallax(result),
            'mag_B': _safe_extract_float(result, 'FLUX_B'),
            'mag_V': _safe_extract_float(result, 'FLUX_V')
        }
        
        print(f"Datos SIMBAD para {star_name}: {data}")
        return data
        
    except Exception as e:
        print(f"Error consultando SIMBAD: {str(e)}")
        return None

def _safe_extract_float(result, field):
    """Extrae un campo numérico de manera segura"""
    if field not in result.colnames:
        return None
    value = result[field][0]
    return float(value) if value is not np.ma.masked else None

def _safe_extract_parallax(result):
    """Extrae y convierte la paralaje de mas a arcsec"""
    if 'PLX_VALUE' not in result.colnames:
        return None
    value = result['PLX_VALUE'][0]
    if value is np.ma.masked:
        return None
    return float(value) / 1000  # Convertir de mas a arcsec