use super::Plotter;
use plotters::prelude::*;
use crate::SomeError;
use std::process::Command;
use std::fs::remove_file;
use thiserror::Error;

static TEMPORARY_FILE: &str = "plot.png";

fn is_source_renewable(source: &str) -> bool {
    matches!(source, "solar" | "wind" | "hydro" | "biomass")
}

#[derive(Debug, Error)]
pub enum KittyPlottingError {
    #[error("Kitty Command Failed: {0}")]
    Display(String),

    #[error("File System Error: {0}")]
    FileSystem(#[from] std::io::Error),
}

pub struct KittyPlotter;

impl KittyPlotter {
    fn display(&self) -> Result<(), KittyPlottingError> {
        let status = Command::new("kitty")
            .args(&["+kitten", "icat", TEMPORARY_FILE])
            .status();

        remove_file(TEMPORARY_FILE)?;
        
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
}

impl Plotter for KittyPlotter {
    fn draw_generation_mix(&self, generation_mix: std::collections::HashMap<String, f64>) -> Result<(), SomeError> {
        let root = BitMapBackend::new(TEMPORARY_FILE, (800, 600)).into_drawing_area();
        root.fill(&WHITE)?;
        
        let largest_percentage = generation_mix.values().cloned().fold(0.0, f64::max);

        let mut chart = ChartBuilder::on(&root)
            .caption("Generation Mix", ("sans-serif", 20))
            .margin(10)
            .x_label_area_size(40)
            .y_label_area_size(50)
            .build_cartesian_2d(0..generation_mix.len(), 0f64..(largest_percentage + 5.0))?;

        chart.configure_mesh()
            .x_labels(generation_mix.len())
            .x_label_formatter(&|x| {
                let i = *x as usize;
                generation_mix.keys().nth(i).unwrap_or(&"".to_string()).clone()
            })
            .x_desc("Source")
            .y_desc("Percentage")
            .draw()?;

        chart.draw_series(
            generation_mix.into_iter().enumerate().map(|(i, (source, percentage))| {
                Rectangle::new(
                    [(i, 0.0), ((i + 1), percentage)],
                    if is_source_renewable(&source) {
                        GREEN.filled()
                    } else {
                        RED.filled()
                    }
                )
            }),
        )?;

        root.present()?;

        self.display()?;

        Ok(())
    }
}