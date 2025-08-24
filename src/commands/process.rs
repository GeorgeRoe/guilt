use crate::SomeError;
use crate::carbon_intensity_api::CarbonIntensityAggregator;
use crate::ip_info::fetch_ip_info;
use crate::models::ProcessedJob;
use crate::repositories::json::JsonUserDataRepository;
use crate::repositories::{ProcessedJobsRepository, UnprocessedJobsRepository, UserDataRepository};
use crate::slurm::accounting::{EndTime, StartTime, get_jobs_by_id};
use crate::users::get_current_user;
use std::collections::HashMap;

pub async fn run() -> Result<(), SomeError> {
    let current_user = get_current_user()?;

    let mut user_data_repo = JsonUserDataRepository::new(current_user)?;

    let unprocessed_jobs = user_data_repo.get_all_unprocessed_jobs()?;

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
        if let Some(sacct_result) = sacct_results.get(&unprocessed_job.job_id) {
            if let (StartTime::Started(start_time), EndTime::Finished(end_time), Some(cores_used)) = (
                sacct_result.start_time,
                sacct_result.end_time,
                sacct_result.resources.cpu,
            ) {
                let tdp_per_core = unprocessed_job.cpu_profile.tdp as f64
                    / unprocessed_job.cpu_profile.cores as f64;
                let duration = end_time - start_time;
                let hours = duration.num_seconds() as f64 / 3600.0;
                let energy = (tdp_per_core * cores_used as f64 * hours) / 1000.0;

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
                    start_time: start_time.clone(),
                    end_time: end_time.clone(),
                    cpu_profile: unprocessed_job.cpu_profile.clone(),
                    energy: energy,
                    emissions: emissions,
                    generation_mix: aggregator
                        .get_average_generation_mix(start_time, end_time)
                        .await?,
                };

                user_data_repo.upsert_processed_job(&processed_job)?;
                user_data_repo.delete_unprocessed_job(&processed_job.job_id)?;
            }
        }
    }

    user_data_repo.commit()?;

    Ok(())
}
