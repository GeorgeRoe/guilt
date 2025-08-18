use crate::SomeError;
use crate::slurm::accounting::get_all_historical_jobs_for_user;
use crate::users::get_current_user;

pub fn run() -> Result<(), SomeError> {
    let current_user = get_current_user()?;

    let jobs = get_all_historical_jobs_for_user(&current_user.name)?;

    for job in jobs {
        println!("Job ID: {}", job.job_id);
        println!("Start Time: {:}", job.start_time);
        println!("End Time: {:}", job.end_time);
        println!("Resources: {:?}", job.resources);
        println!();
    }

    Ok(())
}
