use super::ChartDisplayer;
use super::render::image::render;
use super::ChartDefinition;
pub struct KittyChartDisplayer;
use thiserror::Error;
use std::fs::remove_file;
use std::process::Command;
use std::path::Path;

#[derive(Debug, Error)]
pub enum KittyPlottingError {
    #[error("Kitty Command Failed: {0}")]
    Display(String),

    #[error("File System Error: {0}")]
    FileSystem(#[from] std::io::Error),

    #[error("Path Conversion Error")]
    PathConversion,
}

impl KittyChartDisplayer {
    fn display_file(&self, path: &Path) -> Result<(), KittyPlottingError> {
        let status = Command::new("kitty")
            .args(["+kitten", "icat", path.to_str().ok_or_else(|| KittyPlottingError::PathConversion)?])
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
        let path_to_image = render(chart)?;

        self.display_file(path_to_image.as_path())?;

        Ok(())
    }
}