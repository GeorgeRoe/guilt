mod cli;
mod commands {
    pub mod backfill;
    pub mod batch;
    pub mod forecast;
    pub mod friends;
    pub mod process;
    pub mod report;
    pub mod setup;
    pub mod teardown;
}

use cli::{Cli, Commands};
use clap::Parser;

fn main() {
    let cli = Cli::parse();

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
