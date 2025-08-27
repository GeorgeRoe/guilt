use crate::users::User;
use std::path::{Path, PathBuf};

pub fn guilt_dir_given_home(home: &Path) -> PathBuf {
    home.join(".guilt")
}

pub fn has_guilt_dir(user: &User) -> bool {
    let guilt_dir = guilt_dir_given_home(&user.home_dir);
    guilt_dir.exists()
}
