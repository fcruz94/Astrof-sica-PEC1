# -*- coding: utf-8 -*-

from astroquery.simbad import Simbad

# Crear una instancia personalizada
custom_simbad = Simbad()
custom_simbad.add_votable_fields("rvz_radvel", "plx_value", "B", "V")

# Consultar una estrella
result = custom_simbad.query_object("HD 103095")

# Mostrar resultados
#print(result)
#print(result['MAIN_ID'][0])         # Nombre del objeto
print(result['plx_value'][0])       # Paralaje en mas
print(result['rvz_radvel'][0])      # Velocidad radial en km/s
print(result['B'][0])          # Magnitud B
print(result['V'][0])          # Magnitud V
