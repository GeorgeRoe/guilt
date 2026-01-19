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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_from_getent_passwd_line_success() {
        let line = "johndoe:x:1001:1001:John Doe:/home/johndoe:/bin/bash";
        let user = User::from_getent_passwd_line(line).unwrap();

        assert_eq!(user.name, "johndoe");
        assert_eq!(user.gecos, "John Doe");
        assert_eq!(user.home_dir, PathBuf::from("/home/johndoe"));
    }

    #[test]
    fn test_from_getent_passwd_line_incorrect_field_count() {
        let line = "a:b";
        let result = User::from_getent_passwd_line(line);
        assert!(matches!(
            result,
            Err(ParseGetentPasswdError::IncorrectFieldCount(_, 2))
        ));
    }
}
