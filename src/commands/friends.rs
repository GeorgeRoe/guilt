use crate::guilt_dir::has_guilt_dir;
use crate::users::{User, get_all_users};
use colored::Colorize;

pub fn run() -> anyhow::Result<()> {
    let friends: Vec<User> = get_all_users()?.into_iter().filter(has_guilt_dir).collect();

    if friends.is_empty() {
        println!("{}", "You are the only GUILT user on this system :(".red());
    } else {
        for friend in friends {
            println!("{} -> {}", friend.name, friend.gecos)
        }
    }

    Ok(())
}
