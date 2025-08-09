use crate::users::{get_all_users, User};
use crate::guilt_dir::has_guilt_dir;
use colored::Colorize;

use crate::SomeError;

pub fn run() -> Result<(), SomeError> {
    let friends: Vec<User> = get_all_users()?.into_iter()
        .filter(|user| has_guilt_dir(user))
        .collect();

    if friends.is_empty() {
        println!("{}", "You are the only GUILT user on this system :(".red());
    } else {
        for friend in friends {
            println!("{} -> {}",
                friend.name,
                friend.gecos
            )
        }
    }

    Ok(())
}