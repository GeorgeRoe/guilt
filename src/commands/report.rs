use crate::repositories::json::JsonUserDataRepository;
use crate::repositories::{ProcessedJobsRepository, UserDataRepository};
use crate::users::get_current_user;
use crate::document::*;
use crate::plotting::ChartDefinition;

pub fn run(renderer: &Renderer) -> anyhow::Result<()> {
    let current_user = get_current_user()?;

    let user_data_repo = JsonUserDataRepository::new(&current_user)?;

    let processed_jobs = user_data_repo.get_all_processed_jobs()?;
    
    let mut document = Document::default();
    document.name = "GUILT Report".to_string();

    document.elements.push(Element::Heading(HeadingLevel::H1, "GUILT Report".to_string()));

    if processed_jobs.is_empty() {
        document.elements.push(Element::Paragraph("No processed jobs found.".to_string()));
    } else {
        let total_emissions = processed_jobs.iter().map(|job| job.emissions).sum::<f64>();
        document.elements.push(Element::Paragraph(format!("You have emitted {:.3} grams of CO2.", total_emissions)));
    }

    if let Some(first_job) = processed_jobs.first() {
        document.elements.push(Element::Chart(ChartDefinition::GenerationMix(first_job.generation_mix.clone())));
    }

    println!("Rendering report...");
    renderer.render(&document)?;

    Ok(())
}
