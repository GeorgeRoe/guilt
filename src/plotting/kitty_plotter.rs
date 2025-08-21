use super::Plotter;
use crate::SomeError;
use std::process::Command;
use std::fs::remove_file;
use thiserror::Error;
use charts_rs::{BarChart, Series};
use usvg::{fontdb::Database, Options, Tree};
use tiny_skia::{Pixmap, Transform};
use resvg::render;
use std::sync::Arc;

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
        let mut opt = Options::default();
        let mut db = Database::new();
        db.load_system_fonts();
        opt.fontdb = Arc::new(db);

        let tree = Tree::from_str(svg_data, &opt)?;

        let pixmap_size = tree.size().to_int_size();
        let mut pixmap = Pixmap::new(pixmap_size.width(), pixmap_size.height())
            .ok_or("Failed to create pixmap")?;

        render(&tree, Transform::default(), &mut pixmap.as_mut());

        pixmap.save_png("temp.svg")?;
        self.display_png("temp.svg")?;

        Ok(())
    }
}

impl Plotter for KittyPlotter {
    fn draw_generation_mix(&self, generation_mix: std::collections::HashMap<String, f64>) -> Result<(), SomeError> {
        let series = Series::new("Generation Mix".to_string(), generation_mix.values().cloned().map(|v| v as f32).collect());
        let labels: Vec<String> = generation_mix.keys().cloned().collect();

        let mut bar_chart = BarChart::new(vec![series], labels);

        bar_chart.y_axis_configs[0].axis_width = Some(55.0);
        bar_chart.title_text = "Generation Mix".to_string();
        bar_chart.legend_show = Some(false);
        // TODO: allow user to configure this setting later
        bar_chart.font_family = "DejaVu Sans".to_string();

        self.display_svg(&bar_chart.svg()?)?;

        Ok(())
    }
}