use super::Plotter;
use crate::SomeError;
use charts_rs::{
    BarChart, DEFAULT_FONT_DATA, LineChart, Series, get_or_try_init_fonts, svg_to_png,
};
use std::fs;
use std::fs::remove_file;
use std::process::Command;
use thiserror::Error;

static CHART_WIDTH: f32 = 800.0;
static CHART_HEIGHT: f32 = 600.0;

#[derive(Debug, Error)]
pub enum KittyPlottingError {
    #[error("Kitty Command Failed: {0}")]
    Display(String),

    #[error("File System Error: {0}")]
    FileSystem(#[from] std::io::Error),
}

pub struct KittyPlotter;

impl Default for KittyPlotter {
    fn default() -> Self {
        get_or_try_init_fonts(Some(vec![DEFAULT_FONT_DATA])).unwrap();
        Self
    }
}

impl KittyPlotter {
    fn display_png(&self, file_name: &str) -> Result<(), KittyPlottingError> {
        let status = Command::new("kitty")
            .args(["+kitten", "icat", file_name])
            .status();

        remove_file(file_name)?;

        match status {
            Ok(status) => {
                if status.success() {
                    Ok(())
                } else {
                    Err(KittyPlottingError::Display(format!("status {}", status)))
                }
            }
            Err(e) => Err(KittyPlottingError::Display(e.to_string())),
        }
    }

    fn display_svg(&self, svg_data: &str) -> Result<(), SomeError> {
        let png_data = svg_to_png(svg_data)?;
        fs::write("temp.png", &png_data)?;
        self.display_png("temp.png")?;

        Ok(())
    }
}

impl Plotter for KittyPlotter {
    fn draw_generation_mix(
        &self,
        generation_mix: std::collections::HashMap<String, f64>,
    ) -> Result<(), SomeError> {
        let series = Series::new(
            "Generation Mix".to_string(),
            generation_mix.values().cloned().map(|v| v as f32).collect(),
        );
        let labels: Vec<String> = generation_mix.keys().cloned().collect();

        let mut chart = BarChart::new(vec![series], labels);

        chart.y_axis_configs[0].axis_width = Some(55.0);
        chart.y_axis_configs[0].axis_formatter = Some("{c}%".to_string());
        chart.title_text = "Generation Mix".to_string();
        chart.legend_show = Some(false);
        chart.width = CHART_WIDTH;
        chart.height = CHART_HEIGHT;

        self.display_svg(&chart.svg()?)?;

        Ok(())
    }

    fn draw_intensity_forecast(
        &self,
        intensity_forecast: Vec<crate::carbon_intensity_api::CarbonIntensityTimeSegment>,
    ) -> Result<(), SomeError> {
        let series = Series::new(
            "Intensity Forecast".to_string(),
            intensity_forecast
                .iter()
                .map(|segment| segment.intensity as f32)
                .collect(),
        );
        let labels: Vec<String> = intensity_forecast
            .iter()
            .map(|segment| segment.from.format("%H:%M").to_string())
            .collect();

        let mut chart = LineChart::new(vec![series], labels);

        let min_buffer = 20;

        chart.y_axis_configs[0].axis_width = Some(110.0);
        chart.y_axis_configs[0].axis_formatter = Some("{c} gCO2/kWh".to_string());
        chart.title_text = "Intensity Forecast".to_string();
        chart.legend_show = Some(false);
        chart.width = CHART_WIDTH;
        chart.height = CHART_HEIGHT;
        chart.y_axis_configs[0].axis_min = Some(
            (intensity_forecast
                .iter()
                .map(|s| s.intensity)
                .min()
                .unwrap_or(min_buffer)
                - min_buffer) as f32,
        );

        self.display_svg(&chart.svg()?)?;

        Ok(())
    }
}
