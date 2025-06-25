def format_duration(seconds: float) -> str:
  seconds = int(seconds)
  periods = [
    ('day', 86400),
    ('hour', 3600),
    ('minute', 60),
    ('second', 1),
  ]

  parts: list[str] = []
  for name, count in periods:
    value = seconds // count
    if value:
      seconds -= value * count
      parts.append(f"{value} {name}{'s' if value != 1 else ''}")

  return ', '.join(parts) or '0 seconds'