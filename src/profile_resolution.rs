use crate::slurm::node::Node;
use rhai::{AST, Dynamic, Engine, EvalAltResult, Scope};
use std::path::Path;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ProfileResolutionPolicyFromFileError {
    #[error("failed to compile profile resolution script: {0}")]
    Compilation(#[from] EvalAltResult),

    #[error("script does not contain an 'identify_cpu' function")]
    NoIdentifyCpuFunction,

    #[error("The function 'idenfity_cpu' should only take 2 parameter")]
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
                    Some(function) => {
                        if function.params.len() == 2 {
                            Ok(Self { ast })
                        } else {
                            Err(ProfileResolutionPolicyFromFileError::InvalidIdentifyCpuFunction)
                        }
                    }
                    None => Err(ProfileResolutionPolicyFromFileError::NoIdentifyCpuFunction),
                }
            }
            Err(e) => Err(ProfileResolutionPolicyFromFileError::Compilation(*e)),
        }
    }

    pub fn resolve_cpu_profile(
        &self,
        partition: String,
        nodes: Vec<Node>,
    ) -> Result<String, EvalAltResult> {
        let engine = Engine::new();
        let mut scope = Scope::new();

        let result: Dynamic = engine
            .call_fn(&mut scope, &self.ast, "identify_cpu", (partition, nodes))
            .map_err(|e| *e)?;

        Ok(result.to_string())
    }
}
