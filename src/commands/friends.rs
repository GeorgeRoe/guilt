use crate::users::{User, get_all_users};
use crate::guilt_directory::guilt_directory_for_user;
use colored::Colorize;

pub fn run() -> anyhow::Result<()> {
    let friends: Vec<User> = get_all_users()?.into_iter().filter(|user| guilt_directory_for_user(user).exists()).collect();

    if friends.is_empty() {
        println!("{}", "You are the only GUILT user on this system :(".red());
    } else {
        for friend in friends {
            println!("{} -> {}", friend.name, friend.gecos)
        }
    }

    Ok(())
}
