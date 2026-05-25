import numpy as np

from src.color import make_colored_pattern
from src.physics import calculate_intensity


def calculate_quasi_monochromatic_pattern(
    x: np.ndarray,
    slit_count: int,
    slit_width: float,
    slit_period: float,
    central_wavelength_nm: float,
    spectrum_width_nm: float,
    screen_distance: float,
    sample_count: int = 31,
) -> tuple[np.ndarray, np.ndarray]:
    if spectrum_width_nm <= 0:
        wavelength = central_wavelength_nm * 1e-9

        intensity = calculate_intensity(
            x=x,
            slit_count=slit_count,
            slit_width=slit_width,
            slit_period=slit_period,
            wavelength=wavelength,
            screen_distance=screen_distance,
        )

        image = make_colored_pattern(
            intensity=intensity,
            wavelength_nm=central_wavelength_nm,
        )

        return intensity, image

    start_wavelength = central_wavelength_nm - spectrum_width_nm / 2
    end_wavelength = central_wavelength_nm + spectrum_width_nm / 2

    wavelengths = np.linspace(
        start_wavelength,
        end_wavelength,
        sample_count,
    )

    total_intensity = np.zeros_like(x)
    total_image = np.zeros((80, len(x), 3))

    for wavelength_nm in wavelengths:
        wavelength = wavelength_nm * 1e-9

        intensity = calculate_intensity(
            x=x,
            slit_count=slit_count,
            slit_width=slit_width,
            slit_period=slit_period,
            wavelength=wavelength,
            screen_distance=screen_distance,
        )

        total_intensity += intensity
        total_image += make_colored_pattern(
            intensity=intensity,
            wavelength_nm=wavelength_nm,
        )

    total_intensity /= sample_count
    total_image /= sample_count

    max_value = np.max(total_image)
    if max_value > 0:
        total_image /= max_value

    return total_intensity, total_image