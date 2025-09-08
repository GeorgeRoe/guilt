use charts_rs::{
    BarChart, DEFAULT_FONT_DATA, LineChart, Series, get_or_try_init_fonts, svg_to_png,
};
use crate::plotting::{ChartDefinition, GenerationMixData, CarbonIntensityForecastData};
use std::path::PathBuf;
use std::fs;

static CHART_WIDTH: f32 = 800.0;
static CHART_HEIGHT: f32 = 600.0;

fn prerender() -> anyhow::Result<()> {
    let s = get_or_try_init_fonts(Some(vec![DEFAULT_FONT_DATA]));
    Ok(())
}

fn render_generation_mix(data: &GenerationMixData) -> anyhow::Result<PathBuf> {
    prerender()?;

    let series = Series::new(
        "Generation Mix".to_string(),
        data.values().cloned().map(|v| v as f32).collect(),
    );
    let labels: Vec<String> = data.keys().cloned().collect();

    let mut chart = BarChart::new(vec![series], labels);

    chart.y_axis_configs[0].axis_width = Some(55.0);
    chart.y_axis_configs[0].axis_formatter = Some("{c}%".to_string());
    chart.title_text = "Generation Mix".to_string();
    chart.legend_show = Some(false);
    chart.width = CHART_WIDTH;
    chart.height = CHART_HEIGHT;

    let svg = chart.svg()?;
    let png = svg_to_png(&svg)?;

    let output_path = PathBuf::from("generation_mix.png");

    fs::write(&output_path, &png)?;

    Ok(output_path)
}

fn render_carbon_intensity_forecast(data: &CarbonIntensityForecastData) -> anyhow::Result<PathBuf> {
    prerender()?;

    let series = Series::new(
        "Intensity Forecast".to_string(),
        data
            .iter()
            .map(|segment| segment.intensity as f32)
            .collect(),
    );
    let labels: Vec<String> = data
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
        (data
            .iter()
            .map(|s| s.intensity)
            .min()
            .unwrap_or(min_buffer)
            - min_buffer) as f32,
    );

    let svg = chart.svg()?;
    let png = svg_to_png(&svg)?;

    let output_path = PathBuf::from("carbon_intensity_forecast.png");

    fs::write(&output_path, &png)?;

    Ok(output_path)
}

pub fn render(chart: &ChartDefinition) -> anyhow::Result<PathBuf> {
    match chart {
        ChartDefinition::GenerationMix(data) => render_generation_mix(data),
        ChartDefinition::CarbonIntensityForecast(data) => render_carbon_intensity_forecast(data),
    }
}