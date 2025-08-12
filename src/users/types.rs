use std::path::PathBuf;

pub struct User {
    pub name: String,
    pub gecos: String,
    pub home_dir: PathBuf,
}
