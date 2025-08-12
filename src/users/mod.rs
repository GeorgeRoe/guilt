use std::env;
use std::path::PathBuf;
use std::process::Command;
use std::str;

mod types;

pub use types::User;

pub fn get_all_users() -> std::io::Result<Vec<User>> {
    let output = Command::new("getent").arg("passwd").output()?;

    if !output.status.success() {
        return Err(std::io::Error::new(
            std::io::ErrorKind::Other,
            format!("getent failed with status: {}", output.status),
        ));
    }

    let stdout = str::from_utf8(&output.stdout)
        .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;

    let mut users = Vec::new();
    for line in stdout.lines() {
        let fields: Vec<&str> = line.splitn(7, ":").collect();
        if fields.len() >= 7 {
            let name = fields[0].to_string();
            let gecos = fields[4].to_string();
            let home_dir = PathBuf::from(fields[5]);
            users.push(User {
                name,
                gecos,
                home_dir,
            })
        }
    }

    Ok(users)
}

pub fn get_current_user() -> std::io::Result<User> {
    // Get the username from environment variables
    let username = env::var("USER").map_err(|_| {
        std::io::Error::new(
            std::io::ErrorKind::NotFound,
            "USER environment variable not set",
        )
    })?;

    // Call getent passwd for the specific user
    let output = Command::new("getent")
        .arg("passwd")
        .arg(&username)
        .output()?;

    if !output.status.success() {
        return Err(std::io::Error::new(
            std::io::ErrorKind::Other,
            format!("getent failed with status: {}", output.status),
        ));
    }

    let stdout = str::from_utf8(&output.stdout)
        .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;

    // Parse the single line output
    let fields: Vec<&str> = stdout.trim_end().splitn(7, ":").collect();
    if fields.len() < 7 {
        return Err(std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            "Malformed getent output",
        ));
    }

    let name = fields[0].to_string();
    let gecos = fields[4].to_string();
    let home_dir = PathBuf::from(fields[5]);

    Ok(User {
        name,
        gecos,
        home_dir,
    })
}
