def format_grams(grams: float) -> str:
  if grams < 1:
    return f"{grams:.2f} grams"
  elif grams < 1000:
    unit = "gram" if round(grams) == 1 else "grams"
    return f"{grams:.0f} {unit}"
  elif grams < 1_000_000:
    kilograms = grams / 1000
    unit = "kilogram" if round(kilograms, 2) == 1 else "kilograms"
    return f"{kilograms:.2f} {unit}"
  else:
    tonnes = grams / 1_000_000
    unit = "tonne" if round(tonnes, 2) == 1 else "tonnes"
    return f"{tonnes:.2f} {unit}"