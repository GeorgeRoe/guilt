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

macro_rules! get_required_type {
    (
        fn $name:ident -> $ret:ty,
        $accessor:ident,
        $type_name:expr
    ) => {
        fn $name(&self, key: &str) -> Result<$ret, StructuredJsonError> {
            self.get_required(key)?
                .$accessor()
                .ok_or_else(|| StructuredJsonError::InvalidType(
                    key.to_string(),
                    $type_name.to_string(),
                ))
        }
    };
}

impl JsonGetExtensions for serde_json::Map<String, Value> {
    fn get_required(&self, key: &str) -> Result<&Value, StructuredJsonError> {
        self.get(key)
            .ok_or_else(|| StructuredJsonError::MissingField(key.to_string()))
    }

    get_required_type!(
        fn get_required_str -> &str,
        as_str,
        "string"
    );

    get_required_type!(
        fn get_required_i64 -> i64,
        as_i64,
        "integer"
    );

    get_required_type!(
        fn get_required_f64 -> f64,
        as_f64,
        "float"
    );

    get_required_type!(
        fn get_required_array -> &Vec<Value>,
        as_array,
        "array"
    );

    get_required_type!(
        fn get_required_object -> &serde_json::Map<String, Value>,
        as_object,
        "object"
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_required_succes() {
        let json = serde_json::json!({
            "key": "value"
        });

        let obj = json.as_object().unwrap();

        let value = obj.get_required("key").unwrap().as_str().unwrap();

        assert_eq!(value, "value");
    }

    #[test]
    fn test_get_required_missing_field() {
        let json = serde_json::json!({});

        let obj = json.as_object().unwrap();

        let missing_key = "missing_key";
        let result = obj.get_required(missing_key);

        assert!(matches!(
            result,
            Err(StructuredJsonError::MissingField(field)) if field == missing_key
        ))
    }

    #[test]
    fn test_get_required_type_invalid_value() {
        let json = serde_json::json!({
            "key": 42
        });

        let obj = json.as_object().unwrap();

        let result = obj.get_required_str("key");

        assert!(matches!(
            result,
            Err(StructuredJsonError::InvalidType(field, type_name))
            if field == "key" && type_name == "string"
        ))
    }

    #[test]
    fn test_get_required_type_success() {
        let json = serde_json::json!({
            "key": 123
        });

        let obj = json.as_object().unwrap();

        let result = obj.get_required_i64("key").unwrap();

        assert_eq!(result, 123);
    }
}