use std::process::Command;
use std::str;
use std::path::PathBuf;

pub mod types;

pub fn get_all_users() -> std::io::Result<Vec<types::User>> {
    let output = Command::new("getent")
        .arg("passwd")
        .output()?;

    if !output.status.success() {
        return Err(std::io::Error::new(
            std::io::ErrorKind::Other,
            format!("getent failed with status: {}", output.status)
        ))
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
            users.push(types::User { name, gecos, home_dir })
        }
    }

    Ok(users)
}