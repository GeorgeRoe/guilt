mod cli;
mod commands;

pub mod carbon_intensity_api;
pub mod guilt_dir;
pub mod ip_info;
pub mod models;
pub mod plotting;
pub mod repositories;
pub mod safe_command;
pub mod script_directives;
pub mod slurm;
pub mod structured_json;
pub mod users;

mod parse_duration_string;
pub use parse_duration_string::parse_duration_string;

use clap::Parser;
use cli::{Cli, Commands};

pub type SomeError = Box<dyn std::error::Error>;

#[tokio::main]
async fn main() -> Result<(), SomeError> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Backfill => commands::backfill::run(),
        Commands::Batch { job } => commands::batch::run(job).await,
        Commands::Forecast => commands::forecast::run().await,
        Commands::Friends => commands::friends::run(),
        Commands::Process => commands::process::run().await,
        Commands::Report => commands::report::run(),
        Commands::Setup => commands::setup::run(),
        Commands::Teardown => commands::teardown::run(),
    }?;

    Ok(())
}
