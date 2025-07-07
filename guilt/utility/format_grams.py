def _truncate(value: float, decimals: int = 2) -> float:
  factor = 10 ** decimals
  return int(value * factor) / factor

def format_grams(grams: float) -> str:
  if grams < 1:
    return f"{grams:.2f} grams"
  elif grams < 1000:
    unit = "gram" if round(grams) == 1 else "grams"
    return f"{grams:.0f} {unit}"
  elif grams < 1_000_000:
    kilograms = grams / 1000
    kilograms_truncated = _truncate(kilograms)
    unit = "kilogram" if kilograms_truncated == 1 else "kilograms"
    return f"{kilograms_truncated:.2f} {unit}"
  else:
    tonnes = grams / 1_000_000
    tonnes_truncated = _truncate(tonnes)
    unit = "tonne" if tonnes_truncated == 1 else "tonnes"
    return f"{tonnes_truncated:.2f} {unit}"