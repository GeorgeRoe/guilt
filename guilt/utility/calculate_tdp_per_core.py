from guilt.interfaces.models.cpu_profile import CpuProfileInterface

def calculate_tdp_per_core(cpu_profile: CpuProfileInterface) -> float:
  return cpu_profile.tdp / cpu_profile.cores if cpu_profile.cores > 0 else 0.0