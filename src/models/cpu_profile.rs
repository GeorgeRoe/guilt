use serde::{Deserialize, Serialize};

#[derive(Deserialize, Serialize, Clone)]
pub struct CpuProfile {
    pub name: String,
    pub cores: u16,
    pub tdp: f32
}