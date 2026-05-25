import numpy as np


def sinc_squared(value: np.ndarray) -> np.ndarray:
    result = np.ones_like(value)
    mask = np.abs(value) > 1e-12
    result[mask] = (np.sin(value[mask]) / value[mask]) ** 2
    return result


def interference_factor(alpha: np.ndarray, slit_count: int) -> np.ndarray:
    numerator = np.sin(slit_count * alpha)
    denominator = np.sin(alpha)

    result = np.empty_like(alpha)
    mask = np.abs(denominator) > 1e-12

    result[mask] = (numerator[mask] / denominator[mask]) ** 2
    result[~mask] = slit_count ** 2

    return result


def calculate_intensity(
    x: np.ndarray,
    slit_count: int,
    slit_width: float,
    slit_period: float,
    wavelength: float,
    screen_distance: float,
) -> np.ndarray:
    theta = np.arctan(x / screen_distance)

    beta = np.pi * slit_width * np.sin(theta) / wavelength
    alpha = np.pi * slit_period * np.sin(theta) / wavelength

    diffraction = sinc_squared(beta)
    interference = interference_factor(alpha, slit_count)

    intensity = diffraction * interference

    max_intensity = np.max(intensity)
    if max_intensity > 0:
        intensity = intensity / max_intensity

    return intensity