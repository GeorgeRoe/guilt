use crate::json_io::*;
use std::collections::HashMap;
use std::path::Path;
use serde::{Serialize, de::DeserializeOwned};

pub trait JsonKey {
  fn json_key(&self) -> String;
}

pub struct JsonCollection<T>
where T: Serialize + DeserializeOwned + Clone + JsonKey
{
  cache: HashMap<String, T>
}

impl<T> JsonCollection<T>
where
    T: Serialize + DeserializeOwned + Clone + JsonKey
{
  pub fn empty() -> Self {
    Self {
      cache: HashMap::new(),
    }
  }

  pub fn read(path: &Path) -> Result<Self, JsonFileOperationError> {
    let items: Vec<T> = read_json_file(path)?;
    let cache = items.into_iter().map(|i| (i.json_key(), i)).collect();
    Ok(Self { cache })
  }

  pub fn write(&self, path: &Path) -> Result<(), JsonFileOperationError> {
    let items: Vec<&T> = self.cache.values().collect();
    write_json_file(path, &items)
  }

  pub fn get(&self, key: &str) -> Option<T> {
    self.cache.get(key).cloned()
  }

  pub fn all(&self) -> Vec<T> {
    self.cache.values().cloned().collect()
  }

  pub fn upsert(&mut self, item: T) {
    self.cache.insert(item.json_key(), item);
  }

  pub fn remove(&mut self, key: &str) {
    self.cache.remove(key);
  }
}

#[cfg(test)]
mod tests {
  use super::*;

  struct ExampleStruct {
    value: String
  }

  impl JsonKey for ExampleStruct {
    fn json_key(&self) -> String {
      self.value.clone()
    }
  }

  #[test]
  fn test_read_json_collection() {
    let temp_dir = tempfile::tempdir().unwrap();
    let file_path = temp_dir.path().join("example_collection.json");

    let example_structs = vec![
      ExampleStruct { value: "one".to_string() },
      ExampleStruct { value: "two".to_string() },
    ];

    write_json_file(&file_path, &example_structs).unwrap();

    let collection = JsonCollection::<ExampleStruct>::read(&file_path).unwrap();

    assert_eq!(collection.get("one").unwrap().value, "one");
    assert_eq!(collection.get("two").unwrap().value, "two");
  }

  #[test]
  fn test_write_json_collection() {
    let temp_dir = tempfile::tempdir().unwrap();
    let file_path = temp_dir.path().join("example_collection.json");

    let mut collection = JsonCollection::<ExampleStruct>::empty();
    collection.upsert(ExampleStruct { value: "one".to_string() });
    collection.upsert(ExampleStruct { value: "two".to_string() });

    collection.write(&file_path).unwrap();

    let read_collection = JsonCollection::<ExampleStruct>::read(&file_path).unwrap();

    assert_eq!(read_collection.get("one").unwrap().value, "one");
    assert_eq!(read_collection.get("two").unwrap().value, "two");
  }

  #[test]
  fn test_upsert_and_remove_structs_from_json_collection() {
    let mut collection = JsonCollection::<ExampleStruct>::empty();

    collection.upsert(ExampleStruct { value: "one".to_string() });
    assert!(collection.get("one").is_some());

    collection.remove("one");
    assert!(collection.get("one").is_none());

  }
}