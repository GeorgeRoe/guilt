from guilt.types.json import Json
import json

class MapToJson:
  @staticmethod
  def from_directive_lines(lines: list[str], directive_comment: str) -> dict[str, Json]:
    directives: dict[str, Json] = {}
    for line in lines:
      if line.startswith(directive_comment):
        directive = line.replace(directive_comment, "").replace("--", "").split("=")
        key = directive[0].strip()
        value_str = directive[1].strip()

        value: Json = None
        if value_str:
          try:
            value = json.loads(value_str)
          except json.JSONDecodeError:
            value = value_str
        else:
          value = True
        
        directives[key] = value
        
    return directives