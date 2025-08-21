use std::collections::HashMap;
use crate::SomeError;

pub trait Plotter {
    fn draw_generation_mix(&self, generation_mix: HashMap<String, f64>) -> Result<(), SomeError>;
}