use rhai::{AST, Dynamic, Engine, EvalAltResult, Map, Scope};
use std::path::Path;
use crate::slurm::constraint::Constraint;
use thiserror::Error;

pub struct ProfileResolutionPolicyParameters {
	pub partition: String,
	pub constraints: Option<Constraint>,
}

impl ProfileResolutionPolicyParameters {
	pub fn new(partition: &str, constraints: Option<Constraint>) -> Self {
		Self {
			partition: partition.to_string(),
			constraints,
		}
	}

	pub fn to_map(&self) -> Map {
		let mut map = Map::new();
		map.insert("partition".into(), self.partition.clone().into());
		map
	}
}

#[derive(Debug, Error)]
pub enum ProfileResolutionPolicyFromFileError {
	#[error("failed to compile profile resolution script: {0}")]
	Compilation(#[from] EvalAltResult),

	#[error("script does not contain an 'identify_cpu' function")]
	NoIdentifyCpuFunction,

	#[error("The function 'idenfity_cpu' should only take 1 parameter")]
	InvalidIdentifyCpuFunction,
}

pub struct ProfileResolutionPolicy {
	ast: AST,
}

impl ProfileResolutionPolicy {
	pub fn from_file(path: &Path) -> Result<Self, ProfileResolutionPolicyFromFileError> {
		let engine = Engine::new();

		match engine.compile_file(path.to_path_buf()) {
			Ok(ast) => {
				let identify_cpu_fn = ast.iter_functions().find(|f| f.name == "identify_cpu");

				match identify_cpu_fn {
					Some(function) => if function.params.len() == 1 {
						Ok(Self { ast })
					} else {
						Err(ProfileResolutionPolicyFromFileError::InvalidIdentifyCpuFunction)
					},
					None => Err(ProfileResolutionPolicyFromFileError::NoIdentifyCpuFunction)
				}
			},
			Err(e) => Err(ProfileResolutionPolicyFromFileError::Compilation(*e))
		}
	}

	pub fn resolve_cpu_profile(&self, parameters: &ProfileResolutionPolicyParameters) -> Result<String, EvalAltResult> {
		let engine = Engine::new();
		let mut scope = Scope::new();

		let job_data = parameters.to_map();

		let result: Dynamic = engine.call_fn(&mut scope, &self.ast, "identify_cpu", (job_data,)).map_err(|e| *e)?;
		
		Ok(result.to_string())
	}
}