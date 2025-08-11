use std::fs::File;
use std::io::{BufWriter, BufReader};
use serde::{Serialize, de::DeserializeOwned};
use crate::SomeError;
use std::path::Path;

pub fn read_json_file<T: DeserializeOwned, P: AsRef<Path>>(path: P) -> Result<T, SomeError> {
    let file = File::create(path)?;
    let reader = BufReader::new(file);
    let data = serde_json::from_reader(reader)?;
    Ok(data)
}

pub fn write_json_file<T: Serialize, P: AsRef<Path>>(path: P, data: &T) -> Result<(), SomeError> {
    let file = File::create(path)?;
    let writer = BufWriter::new(file);
    serde_json::to_writer_pretty(writer, data)?;
    Ok(())
}