import numpy as np


def wavelength_to_rgb(wavelength_nm: float) -> np.ndarray:
    wavelength = float(wavelength_nm)

    if 380 <= wavelength < 440:
        red = -(wavelength - 440) / (440 - 380)
        green = 0.0
        blue = 1.0
    elif 440 <= wavelength < 490:
        red = 0.0
        green = (wavelength - 440) / (490 - 440)
        blue = 1.0
    elif 490 <= wavelength < 510:
        red = 0.0
        green = 1.0
        blue = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        red = (wavelength - 510) / (580 - 510)
        green = 1.0
        blue = 0.0
    elif 580 <= wavelength < 645:
        red = 1.0
        green = -(wavelength - 645) / (645 - 580)
        blue = 0.0
    elif 645 <= wavelength <= 750:
        red = 1.0
        green = 0.0
        blue = 0.0
    else:
        red = green = blue = 0.0

    if 380 <= wavelength < 420:
        factor = 0.3 + 0.7 * (wavelength - 380) / (420 - 380)
    elif 420 <= wavelength < 700:
        factor = 1.0
    elif 700 <= wavelength <= 750:
        factor = 0.3 + 0.7 * (750 - wavelength) / (750 - 700)
    else:
        factor = 0.0

    gamma = 0.8

    return np.array([
        (red * factor) ** gamma,
        (green * factor) ** gamma,
        (blue * factor) ** gamma,
    ])

def make_colored_pattern(
    intensity: np.ndarray,
    wavelength_nm: float,
    height: int = 80,
) -> np.ndarray:
    rgb = wavelength_to_rgb(wavelength_nm)
    return np.tile(intensity, (height, 1))[:, :, np.newaxis] * rgb