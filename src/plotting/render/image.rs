use charts_rs::{
    BarChart, DEFAULT_FONT_DATA, LineChart, Series, get_or_try_init_fonts, svg_to_png,
};
use crate::plotting::{ChartDefinition, GenerationMixData, CarbonIntensityForecastData};
use ::image::DynamicImage;

pub struct Resolution {
    pub width: u32,
    pub height: u32,
}

fn prerender() -> anyhow::Result<()> {
    let _ = get_or_try_init_fonts(Some(vec![DEFAULT_FONT_DATA]));
    Ok(())
}

fn svg_string_to_image(svg: &str) -> anyhow::Result<DynamicImage> {
    let png_data = svg_to_png(svg)?;
    let img = image::load_from_memory(&png_data)?;
    Ok(img)
}

fn render_generation_mix(data: &GenerationMixData, resolution: &Resolution) -> anyhow::Result<DynamicImage> {
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
    chart.width = resolution.width as f32;
    chart.height = resolution.height as f32;

    svg_string_to_image(&chart.svg()?)
}

fn render_carbon_intensity_forecast(data: &CarbonIntensityForecastData, resolution: &Resolution) -> anyhow::Result<DynamicImage> {
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
    chart.width = resolution.width as f32;
    chart.height = resolution.height as f32;
    chart.y_axis_configs[0].axis_min = Some(
        (data
            .iter()
            .map(|s| s.intensity)
            .min()
            .unwrap_or(min_buffer)
            - min_buffer) as f32,
    );

    svg_string_to_image(&chart.svg()?)
}

pub fn render(chart: &ChartDefinition, resolution: &Resolution) -> anyhow::Result<DynamicImage> {
    match chart {
        ChartDefinition::GenerationMix(data) => render_generation_mix(data, resolution),
        ChartDefinition::CarbonIntensityForecast(data) => render_carbon_intensity_forecast(data, resolution),
    }
}