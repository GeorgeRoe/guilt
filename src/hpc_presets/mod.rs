mod types;
pub use types::HpcPreset;

mod scarf;
pub use scarf::ScarfPreset;

mod isambard_3_grace;
pub use isambard_3_grace::Isambard3GracePreset;

mod archer2;
pub use archer2::Archer2Preset;

mod get;
pub use get::{get_all_hpc_presets, get_current_hpc_preset};
