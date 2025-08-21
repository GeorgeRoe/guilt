use crate::SomeError;
use crate::carbon_intensity_api::CarbonIntensityAggregator;
use crate::ip_info::fetch_ip_info;
use chrono::{DateTime, Duration, Utc};
use crate::plotting::get_plotter;

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

    let generation_mix = aggregator.get_average_generation_mix(now, finish).await?;
    let plotter = get_plotter();
    plotter.draw_generation_mix(generation_mix)?;

    Ok(())
}
