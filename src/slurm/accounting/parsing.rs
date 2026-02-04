use super::super::node_string::parse_slurm_nodes;
use super::types::*;
use crate::structured_json::{JsonGetExtensions, errors::*};
use chrono::{TimeZone, Utc};
use serde_json::Value;

impl SlurmAccountingResources {
    fn from_value_array(values: &[Value]) -> Result<Self, StructuredJsonError> {
        let mut resources = Self { cpu: None };

        for entry in values {
            match entry {
                Value::Object(map) => {
                    let resource_type = map
                        .get("type")
                        .ok_or(StructuredJsonError::MissingField(
                            "resource type".to_string(),
                        ))?
                        .as_str()
                        .ok_or(StructuredJsonError::InvalidType(
                            "resource type".to_string(),
                            "string".to_string(),
                        ))?;
                    let count = map
                        .get("count")
                        .ok_or(StructuredJsonError::MissingField(
                            "resource count".to_string(),
                        ))?
                        .as_f64()
                        .ok_or(StructuredJsonError::InvalidType(
                            "resource count".to_string(),
                            "number".to_string(),
                        ))?;

                    // allow single match here, as we may want to add more resource types in the future
                    #[allow(clippy::single_match)]
                    match resource_type {
                        "cpu" => {
                            resources.cpu = Some(count);
                        }
                        _ => {}
                    }
                }
                _ => {
                    return Err(StructuredJsonError::InvalidType(
                        "tres entry".to_string(),
                        "JSON object".to_string(),
                    ));
                }
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

        // parse partition
        let partition = obj.get_required_str("partition")?.to_string();

        // parse nodes
        let nodes_string = obj.get_required_str("nodes")?;
        let nodes = parse_slurm_nodes(nodes_string).map_err(|e| {
            StructuredJsonError::InvalidType(
                "nodes".to_string(),
                format!("valid node string: {}", e),
            )
        })?;

        Ok(Self {
            job_id,
            start_time,
            end_time,
            resources,
            partition,
            nodes,
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

#[cfg(test)]
mod tests {
    use super::*;

    mod test_from_value_array {
        use super::*;

        #[test]
        fn test_empty_array() {
            let value_array = vec![];

            let resources = SlurmAccountingResources::from_value_array(&value_array).unwrap();

            assert!(resources.cpu.is_none());
        }

        #[test]
        fn test_array_with_invalid_value() {
            let value_array = vec![serde_json::json!("invalid entry")];

            let result = SlurmAccountingResources::from_value_array(&value_array);

            assert!(matches!(
                result,
                Err(StructuredJsonError::InvalidType(field, _)) if field == "tres entry"
            ));
        }

        #[test]
        fn test_entry_without_type() {
            let value_array = vec![serde_json::json!({ "count": 8 })];

            let result = SlurmAccountingResources::from_value_array(&value_array);

            assert!(matches!(
                result,
                Err(StructuredJsonError::MissingField(field)) if field == "resource type"
            ));
        }

        #[test]
        fn test_entry_with_invalid_type() {
            let value_array = vec![serde_json::json!({ "type": 42, "count": 8 })];

            let result = SlurmAccountingResources::from_value_array(&value_array);

            assert!(matches!(
                result,
                Err(StructuredJsonError::InvalidType(field, _)) if field == "resource type"
            ));
        }

        #[test]
        fn test_entry_without_count() {
            let value_array = vec![serde_json::json!({ "type": "cpu" })];

            let result = SlurmAccountingResources::from_value_array(&value_array);

            assert!(matches!(
                result,
                Err(StructuredJsonError::MissingField(field)) if field == "resource count"
            ));
        }

        #[test]
        fn test_valid_cpu_entry() {
            let value_array = vec![serde_json::json!({ "type": "cpu", "count": 16 })];

            let resources = SlurmAccountingResources::from_value_array(&value_array).unwrap();

            assert_eq!(resources.cpu, Some(16.0));
        }

        #[test]
        fn test_missing_cpu_entry() {
            let value_array = vec![];

            let resources = SlurmAccountingResources::from_value_array(&value_array).unwrap();

            assert!(resources.cpu.is_none());
        }

        #[test]
        fn test_invalid_cpu_type() {
            let value_array = vec![serde_json::json!({ "type": "cpu", "count": "sixteen" })];

            let result = SlurmAccountingResources::from_value_array(&value_array);

            assert!(matches!(
                result,
                Err(StructuredJsonError::InvalidType(field, _)) if field == "resource count"
            ));
        }
    }

    mod test_from_value {
        use super::*;

        #[test]
        fn test_valid_json() {
            let job_id = 12345;
            let start_time = 1625079600;
            let end_time = 1625083200;
            let cpu_count = 8;

            let json = serde_json::json!({
                "job_id": job_id,
                "time": {
                    "start": start_time,
                    "end": end_time
                },
                "tres": {
                    "allocated": [
                        { "type": "cpu", "count": cpu_count }
                    ]
                },
                "partition": "test_partition",
                "nodes": "node1"
            });

            let obj = json.as_object().unwrap();

            let result = SlurmAccountingResult::from_value(obj).unwrap();

            assert_eq!(result.job_id, job_id.to_string());

            assert!(
                matches!(result.start_time, StartTime::Started(time) if time.timestamp() == start_time)
            );
            assert!(
                matches!(result.end_time, EndTime::Finished(time) if time.timestamp() == end_time)
            );

            assert_eq!(result.resources.cpu, Some(cpu_count as f64));

            assert_eq!(result.partition, "test_partition".to_string());

            assert!(matches!(
                result.nodes,
                Some(nodes) if nodes == vec!["node1".to_string()]
            ))
        }

        #[test]
        fn test_valid_json_with_less_data() {
            let job_id = 12345;

            let json = serde_json::json!({
                "job_id": job_id,
                "time": {
                    "start": 0,
                    "end": 0
                },
                "tres": {
                    "allocated": []
                },
                "partition": "test_partition",
                "nodes": "None assigned"
            });

            let obj = json.as_object().unwrap();

            let result = SlurmAccountingResult::from_value(obj).unwrap();

            assert_eq!(result.job_id, job_id.to_string());

            assert!(matches!(result.start_time, StartTime::NotStarted));
            assert!(matches!(result.end_time, EndTime::NotFinished));

            assert!(result.resources.cpu.is_none());

            assert_eq!(result.partition, "test_partition".to_string());

            assert!(result.nodes.is_none());
        }
    }
}
