use crate::guilt_directory::GuiltDirectoryManager;
use crate::models::{CpuProfileResolutionData, UnprocessedJob};
use crate::slurm::accounting::{EndTime, get_all_historical_jobs_for_user};
use crate::users::get_current_user;

pub fn run() -> anyhow::Result<()> {
    let current_user = get_current_user()?;

    let jobs = get_all_historical_jobs_for_user(&current_user.name)?;

    let mut guilt_dir_manager = GuiltDirectoryManager::read_for_user(&current_user);

    let mut unfinished_jobs_count = 0;

    for job in jobs {
        match job.end_time {
            EndTime::Finished(_) => {
                let unprocessed_job = UnprocessedJob {
                    job_id: job.job_id,
                    cpu_profile_resolution_data: CpuProfileResolutionData::None
                };

                guilt_dir_manager.upsert_unprocessed_job(unprocessed_job)?;
            }
            EndTime::NotFinished => {
                unfinished_jobs_count += 1;
            }
        }
    }

    if unfinished_jobs_count > 0 {
        println!(
            "There are {} unfinished jobs yet to be backfilled.",
            unfinished_jobs_count
        );
    } else {
        println!("All jobs have been processed.");
    }

    guilt_dir_manager.write()?;

    Ok(())
}
