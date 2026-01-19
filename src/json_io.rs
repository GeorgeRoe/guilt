use serde::{Serialize, de::DeserializeOwned};
use std::fs::File;
use std::io;
use std::io::{BufReader, BufWriter};
use std::path::Path;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum JsonFileOperationError {
    #[error("I/O error: {0}")]
    Io(#[from] io::Error),

    #[error("JSON serialization/deserialization error: {0}")]
    Serde(#[from] serde_json::Error),
}

pub fn read_json_file<T: DeserializeOwned, P: AsRef<Path>>(
    path: P,
) -> Result<T, JsonFileOperationError> {
    let file = File::open(path).map_err(JsonFileOperationError::Io)?;
    let reader = BufReader::new(file);
    let data = serde_json::from_reader(reader).map_err(JsonFileOperationError::Serde)?;
    Ok(data)
}

pub fn write_json_file<T: Serialize, P: AsRef<Path>>(
    path: P,
    data: &T,
) -> Result<(), JsonFileOperationError> {
    let file = File::create(path).map_err(JsonFileOperationError::Io)?;
    let writer = BufWriter::new(file);
    serde_json::to_writer_pretty(writer, data).map_err(JsonFileOperationError::Serde)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::NamedTempFile;

    #[test]
    fn test_write_read_json_file_success() {
        let temp_file = NamedTempFile::new().unwrap();

        let test_data = vec!["item1", "item2", "item3"];

        write_json_file(temp_file.path(), &test_data).unwrap(); 

        let read_data: Vec<String> = read_json_file(temp_file.path()).unwrap();

        assert_eq!(test_data, read_data);
    }

    #[test]
    fn test_write_json_file_invalid_data() {
        let temp_file = NamedTempFile::new().unwrap();

        let test_data = vec!["item1", "item2", "item3"];

        write_json_file(temp_file.path(), &test_data).unwrap();

        let result: Result<Vec<u32>, JsonFileOperationError> = read_json_file(temp_file.path());

        assert!(matches!(result, Err(JsonFileOperationError::Serde(_))));
    }
}