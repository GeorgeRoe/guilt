use super::Plotter;
use crate::SomeError;
use terminal_size::{terminal_size, Width};
use colored::Colorize;

fn is_source_renewable(source: &str) -> bool {
    matches!(source, "solar" | "wind" | "hydro" | "biomass")
}

pub struct TerminalPlotter;

impl Plotter for TerminalPlotter {
    fn draw_generation_mix(&self, generation_mix: std::collections::HashMap<String, f64>) -> Result<(), SomeError> {
        static SPLIT: &str = " | ";

        println!("Generation Mix:");

        let longest_key_length = generation_mix.keys()
            .map(|key| key.len())
            .max()
            .unwrap_or(0);

        let size = terminal_size();
        let terminal_width = size.map_or(70, |(Width(w), _)| w as usize);

        let max_bar_width = terminal_width - longest_key_length - SPLIT.len() - 6;

        for (source, percentage) in generation_mix.iter() {
            let bar_length = ((percentage / 100.0) * max_bar_width as f64).round() as usize;
            let bar = "█".repeat(bar_length);
            let padding = " ".repeat(longest_key_length - source.len());

            println!("{}{}{}{} {:.2}", source, padding, SPLIT, if is_source_renewable(source) { bar.green() } else { bar.red() }, percentage);
        }

        Ok(())
    }
}