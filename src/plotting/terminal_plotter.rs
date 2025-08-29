use super::Plotter;
use colored::Colorize;
use std::collections::HashMap;
use terminal_size::{Width, terminal_size};

pub struct TerminalPlotter;

impl TerminalPlotter {
    fn plot_map(&self, map: &HashMap<String, f64>) {
        static SPLIT: &str = " | ";

        let longest_key_length = map.keys().map(|key| key.len()).max().unwrap_or(0);

        let size = terminal_size();
        let terminal_width = size
            .map_or(80, |(Width(w), _)| w as usize)
            .saturating_sub(2);

        let max_bar_width = terminal_width - longest_key_length - SPLIT.len() - 6;
        let max_value = map.values().cloned().fold(0.0, f64::max);

        for (key, value) in map.iter() {
            let bar_length = ((value / max_value) * max_bar_width as f64).round() as usize;
            let bar = "█".repeat(bar_length);
            let padding = " ".repeat(longest_key_length - key.len());

            println!("{}{}{}{} {:.2}", key, padding, SPLIT, bar.blue(), value);
        }
    }
}

impl Plotter for TerminalPlotter {
    fn draw_generation_mix(&self, generation_mix: HashMap<String, f64>) -> anyhow::Result<()> {
        println!("Generation Mix:");
        println!("-----------------");
        self.plot_map(&generation_mix);
        Ok(())
    }

    fn draw_intensity_forecast(
        &self,
        intensity_forecast: Vec<crate::carbon_intensity_api::CarbonIntensityTimeSegment>,
    ) -> anyhow::Result<()> {
        println!("Intensity Forecast:");
        println!("---------------------");
        self.plot_map(
            &intensity_forecast
                .iter()
                .map(|segment| {
                    (
                        segment.from.format("%H:%M").to_string(),
                        segment.intensity as f64,
                    )
                })
                .collect::<HashMap<_, _>>(),
        );
        Ok(())
    }
}
