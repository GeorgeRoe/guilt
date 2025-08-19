use crate::SomeError;
use crate::models::{CpuProfile, UnprocessedJob};
use crate::repositories::json::JsonUserDataRepository;
use crate::repositories::{UnprocessedJobsRepository, UserDataRepository};
use crate::slurm::accounting::{EndTime, get_all_historical_jobs_for_user};
use crate::users::get_current_user;

pub fn run() -> Result<(), SomeError> {
    let current_user = get_current_user()?;

    let jobs = get_all_historical_jobs_for_user(&current_user.name)?;

    let mut user_data_repo = JsonUserDataRepository::new(current_user)?;

    let default_cpu_profile = CpuProfile {
        name: "Default".to_string(),
        cores: 1,
        tdp: 10.0,
    };

    let mut unfinished_jobs_count = 0;

    for job in jobs {
        match job.end_time {
            EndTime::Finished(_) => {
                let unprocessed_job = UnprocessedJob {
                    job_id: job.job_id,
                    cpu_profile: default_cpu_profile.clone(),
                };

                user_data_repo.upsert_unprocessed_job(&unprocessed_job)?;
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

    user_data_repo.commit()?;

    Ok(())
}
