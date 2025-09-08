use super::ChartDisplayer;
use super::render::ascii::render;
use super::ChartDefinition;

pub struct AsciiChartDisplayer;

impl ChartDisplayer for AsciiChartDisplayer {
    fn display(&self, chart: &ChartDefinition) -> anyhow::Result<()> {
        Ok(render(chart))
    }
}