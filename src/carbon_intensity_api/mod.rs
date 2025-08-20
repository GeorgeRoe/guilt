static DATE_TIME_FORMAT: &str = "%Y-%m-%dT%H:%M:%S%z";

mod api_types;

mod types;
pub use types::CarbonIntensityTimeSegment;

mod parsing;

mod fetch;
pub use fetch::{CarbonIntensityApiFetchError, fetch_carbon_intensity};
