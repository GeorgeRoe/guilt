use super::types::*;
use crate::structured_json::{JsonGetExtensions, errors::*};
use chrono::{TimeZone, Utc};
use serde_json::Value;

impl SlurmAccountingResources {
    fn from_value_array(values: &[Value]) -> Result<Self, StructuredJsonError> {
        let mut resources = Self { cpu: None };

        for entry in values {
            let resource_type = entry
                .get("type")
                .ok_or(StructuredJsonError::MissingField(
                    "resource type".to_string(),
                ))?
                .as_str()
                .ok_or(StructuredJsonError::InvalidType(
                    "resource type".to_string(),
                    "string".to_string(),
                ))?;
            let count = entry
                .get("count")
                .ok_or(StructuredJsonError::MissingField(
                    "resource count".to_string(),
                ))?
                .as_f64()
                .ok_or(StructuredJsonError::InvalidType(
                    "resource count".to_string(),
                    "number".to_string(),
                ))?;

            if resource_type == "cpu" {
                resources.cpu = Some(count);
            }
        }

        Ok(resources)
    }
}

impl SlurmAccountingResult {
    fn from_value(obj: &serde_json::Map<String, Value>) -> Result<Self, StructuredJsonError> {
        // parse job_id
        let job_id = obj.get_required_i64("job_id")?.to_string();

        // parse time data
        let time_obj = obj.get_required_object("time")?;

        // start time
        let start_time_timestamp = time_obj.get_required_i64("start")?;

        let start_time = if start_time_timestamp > 0 {
            Utc.timestamp_opt(start_time_timestamp, 0)
                .single()
                .map(StartTime::Started)
                .ok_or(StructuredJsonError::InvalidType(
                    "start".to_string(),
                    "unix timestamp".to_string(),
                ))?
        } else {
            StartTime::NotStarted
        };

        // end time
        let end_time_timestamp = time_obj.get_required_i64("end")?;

        let end_time = if end_time_timestamp > 0 {
            Utc.timestamp_opt(end_time_timestamp, 0)
                .single()
                .map(EndTime::Finished)
                .ok_or(StructuredJsonError::InvalidType(
                    "end".to_string(),
                    "unix timestamp".to_string(),
                ))?
        } else {
            EndTime::NotFinished
        };

        // parse reources
        let resources = SlurmAccountingResources::from_value_array(
            obj.get_required_object("tres")?
                .get_required_array("allocated")?,
        )?;

        Ok(Self {
            job_id,
            start_time,
            end_time,
            resources,
        })
    }
}

pub fn parse_command_output(
    stdout: &str,
) -> Result<Vec<SlurmAccountingResult>, StructuredJsonParsingError> {
    let root: Value = serde_json::from_str(stdout).map_err(StructuredJsonParsingError::Parsing)?;

    let root = root
        .as_object()
        .ok_or(StructuredJsonParsingError::Structure(
            StructuredJsonError::InvalidType("root".to_string(), "JSON object".to_string()),
        ))?;

    let job_json_values = root.get_required_array("jobs")?;

    let jobs: Vec<SlurmAccountingResult> = job_json_values
        .iter()
        .map(|value| {
            let item = value.as_object().ok_or_else(|| {
                StructuredJsonParsingError::Structure(StructuredJsonError::InvalidType(
                    "job item".to_string(),
                    "JSON object".to_string(),
                ))
            })?;
            SlurmAccountingResult::from_value(item).map_err(StructuredJsonParsingError::Structure)
        })
        .collect::<Result<_, StructuredJsonParsingError>>()?;

    Ok(jobs)
}
