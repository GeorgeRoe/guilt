use std::path::PathBuf;

pub fn guilt_dir_given_home(home: &PathBuf) -> PathBuf {
    let mut guilt_dir = home.clone();
    guilt_dir.push(".guilt");
    guilt_dir
}