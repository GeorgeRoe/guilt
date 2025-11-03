mod fetch;
pub use fetch::FetchCarbonIntensity;

mod types;
pub use types::CarbonIntensityTimeSegment;

pub mod api;

mod aggregator;
pub use aggregator::CarbonIntensityAggregator;
