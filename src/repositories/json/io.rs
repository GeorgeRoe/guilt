use crate::SomeError;
use serde::{Serialize, de::DeserializeOwned};
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::path::Path;

pub fn read_json_file<T: DeserializeOwned, P: AsRef<Path>>(path: P) -> Result<T, SomeError> {
    let file = File::open(path)?;
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
