static DATE_TIME_FORMAT: &str = "%Y-%m-%dT%H:%MZ";

use super::{CarbonIntensityTimeSegment, FetchCarbonIntensity};

mod parsing;
mod types;

mod fetch;
pub use fetch::{ApiFetchCarbonIntensity, CarbonIntensityApiFetchError};
