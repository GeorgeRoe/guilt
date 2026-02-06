use super::Migration;
use crate::users::User;
use crate::json_io::{read_json_file, write_json_file};
use std::fs::{read_to_string, write};
use crate::version::Version;
use serde::{Serialize, Deserialize};
use chrono::{DateTime, Utc};
use std::collections::HashMap;

// Unprocessed Jobs

#[derive(Serialize, Deserialize)]
struct OldUnprocessedJob {
	pub job_id: String,
	pub cpu_profile_name: String,
}

#[derive(Serialize, Deserialize)]
pub enum CpuProfileResolutionData {
	Name(String),
	None
}

#[derive(Serialize, Deserialize)]
struct NewUnprocessedJob {
	pub job_id: String,
	pub cpu_profile_resolution_data: CpuProfileResolutionData,
}

impl From<OldUnprocessedJob> for NewUnprocessedJob {
	fn from(old: OldUnprocessedJob) -> Self {
		Self {
			job_id: old.job_id,
			cpu_profile_resolution_data: if old.cpu_profile_name == "Default" {
				CpuProfileResolutionData::None
			} else {
				CpuProfileResolutionData::Name(old.cpu_profile_name)
			}
		}
	}
}

// Processed Jobs

#[derive(Deserialize, Serialize)]
struct OldProcessedJob {
	pub start_time: DateTime<Utc>,
	pub end_time: DateTime<Utc>,
	pub job_id: String,
	pub cpu_profile_name: String,
	pub energy: f64,
	pub emissions: f64,
	pub generation_mix: HashMap<String, f64>,
}

// CPU Profiles

#[derive(Deserialize, Serialize)]
pub struct OldCpuProfile {
    pub name: String,
    pub cores: u16,
    pub tdp: f32,
}

// Migration

pub struct MigrateToProfileResolution;

impl Migration for MigrateToProfileResolution {
	fn migrate(&self, user: &User) -> anyhow::Result<()> {
		let guilt_dir_path = user.home_dir.join(".guilt");

		let unprocessed_jobs_path = guilt_dir_path.join("unprocessed_jobs.json");
		let old_unprocessed_jobs: Vec<OldUnprocessedJob> = read_json_file(&unprocessed_jobs_path)?;
		let new_unprocessed_jobs: Vec<NewUnprocessedJob> = old_unprocessed_jobs.into_iter().map(Into::into).collect();
		write_json_file(&unprocessed_jobs_path, &new_unprocessed_jobs)?;

		let processed_jobs_path = guilt_dir_path.join("processed_jobs.json");
		let old_processed_jobs: Vec<OldProcessedJob> = read_json_file(&processed_jobs_path)?;
		let new_processed_jobs: Vec<OldProcessedJob> = old_processed_jobs.into_iter().filter(|job| job.cpu_profile_name != "Default").collect();
		write_json_file(&processed_jobs_path, &new_processed_jobs)?;

		let cpu_profiles_path = guilt_dir_path.join("cpu_profiles.json");
		let old_cpu_profiles: Vec<OldCpuProfile> = read_json_file(&cpu_profiles_path)?;
		let new_cpu_profiles: Vec<OldCpuProfile> = old_cpu_profiles.into_iter().filter(|profile| profile.name != "Default").collect();
		write_json_file(&cpu_profiles_path, &new_cpu_profiles)?;

        write(guilt_dir_path.join("last_written_version"), b"1.3.0")?;

		Ok(())
	}

	fn detect_applicable(&self, user: &User) -> anyhow::Result<bool> {
		let last_written_version_path = user.home_dir.join(".guilt/last_written_version");

		let version_str = read_to_string(last_written_version_path)?.trim().to_string();
		let version = Version::parse_str(&version_str)?;

		Ok(version < Version::new(1, 3, 0))
	}
}

