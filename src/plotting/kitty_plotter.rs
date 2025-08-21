use super::Plotter;
use crate::SomeError;
use std::process::Command;
use std::fs::remove_file;
use thiserror::Error;
use charts_rs::{BarChart, Series, svg_to_png, get_or_try_init_fonts};
use std::fs;

#[derive(Debug, Error)]
pub enum KittyPlottingError {
    #[error("Kitty Command Failed: {0}")]
    Display(String),

    #[error("File System Error: {0}")]
    FileSystem(#[from] std::io::Error),
}

pub struct KittyPlotter;

impl KittyPlotter {
    fn display_png(&self, file_name: &str) -> Result<(), KittyPlottingError> {
        let status = Command::new("kitty")
            .args(&["+kitten", "icat", file_name])
            .status();

        remove_file(file_name)?;
        
        match status {
            Ok(status) => {
                if status.success() {
                    Ok(())
                } else {
                    Err(KittyPlottingError::Display(format!("status {}", status)))
                }

            },
            Err(e) => Err(KittyPlottingError::Display(e.to_string()))
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
    fn draw_generation_mix(&self, generation_mix: std::collections::HashMap<String, f64>) -> Result<(), SomeError> {
        let data = include_bytes!("../../assets/Roboto.ttf") as &[u8];
        get_or_try_init_fonts(Some(vec![data])).unwrap();

        let series = Series::new("Generation Mix".to_string(), generation_mix.values().cloned().map(|v| v as f32).collect());
        let labels: Vec<String> = generation_mix.keys().cloned().collect();

        let mut bar_chart = BarChart::new(vec![series], labels);

        bar_chart.y_axis_configs[0].axis_width = Some(55.0);
        bar_chart.title_text = "Generation Mix".to_string();
        bar_chart.legend_show = Some(false);
        // TODO: allow user to configure this setting later
        bar_chart.font_family = "Roboto".to_string();

        self.display_svg(&bar_chart.svg()?)?;

        Ok(())
    }
}