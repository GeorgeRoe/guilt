use super::User;
use std::path::PathBuf;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ParseGetentPasswdError {
    #[error("Field at index {1} is missing in getent passwd line: '{0}'")]
    MissingField(String, usize),

    #[error(
        "Incorrect number of fields in getent passwd line: expected 7, however '{0}' contains {1}"
    )]
    IncorrectFieldCount(String, usize),
}

impl User {
    pub fn from_getent_passwd_line(line: &str) -> Result<Self, ParseGetentPasswdError> {
        let fields: Vec<&str> = line.splitn(7, ":").collect();

        if fields.len() != 7 {
            return Err(ParseGetentPasswdError::IncorrectFieldCount(
                line.to_string(),
                fields.len(),
            ));
        }

        let name = fields
            .first()
            .ok_or_else(|| ParseGetentPasswdError::MissingField(line.to_string(), 0))?
            .to_string();
        let gecos = fields
            .get(4)
            .ok_or_else(|| ParseGetentPasswdError::MissingField(line.to_string(), 4))?
            .to_string();
        let home_dir = PathBuf::from(
            fields
                .get(5)
                .ok_or_else(|| ParseGetentPasswdError::MissingField(line.to_string(), 5))?,
        );

        Ok(User {
            name,
            gecos,
            home_dir,
        })
    }
}
