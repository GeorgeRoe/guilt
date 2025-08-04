from guilt.interfaces.services.plotting import PlottingServiceInterface

class PlottingContext:
  def __init__(self, plotting_service: PlottingServiceInterface) -> None:
    self._plotting_service = plotting_service

  def __enter__(self) -> PlottingServiceInterface:
    self._plotting_service.clear()
    return self._plotting_service

  def __exit__(self, exc_type, exc_value, traceback) -> None:
    self._plotting_service.show()
    self._plotting_service.clear()