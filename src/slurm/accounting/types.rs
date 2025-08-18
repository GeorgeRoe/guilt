use chrono::{DateTime, Utc};
use std::fmt;

#[derive(Debug)]
pub struct SlurmAccountingResources {
    pub cpu: Option<f64>,
}

pub enum StartTime {
    Started(DateTime<Utc>),
    NotStarted,
}

impl fmt::Display for StartTime {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            StartTime::Started(time) => write!(f, "{}", time),
            StartTime::NotStarted => write!(f, "Not Started"),
        }
    }
}

pub enum EndTime {
    Finished(DateTime<Utc>),
    NotFinished,
}

impl fmt::Display for EndTime {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            EndTime::Finished(time) => write!(f, "{}", time),
            EndTime::NotFinished => write!(f, "Not Finished"),
        }
    }
}

pub struct SlurmAccountingResult {
    pub job_id: String,
    pub start_time: StartTime,
    pub end_time: EndTime,
    pub resources: SlurmAccountingResources,
}
