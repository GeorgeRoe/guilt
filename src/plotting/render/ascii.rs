use super::{CarbonIntensityForecastData, ChartDefinition, GenerationMixData};
use colored::Colorize;
use std::collections::HashMap;
use terminal_size::{Width, terminal_size};

fn plot_map(map: &HashMap<String, f64>) {
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

pub fn render_generation_mix(data: &GenerationMixData) {
    println!("Generation Mix:");
    println!("-----------------");
    plot_map(data);
}

pub fn render_carbon_intensity_forecast(data: &CarbonIntensityForecastData) {
    println!("Intensity Forecast:");
    println!("---------------------");
    plot_map(
        &data
            .iter()
            .map(|segment| {
                (
                    segment.from.format("%H:%M").to_string(),
                    segment.intensity as f64,
                )
            })
            .collect::<HashMap<_, _>>(),
    );
}

pub fn render(chart: &ChartDefinition) {
    match chart {
        ChartDefinition::GenerationMix(data) => render_generation_mix(data),
        ChartDefinition::CarbonIntensityForecast(data) => render_carbon_intensity_forecast(data),
    }
}
