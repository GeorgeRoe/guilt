use crate::carbon_intensity::{CarbonIntensityAggregator, api::ApiFetchCarbonIntensity};
use crate::guilt_directory::GuiltDirectoryManager;
use crate::ip_info::fetch_ip_info;
use crate::models::UnprocessedJob;
use crate::script_directives::{GuiltScriptDirectives, SlurmScriptDirectives};
use crate::slurm::batch;
use crate::users::get_current_user;
use chrono::{DateTime, Duration, Utc};
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum BatchCommandError {
    #[error("CPU profile '{0}' not found.")]
    CpuProfileNotFound(String),
}

fn resolve_path(path_str: &str) -> std::io::Result<PathBuf> {
    let path = Path::new(path_str);

    if path.is_absolute() {
        Ok(path.to_path_buf())
    } else {
        let cwd = env::current_dir()?;
        Ok(cwd.join(path))
    }
}

static SEARCH_RESOLUTION: i64 = 15;

pub async fn run(job: &str) -> anyhow::Result<()> {
    let path = resolve_path(job)?;

    let contents = fs::read_to_string(&path)?;

    let guilt_directives = GuiltScriptDirectives::from_file_contents(&contents)?;
    let slurm_directives = SlurmScriptDirectives::from_file_contents(&contents)?;

    let test_job = batch::test(job, None)?;

    let earliest_possible_start_time = test_job.start_time;
    let latest_forecast_time = Utc::now() + Duration::days(2) - Duration::minutes(30);

    let mut guilt_dir_manager = GuiltDirectoryManager::read_for_user(&get_current_user()?);
    let cpu_profile = guilt_dir_manager
        .get_cpu_profile(&guilt_directives.cpu_profile)?
        .ok_or(BatchCommandError::CpuProfileNotFound(
            guilt_directives.cpu_profile,
        ))?;

    let begin: Option<DateTime<Utc>> = if earliest_possible_start_time + slurm_directives.time
        > latest_forecast_time
    {
        println!(
            "Your job is extends into unforecasted carbon intensity data. No delays will be applied."
        );
        None
    } else {
        let tdp_kilowatts = (slurm_directives.tasks_per_node
            * slurm_directives.cpus_per_task
            * slurm_directives.nodes) as f64
            * (cpu_profile.tdp as f64 / cpu_profile.cores as f64)
            / 1000.0;

        let ip_info = fetch_ip_info().await?;
        let mut aggregator =
            CarbonIntensityAggregator::new(ApiFetchCarbonIntensity::new(ip_info.postal));

        // initialise the cache (make all requests at start, instead of many small requests later)
        aggregator
            .get_segments(earliest_possible_start_time, latest_forecast_time)
            .await?;

        let earliest_possible_intensity = aggregator
            .get_average_intensity(
                earliest_possible_start_time,
                earliest_possible_start_time + slurm_directives.time,
            )
            .await?;
        let earliest_possible_emissions = earliest_possible_intensity * tdp_kilowatts;

        let latest_possible_start_time = latest_forecast_time - slurm_directives.time;
        let start_times = (1..(latest_possible_start_time - earliest_possible_start_time)
            .num_minutes()
            / SEARCH_RESOLUTION)
            .map(|m| earliest_possible_start_time + Duration::minutes(m * SEARCH_RESOLUTION));
        let time_windows = start_times.map(|start| (start, start + slurm_directives.time));

        let mut intensities: Vec<(DateTime<Utc>, f64)> = Vec::new();
        for (start, end) in time_windows {
            let intensity = aggregator
                .get_average_intensity(start, end)
                .await
                .unwrap_or(f64::MAX);
            intensities.push((start, intensity));
        }
        intensities.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap_or(std::cmp::Ordering::Equal));

        let best_time = intensities.iter().find_map(|(start, intensity)| {
            if intensity > &earliest_possible_intensity {
                None
            } else {
                let emissions = tdp_kilowatts * intensity;

                let emissions_reduction = earliest_possible_emissions - emissions;
                let delay = *start - earliest_possible_start_time;
                let delay_seconds = delay.num_seconds().max(1) as f64;

                if emissions_reduction / delay_seconds > 0.001 {
                    Some((*start, emissions))
                } else {
                    None
                }
            }
        });

        match best_time {
            Some((start, emissions)) => {
                println!(
                    "If you had used 'sbatch', the job would have begun at {} and emitted {:.2} grams of CO2.",
                    earliest_possible_start_time.format("%Y-%m-%d %H:%M"),
                    earliest_possible_emissions
                );
                println!(
                    "By delaying the job to {}, it will emit {:.2} grams of CO2.",
                    start.format("%Y-%m-%d %H:%M"),
                    emissions
                );
                println!(
                    "You are saving {:.2} grams of CO2 by delaying the job.",
                    earliest_possible_emissions - emissions
                );

                Some(start)
            }
            None => {
                println!(
                    "Could not find a better time to run your job, no delays will be applied."
                );
                None
            }
        }
    };

    let local_begin = begin.map(|b| b.with_timezone(&chrono::Local));
    let naive_begin = local_begin.map(|b| b.naive_local());

    let job_id = batch::submit(job, naive_begin)?;
    println!("Submitted job {}.", job_id);

    let unprocessed_job = UnprocessedJob {
        job_id,
        cpu_profile,
    };

    guilt_dir_manager.upsert_unprocessed_job(unprocessed_job)?;
    guilt_dir_manager.write()?;

    Ok(())
}
