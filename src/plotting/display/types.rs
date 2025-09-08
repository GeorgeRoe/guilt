use super::ChartDefinition;

pub trait ChartDisplayer {
    fn display(&self, chart: &ChartDefinition) -> anyhow::Result<()>;
}