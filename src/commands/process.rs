use crate::carbon_intensity::CarbonIntensityAggregator;
use crate::guilt_directory::GuiltDirectoryManager;
use crate::ip_info::fetch_ip_info;
use crate::models::ProcessedJob;
use crate::slurm::accounting::{EndTime, StartTime, get_jobs_by_id};
use crate::users::get_current_user;
use std::collections::HashMap;

pub async fn run() -> anyhow::Result<()> {
    let current_user = get_current_user()?;

    let mut guilt_dir_manager = GuiltDirectoryManager::read_for_user(&current_user);

    let unprocessed_jobs = guilt_dir_manager.get_all_unprocessed_jobs()?;

    if unprocessed_jobs.is_empty() {
        println!("No jobs to be processed.");
        return Ok(());
    }

    let sacct_results = get_jobs_by_id(
        &unprocessed_jobs
            .iter()
            .map(|job| job.job_id.clone())
            .collect::<Vec<_>>(),
    )?
    .into_iter()
    .map(|result| (result.job_id.clone(), result))
    .collect::<HashMap<_, _>>();

    let ip_info = fetch_ip_info().await?;

    let mut aggregator = CarbonIntensityAggregator::new(ip_info.postal);

    for unprocessed_job in unprocessed_jobs {
        if let Some(sacct_result) = sacct_results.get(&unprocessed_job.job_id)
            && let (StartTime::Started(start_time), EndTime::Finished(end_time), Some(cores_used)) = (
                sacct_result.start_time,
                sacct_result.end_time,
                sacct_result.resources.cpu,
            )
        {
            let tdp_per_core =
                unprocessed_job.cpu_profile.tdp as f64 / unprocessed_job.cpu_profile.cores as f64;
            let duration = end_time - start_time;
            let hours = duration.num_seconds() as f64 / 3600.0;
            let energy = (tdp_per_core * cores_used * hours) / 1000.0;

            let intensity = aggregator
                .get_average_intensity(start_time, end_time)
                .await?;
            let emissions = energy * intensity;

            println!(
                "Processed job {}: {:.2} kWh, {:.2} gCO2",
                unprocessed_job.job_id, energy, emissions
            );

            let processed_job = ProcessedJob {
                job_id: unprocessed_job.job_id,
                start_time,
                end_time,
                cpu_profile: unprocessed_job.cpu_profile.clone(),
                energy,
                emissions,
                generation_mix: aggregator
                    .get_average_generation_mix(start_time, end_time)
                    .await?,
            };

            guilt_dir_manager.remove_unprocessed_job(&processed_job.job_id)?;
            guilt_dir_manager.upsert_processed_job(processed_job)?;
        }
    }

    guilt_dir_manager.write()?;

    Ok(())
}
