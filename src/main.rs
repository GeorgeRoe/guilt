mod cli;
mod commands;

pub mod carbon_intensity_api;
pub mod guilt_dir;
pub mod ip_info;
pub mod models;
pub mod repositories;
pub mod safe_command;
pub mod slurm;
pub mod structured_json;
pub mod users;

use clap::Parser;
use cli::{Cli, Commands};

pub type SomeError = Box<dyn std::error::Error>;

#[tokio::main]
async fn main() -> Result<(), SomeError> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Backfill => commands::backfill::run(),
        Commands::Batch => commands::batch::run(),
        Commands::Forecast => commands::forecast::run().await,
        Commands::Friends => commands::friends::run(),
        Commands::Process => commands::process::run(),
        Commands::Report => commands::report::run(),
        Commands::Setup => commands::setup::run(),
        Commands::Teardown => commands::teardown::run(),
    }?;

    Ok(())
}
