use super::*;

pub fn get_all_hpc_presets() -> Vec<Box<dyn HpcPreset>> {
    vec![
        Box::new(ScarfPreset),
        Box::new(Isambard3GracePreset),
        Box::new(Isambard3MacsPreset),
        Box::new(IsambardAiPhase1Preset),
        Box::new(IsambardAiPhase2Preset),
        Box::new(Archer2Preset),
    ]
}

pub fn get_current_hpc_preset() -> Option<Box<dyn HpcPreset>> {
    get_all_hpc_presets()
        .into_iter()
        .find(|preset| preset.is_current())
}
