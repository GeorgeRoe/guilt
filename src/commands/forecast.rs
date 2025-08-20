use crate::SomeError;
use crate::carbon_intensity_api::CarbonIntensityAggregator;
use crate::ip_info::fetch_ip_info;
use chrono::{DateTime, Duration, Utc};
use plotters::prelude::*;

pub async fn run() -> Result<(), SomeError> {
    let ip_info = fetch_ip_info().await?;
    let mut aggregator = CarbonIntensityAggregator::new(ip_info.postal);

    let duration = Duration::days(1);
    let now: DateTime<Utc> = Utc::now();
    let finish = now + duration;

    let forecast = aggregator.get_segments(now, finish).await?;
    if forecast.is_empty() {
        println!(
            "No forecast data available for the next {} day(s).",
            duration.num_days()
        );
        return Ok(());
    }

    println!("Forecast Summary over next {} day(s):", duration.num_days());

    if let Some(min_intensity) = forecast.iter().map(|s| s.intensity).min() {
        println!("  Minimum Intensity: {} gCO2eq/kWh", min_intensity);
    }

    if let Some(max_intensity) = forecast.iter().map(|s| s.intensity).max() {
        println!("  Maximum Intensity: {} gCO2eq/kWh", max_intensity);
    }

    let average_intensity = aggregator.get_average_intensity(now, finish).await?;
    println!("  Average Intensity: {:.3} gCO2eq/kWh", average_intensity);

    println!("");

    let data: Vec<(DateTime<Utc>, i32)> = forecast
        .into_iter()
        .map(|segment| (segment.from, segment.intensity))
        .collect();

    let root = BitMapBackend::new("barchart.png", (800, 500)).into_drawing_area();
    root.fill(&WHITE)?;

    let (min_time, max_time) = (
        data.first().unwrap().0,
        data.last().unwrap().0 + Duration::minutes(30)
    );

    let max_val = data.iter().map(|(_, intensity)| *intensity).max().unwrap_or(400);
    let min_val = data.iter().map(|(_, intensity)| *intensity).min().unwrap_or(0);
    let buffer = 20;

    let mut chart = ChartBuilder::on(&root)
        .caption("Carbon Intensity Forecast", ("sans-serif", 20))
        .margin(10)
        .x_label_area_size(40)
        .y_label_area_size(50)
        .build_cartesian_2d(min_time..max_time, (min_val - buffer)..(max_val + buffer))?;

    chart.configure_mesh()
        .x_labels(10)
        .x_label_formatter(&|dt| dt.format("%Y-%m-%d %H:%M %:z").to_string())
        .y_desc("Intensity (gCO2eq/kWh)")
        .draw()?;

    chart.draw_series(
        data.iter().map(|(time, intensity)| {
            let start = *time;
            let end = *time + Duration::minutes(30);
            Rectangle::new(
                [
                    (start, 0),
                    (end, *intensity)
                ],
                BLUE.filled()
            )
        }),
    )?;

    Ok(())
}
