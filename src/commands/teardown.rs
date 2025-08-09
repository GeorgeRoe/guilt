use std::io::{self, Write};
use colored::Colorize;
use std::env;
use std::fs;
use crate::guilt_dir::guilt_dir_given_home;

use crate::SomeError;

pub fn run() -> Result<(), SomeError> {
    let home = env::home_dir().ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "Could not find home directory"))?;
    let guilt_dir = guilt_dir_given_home(&home);

    let confirmation = "I am guilty";

    println!("{}", "Feeling too guilty?".red());
    println!("");
    println!("This command will permanently delete your GUILT data by removing the directory at: {}", guilt_dir.display().to_string().red());
    print!("Confirm by typing the following: '{}': ", confirmation);
    io::stdout().flush().unwrap();

    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Failed to read line");

    let input = input.trim();

    if input != confirmation {
        println!("{}", "Oh so you arent guilty? No data has been deleted, the polar bears will thank you!".green());
    } else {
        fs::remove_dir_all(&guilt_dir)?;
        println!("{}", "GUILT has been successfully removed from your system :(".red());
    }

    Ok(())
}