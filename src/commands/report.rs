use crate::document::*;
use crate::guilt_directory::GuiltDirectoryManager;
use crate::plotting::ChartDefinition;
use crate::users::get_current_user;

pub fn run(renderer_type: &DocumentRendererType) -> anyhow::Result<()> {
    let current_user = get_current_user()?;

    let mut guilt_dir_manager = GuiltDirectoryManager::read_for_user(&current_user);

    let processed_jobs = guilt_dir_manager.get_all_processed_jobs()?;

    let mut document = Document {
        name: "GUILT Report".to_string(),
        ..Default::default()
    };

    document.elements.extend(vec![
        Element::Heading(HeadingLevel::H1, "GUILT Report".to_string()),
        Element::Heading(HeadingLevel::H2, "Introduction".to_string()),
        Element::Paragraph(format!(
            "This report provides an overview of the carbon emissions for the user '{}'. It includes an analysis of emissions, recommendations for reducing carbon footprint, and references for further reading.",
            current_user.name
        )),
        Element::Heading(HeadingLevel::H2, "Methodology & Assumptions".to_string()),
        Element::Paragraph("To calculate the carbon emissions associated with the users slurm jobs Green Usage Impact Logging Tool was used. GUILT makes the following assumptions:".to_string()),
        Element::Paragraph("Throughout any given job, the utilisation of the CPU is assumed to be 100%.".to_string()),
        Element::Paragraph("Carbon Intensity is gathered from an API in 30 minute chunks, thus all results are approximate.".to_string()),
        Element::Paragraph("The CPU power draw is estimated using the TDP of the CPU model. This is configured by the user and could be innacurate.".to_string()),
        Element::Heading(HeadingLevel::H2, "Results".to_string()),
    ]);

    if processed_jobs.is_empty() {
        document
            .elements
            .push(Element::Paragraph("No processed jobs found".to_string()));
    } else {
        let total_emissions = processed_jobs.iter().map(|job| job.emissions).sum::<f64>();
        document.elements.push(Element::Paragraph(format!(
            "You have emitted {:.3} grams of CO2 overall.",
            total_emissions
        )));

        let average_generation_mix = {
            let mut total_mix = std::collections::HashMap::new();
            let mut total_duration: f64 = 0.0;

            for job in &processed_jobs {
                let duration = job.end_time - job.start_time;

                for (source, percentage) in &job.generation_mix {
                    *total_mix.entry(source.clone()).or_insert(0.0) +=
                        percentage * duration.as_seconds_f64();
                }
                total_duration += duration.as_seconds_f64();
            }

            if total_duration > 0.0 {
                for value in total_mix.values_mut() {
                    *value /= total_duration;
                }
            }

            total_mix
        };

        document
            .elements
            .push(Element::Chart(ChartDefinition::GenerationMix(
                average_generation_mix,
            )));
    }

    document.elements.extend(vec![
        Element::Heading(HeadingLevel::H2, "Recommendations".to_string()),
        Element::Paragraph("To reduce your carbon footprint, consider the following recommendations:".to_string()),
        Element::Paragraph("1. Optimize Job Scheduling: Schedule jobs during periods of low carbon intensity.".to_string()),
        Element::Paragraph("2. Resource Allocation: Allocate resources based on job requirements to avoid over-provisioning.".to_string()),
        Element::Paragraph("3. Monitor and Adjust: Regularly monitor your jobs and adjust configurations to improve efficiency.".to_string()),
        Element::Heading(HeadingLevel::H2, "References".to_string()),
        Element::Paragraph("1. GUILT - https://www.github.com/SCD-Energy-Efficiency-Team/guilt".to_string()),
        Element::Paragraph("2. Carbon Intensity API - https://carbonintensity.org.uk/".to_string()),
        Element::Paragraph("3. Ip Info - https://ipinfo.io/".to_string()),
        Element::Paragraph("4. Inspired by the CATS project - https://github.com/GreenScheduler/cats".to_string())
    ]);

    renderer_type.get_renderer().render(&document)?;

    Ok(())
}