#[cfg(test)]
mod tests {
	use super::{
		MigrateToProfileResolution,
		Migration,
		NewUnprocessedJob,
		OldCpuProfile,
		OldProcessedJob,
		OldUnprocessedJob,
		CpuProfileResolutionData
	};
	use crate::users::TestingUser;
	use std::fs;
	use crate::json_io::{read_json_file, write_json_file};
	use chrono::{TimeZone, Utc};
	use std::collections::HashMap;

	fn new_old_processed_job(cpu_profile_name: &str) -> OldProcessedJob {
		OldProcessedJob {
			start_time: Utc.with_ymd_and_hms(2000, 1, 1, 1, 1, 1).unwrap(),
			end_time: Utc.with_ymd_and_hms(2001, 1, 1, 1, 1, 1).unwrap(),
			job_id: "0".to_string(),
			cpu_profile_name: cpu_profile_name.to_string(),
			energy: 0.0,
			emissions: 0.0,
			generation_mix: HashMap::new()
		}
	}

	fn setup_testing_user_with_previous_structure() -> anyhow::Result<TestingUser> {
		let testing_user = TestingUser::test_user()?;

		let guilt_dir = testing_user.user.home_dir.join(".guilt");

		fs::create_dir_all(&guilt_dir)?;

		write_json_file(
			guilt_dir.join("cpu_profiles.json"),
			&vec![
				OldCpuProfile {
					name: "Default".to_string(),
					cores: 1, 
					tdp: 10.0
				}
			]
		)?;

		write_json_file(
			guilt_dir.join("unprocessed_jobs.json"),
			&vec![
				OldUnprocessedJob {
					job_id: "1".to_string(),
					cpu_profile_name: "Default".to_string()
				},
				OldUnprocessedJob {
					job_id: "2".to_string(),
					cpu_profile_name: "Real CPU".to_string()
				}
			]
		)?;

		write_json_file(
			guilt_dir.join("processed_jobs.json"),
			&vec![
				new_old_processed_job("Default"),
				new_old_processed_job("Real Cpu")
			]
		)?;

        fs::write(guilt_dir.join("last_written_version"), b"1.2.1")?;

		Ok(testing_user)
	}

	#[test]
	fn detect_applicable_when_version_is_below_1_dot_3() {
		let testing_user = setup_testing_user_with_previous_structure().unwrap();

        let result = MigrateToProfileResolution.detect_applicable(&testing_user.user);

        assert!(matches!(result, Result::Ok(value) if value));
	}

	#[test]
	fn migrate_removes_processed_jobs_with_default_cpu() {
		let testing_user = setup_testing_user_with_previous_structure().unwrap();

		MigrateToProfileResolution.migrate(&testing_user.user).unwrap();

		let guilt_dir = testing_user.user.home_dir.join(".guilt");

		let processed_jobs: Vec<OldProcessedJob> = read_json_file(guilt_dir.join("processed_jobs.json")).unwrap();

		assert!(processed_jobs.iter().all(|job| job.cpu_profile_name != "Default"));
	}

	#[test]
	fn migrate_swaps_default_cpu_jobs_to_no_resolution_data() {
		let testing_user = setup_testing_user_with_previous_structure().unwrap();

		MigrateToProfileResolution.migrate(&testing_user.user).unwrap();

		let guilt_dir = testing_user.user.home_dir.join(".guilt");

		let unprocessed_jobs: Vec<NewUnprocessedJob> = read_json_file(guilt_dir.join("unprocessed_jobs.json")).unwrap();

		assert!(unprocessed_jobs.iter().all(|job| 
			matches!(&job.cpu_profile_resolution_data, CpuProfileResolutionData::Name(name) if name != "Default") ||
			matches!(job.cpu_profile_resolution_data, CpuProfileResolutionData::None)
		));
	}

	#[test]
	fn migrate_bumps_last_written_version() {
		let testing_user = setup_testing_user_with_previous_structure().unwrap();

		MigrateToProfileResolution.migrate(&testing_user.user).unwrap();

		let guilt_dir = testing_user.user.home_dir.join(".guilt");

		assert_eq!(fs::read_to_string(guilt_dir.join("last_written_version")).unwrap(), "1.3.0");
	}
}