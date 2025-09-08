use super::ChartDisplayer;
use super::render::image::{render, Resolution};
use super::ChartDefinition;
pub struct KittyChartDisplayer;
use thiserror::Error;
use std::fs::remove_file;
use std::process::Command;
use image::DynamicImage;

static RESOLUTION: Resolution = Resolution {
    width: 800,
    height: 600,
};

#[derive(Debug, Error)]
pub enum KittyPlottingError {
    #[error("Kitty Command Failed: {0}")]
    Display(String),

    #[error("File System Error: {0}")]
    FileSystem(#[from] std::io::Error),

    #[error("Image Processing Error: {0}")]
    ImageProcessing(#[from] image::ImageError),
}

impl KittyChartDisplayer {
    fn display_image(&self, img: &DynamicImage) -> Result<(), KittyPlottingError> {
        let path = "temp_chart.png";

        img.save(path)?;

        let status = Command::new("kitty")
            .args(["+kitten", "icat", path])
            .status();

        remove_file(path)?;

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
}

impl ChartDisplayer for KittyChartDisplayer {
    fn display(&self, chart: &ChartDefinition) -> anyhow::Result<()> {
        Ok(self.display_image(&render(chart, &RESOLUTION)?)?)
    }
}