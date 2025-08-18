use super::errors::StructuredJsonError;
use serde_json::Value;

pub trait JsonGetExtensions {
    fn get_required(&self, key: &str) -> Result<&Value, StructuredJsonError>;
    fn get_required_str(&self, key: &str) -> Result<&str, StructuredJsonError>;
    fn get_required_i64(&self, key: &str) -> Result<i64, StructuredJsonError>;
    fn get_required_f64(&self, key: &str) -> Result<f64, StructuredJsonError>;
    fn get_required_array(&self, key: &str) -> Result<&Vec<Value>, StructuredJsonError>;
    fn get_required_object(
        &self,
        key: &str,
    ) -> Result<&serde_json::Map<String, Value>, StructuredJsonError>;
}

impl JsonGetExtensions for serde_json::Map<String, Value> {
    fn get_required(&self, key: &str) -> Result<&Value, StructuredJsonError> {
        self.get(key)
            .ok_or_else(|| StructuredJsonError::MissingField(key.to_string()))
    }

    fn get_required_str(&self, key: &str) -> Result<&str, StructuredJsonError> {
        self.get_required(key)?
            .as_str()
            .ok_or_else(|| StructuredJsonError::InvalidType(key.to_string(), "string".to_string()))
    }

    fn get_required_i64(&self, key: &str) -> Result<i64, StructuredJsonError> {
        self.get_required(key)?
            .as_i64()
            .ok_or_else(|| StructuredJsonError::InvalidType(key.to_string(), "integer".to_string()))
    }

    fn get_required_f64(&self, key: &str) -> Result<f64, StructuredJsonError> {
        self.get_required(key)?
            .as_f64()
            .ok_or_else(|| StructuredJsonError::InvalidType(key.to_string(), "float".to_string()))
    }

    fn get_required_array(&self, key: &str) -> Result<&Vec<Value>, StructuredJsonError> {
        self.get_required(key)?
            .as_array()
            .ok_or_else(|| StructuredJsonError::InvalidType(key.to_string(), "array".to_string()))
    }

    fn get_required_object(
        &self,
        key: &str,
    ) -> Result<&serde_json::Map<String, Value>, StructuredJsonError> {
        self.get_required(key)?
            .as_object()
            .ok_or_else(|| StructuredJsonError::InvalidType(key.to_string(), "object".to_string()))
    }
}
