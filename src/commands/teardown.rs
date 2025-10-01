use crate::users::get_current_user;
use crate::guilt_directory::GuiltDirectoryManager;
use colored::Colorize;
use std::io::{self, Write};

pub fn run() -> anyhow::Result<()> {
    let current_user = get_current_user()?;

    let guilt_dir_manager = GuiltDirectoryManager::read_for_user(&current_user);

    let confirmation = "I am guilty";

    println!("{}", "Feeling too guilty?".red());
    println!();
    println!(
        "This command will permanently delete your GUILT data by removing the directory at: {}",
        guilt_dir_manager.path().display().to_string().red()
    );
    print!("Confirm by typing the following: '{}': ", confirmation);
    io::stdout().flush().unwrap();

    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");

    let input = input.trim();

    if input != confirmation {
        println!(
            "{}",
            "Oh so you arent guilty? No data has been deleted, the polar bears will thank you!"
                .green()
        );
    } else {
        guilt_dir_manager.teardown()?;
        println!(
            "{}",
            "GUILT has been successfully removed from your system :(".red()
        );
    }

    Ok(())
}
