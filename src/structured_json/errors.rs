use thiserror::Error;

#[derive(Error, Debug)]
pub enum StructuredJsonError {
    #[error("Missing required field: {0}")]
    MissingField(String),

    #[error("Invalid type for field: {0}. Expected: {1}")]
    InvalidType(String, String),
}

#[derive(Error, Debug)]
pub enum StructuredJsonParsingError {
    #[error("Structured Json error: {0}")]
    Structure(#[from] StructuredJsonError),

    #[error("JSON parsing error: {0}")]
    Parsing(#[from] serde_json::Error),
}
