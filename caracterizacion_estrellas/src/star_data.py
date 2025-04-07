
import numpy as np
# Estrellas estándar para construir la secuencia principal
# en el diagrama H-R
STANDARD_STARS = [
    # (Tipo espectral, B-V, Mv)
    ('O5', -0.35, -5.8),
    ('B0', -0.31, -4.1),
    ('B5', -0.16, -1.1),
    ('A0', 0.00, 0.7),
    ('A5', 0.13, 2.0),
    ('F0', 0.27, 2.6),
    ('F5', 0.42, 3.4),
    ('G0', 0.58, 4.4),
    ('G5', 0.70, 5.1),
    ('K0', 0.89, 5.9),
    ('K5', 1.18, 7.3),
    ('M0', 1.45, 9.0),
    ('M5', 1.63, 11.8),
    ('M8', 1.80, 16)
]

def calculate_proper_motion(angular_displacement, delta_time_years):
    """Calcula el movimiento propio en arcsec/año"""
    return angular_displacement / delta_time_years

def calculate_distance(parallax_arcsec):
    """Calcula la distancia en parsecs"""
    if parallax_arcsec <= 0:
        return float('inf')
    return 1 / parallax_arcsec

def calculate_spectral_index(B, V):
    """Calcula el índice espectral B-V"""
    return B - V

def calculate_absolute_magnitude(V, distance_pc):
    """Calcula la magnitud absoluta visual Mv"""
    return V - 5 * (np.log10(distance_pc) - 1)

def calculate_tangential_velocity(proper_motion_arcsec_year, distance_pc):
    """Calcula la velocidad tangencial en km/s"""
    # Sustituyo la ecuación 'corta' por el desarrollo completo
    proper_motion_rad_year = proper_motion_arcsec_year * (np.pi / (180 * 3600))
    distance_km = distance_pc * 3.086e13
    return proper_motion_rad_year * distance_km / (365.25 * 24 * 3600)

def calculate_total_velocity(Vr, Vt):
    """Calcula la velocidad total en km/s"""
    return np.sqrt(Vr**2 + Vt**2)
