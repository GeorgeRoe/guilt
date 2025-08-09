mod cli;
mod commands;

pub mod ip_info;
pub mod users;
pub mod guilt_dir;

use cli::{Cli, Commands};
use clap::Parser;

#[tokio::main]
async fn main() {
    let cli = Cli::parse();

    let data = ip_info::fetch_ip_info().await.unwrap();
    println!("Your postcode is {}", data.postal);

    let result = match &cli.command {
        Commands::Backfill => commands::backfill::run(),
        Commands::Batch => commands::batch::run(),
        Commands::Forecast => commands::forecast::run(),
        Commands::Friends => commands::friends::run(),
        Commands::Process => commands::process::run(),
        Commands::Report => commands::report::run(),
        Commands::Setup => commands::setup::run(),
        Commands::Teardown => commands::teardown::run(),
    };

    if let Err(e) = result {
        eprintln!("Error: {}", e);
        std::process::exit(1);
    }
}
