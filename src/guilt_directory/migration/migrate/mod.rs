pub use super::Migration;

mod repo_migrations;
use repo_migrations::MigrateToRepoMigrations;

pub fn all_migrations_in_order() -> Vec<Box<dyn Migration>> {
    vec![Box::new(MigrateToRepoMigrations)]
}
