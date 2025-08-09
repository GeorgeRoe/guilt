mod cli;
mod commands;
mod ip_info;

use cli::{Cli, Commands};
use clap::Parser;

#[tokio::main]
async fn main() {
    let cli = Cli::parse();

    let data = ip_info::fetch_ip_info().await.unwrap();
    println!("Your postcode is {}", data.postal);

    match &cli.command {
        Commands::Backfill => commands::backfill::run(),
        Commands::Batch => commands::batch::run(),
        Commands::Forecast => commands::forecast::run(),
        Commands::Friends => commands::friends::run(),
        Commands::Process => commands::process::run(),
        Commands::Report => commands::report::run(),
        Commands::Setup => commands::setup::run(),
        Commands::Teardown => commands::teardown::run(),
    }
}
