use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Node {
	pub architecture: String,

	pub cores: i32,

	pub cpus: i32,

	pub features: Vec<String>,

	pub name: String,

	pub operating_system: String,

	pub partitions: Vec<String>,

	#[serde(rename = "real_memory")]
	pub memory: u64,

	pub sockets: i32,

	pub threads: i32,
}