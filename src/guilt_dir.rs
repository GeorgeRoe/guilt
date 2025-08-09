use std::path::PathBuf;
use crate::users::User;

pub fn guilt_dir_given_home(home: &PathBuf) -> PathBuf {
    let mut guilt_dir = home.clone();
    guilt_dir.push(".guilt");
    guilt_dir
}

pub fn has_guilt_dir(user: &User) -> bool {
    let guilt_dir = guilt_dir_given_home(&user.home_dir);
    guilt_dir.exists()
}