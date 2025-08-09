use std::env;
use std::fs;
use std::io;

pub fn run() -> Result<(), Box<dyn std::error::Error>> {
    let mut home = env::home_dir().ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "Could not find home directory"))?;

    home.push(".guilt");

    fs::create_dir_all(&home)?;

    println!("Created '.guilt' directory at {}", home.display());

    Ok(())
}