use super::ChartDefinition;
use super::ChartDisplayer;
use super::render::ascii::render;

pub struct AsciiChartDisplayer;

impl ChartDisplayer for AsciiChartDisplayer {
    fn display(&self, chart: &ChartDefinition) -> anyhow::Result<()> {
        render(chart);
        Ok(())
    }
}
