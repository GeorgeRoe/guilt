pub use super::*;

mod types;
pub use types::ChartDisplayer;

mod ascii;
pub use ascii::AsciiChartDisplayer;

mod kitty;
pub use kitty::KittyChartDisplayer;

pub fn get_chart_displayer() -> Box<dyn ChartDisplayer> {
    if std::env::var("TERM").unwrap_or_default().contains("kitty") {
        Box::new(KittyChartDisplayer)
    } else {
        Box::new(AsciiChartDisplayer)
    }
}