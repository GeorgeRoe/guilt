use std::env;
use std::fs;
use std::io;
use colored::Colorize;
use crate::guilt_dir::guilt_dir_given_home;

use crate::SomeError;

pub fn run() -> Result<(), SomeError> {
    let home = env::home_dir().ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "Could not find home directory"))?;
    let guilt_dir = guilt_dir_given_home(&home);

    fs::create_dir_all(&guilt_dir)?;

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

    println!("Welcome to GUILT! A directory has been created for your data at: {}", guilt_dir.display().to_string().green());

    Ok(())
}