use crate::document::Renderer;
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "guilt")]
#[command(about = "GUILT: Green Usage Impact Logging Tool")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand, Clone)]
pub enum Commands {
    #[command(about = "Add all previous slurm jobs to GUILT's scope")]
    Backfill,

    #[command(about = "Submit a slurm job")]
    Batch {
        #[arg(value_name = "JOB_SCRIPT", help = "The slurm job script to submit")]
        job: String,
    },

    #[command(about = "Disply a carbon intensity forecast")]
    Forecast,

    #[command(about = "Display the other GUILT users on the system")]
    Friends,

    #[command(about = "Migrate GUILT configuration/data to the latest version")]
    Migrate,

    #[command(about = "Calculate the carbon impact of your jobs")]
    Process,

    #[command(about = "Display a report of your carbon impact")]
    Report {
        #[arg(long, value_enum, default_value_t = Renderer::Terminal)]
        format: Renderer,
    },

    #[command(about = "Setup GUILT for use")]
    Setup,

    #[command(about = "Remove GUILT's configuration and data")]
    Teardown,
}
