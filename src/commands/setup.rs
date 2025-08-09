use std::env;
use std::fs;
use std::io;
use colored::Colorize;

pub fn run() -> Result<(), Box<dyn std::error::Error>> {
    let mut home = env::home_dir().ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "Could not find home directory"))?;

    home.push(".guilt");

    fs::create_dir_all(&home)?;

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

    println!("Welcome to GUILT! A directory has been created for your data at: {}", home.display().to_string().green());

    Ok(())
}