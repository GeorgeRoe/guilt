use crate::repositories::json::JsonUserDataRepository;
use crate::repositories::{ProcessedJobsRepository, UserDataRepository};
use crate::users::get_current_user;
use colored::Colorize;

pub fn run() -> anyhow::Result<()> {
    let current_user = get_current_user()?;

    let user_data_repo = JsonUserDataRepository::new(&current_user)?;

    let processed_jobs = user_data_repo.get_all_processed_jobs()?;

    if processed_jobs.is_empty() {
        println!("{}", "No processed jobs found.".red());
    } else {
        let total_emissions = processed_jobs.iter().map(|job| job.emissions).sum::<f64>();
        println!("You have emitted {:.3} grams of CO2.", total_emissions);
    }

    Ok(())
}
