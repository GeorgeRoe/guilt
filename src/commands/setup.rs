use crate::guilt_dir::guilt_dir_given_home;
use crate::hpc_presets::{HpcPreset, get_all_hpc_presets, get_current_hpc_preset};
use crate::repositories::json::JsonUserDataRepository;
use crate::repositories::{CpuProfilesRepository, UserDataRepository};
use crate::users::get_current_user;
use colored::Colorize;
use dialoguer::{Confirm, Select, theme::ColorfulTheme};
use std::collections::HashMap;
use std::fs;

fn choose_hpc_preset() -> Option<Box<dyn HpcPreset>> {
    let mut presets = get_all_hpc_presets()
        .into_iter()
        .map(|p| (p.get_name().to_string(), p))
        .collect::<HashMap<_, _>>();

    let mut preset_names: Vec<String> = vec!["Unknown".to_string()];
    preset_names.extend(presets.keys().cloned());

    let selection = Select::with_theme(&ColorfulTheme::default())
        .with_prompt("Select your HPC system")
        .items(preset_names.iter().map(|s| s.as_str()).collect::<Vec<_>>())
        .default(0)
        .interact()
        .ok()?;

    if selection == 0 {
        return None;
    }

    let name = &preset_names[selection];
    presets.remove(name)
}

pub fn run() -> anyhow::Result<()> {
    let current_user = get_current_user()?;
    let guilt_dir = guilt_dir_given_home(&current_user.home_dir);

    fs::create_dir_all(&guilt_dir)?;
    JsonUserDataRepository::setup(&current_user)?;

    let logo = r#"
 .d8888b.  888     888 8888888 888      88888888888 
d88P  Y88b 888     888   888   888          888     
888    888 888     888   888   888          888     
888        888     888   888   888          888     
888  88888 888     888   888   888          888     
888    888 888     888   888   888          888     
Y88b  d88P Y88b. .d88P   888   888          888     
 "Y8888P88  "Y88888P"  8888888 88888888     888
 
         Green Usage Impact Logging Tool
"#;

    println!("{}", logo.red());

    println!(
        "Welcome to GUILT! A directory has been created for your data at: {}",
        guilt_dir.display().to_string().green()
    );

    let hpc_preset = match get_current_hpc_preset() {
        Some(preset) => {
            println!("{} {}", "Detected HPC:".green(), preset.get_name());
            match Confirm::new()
                .with_prompt(format!(
                    "Do you want to use the preset for {}?",
                    preset.get_name()
                ))
                .default(true)
                .interact()
                .unwrap_or(false)
            {
                true => Some(preset),
                false => choose_hpc_preset(),
            }
        }
        None => {
            println!(
                "{}",
                "GUILT could not automatically detect the HPC you are using.".yellow()
            );
            choose_hpc_preset()
        }
    };

    if let Some(preset) = hpc_preset {
        let mut user_data_repo = JsonUserDataRepository::new(&current_user)?;
        println!("Setting up default CPU profiles. The following profiles will be added:");
        for profile in preset.get_cpu_profiles() {
            println!("{}", profile.name);
            user_data_repo.upsert_cpu_profile(&profile)?;
        }
        user_data_repo.commit()?;
    }

    println!(
        "{}",
        "Setup complete! You can now start using GUILT.".green()
    );

    Ok(())
}
