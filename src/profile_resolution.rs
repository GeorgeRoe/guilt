use crate::slurm::node::Node;
use rhai::{AST, Dynamic, Engine, EvalAltResult, ParseError, Scope, serde::to_dynamic};
use std::path::Path;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum InvalidProfileResolutionPolicyScriptError {
    #[error("Script does not contain an 'identify_cpu' function")]
    NoIdentifyCpuFunction,

    #[error("The function 'idenfity_cpu' should take 2 parameters, not {0}")]
    InvalidIdentifyCpuFunctionNumParams(usize),
}

#[derive(Debug, Error)]
pub enum ProfileResolutionPolicyFromFileError {
    #[error("Failed to compile profile resolution script: {0}")]
    Compilation(#[from] EvalAltResult),

    #[error("Profile resolution policy script is invalid: {0}")]
    InvalidScript(#[from] InvalidProfileResolutionPolicyScriptError),
}

#[derive(Debug, Error)]
pub enum ProfileResolutionPolicyFromStringError {
    #[error("Failed to compile profile resolution script: {0}")]
    Compilation(#[from] ParseError),

    #[error("Profile resolution policy script is invalid: {0}")]
    InvalidScript(#[from] InvalidProfileResolutionPolicyScriptError),
}

fn validate_ast(ast: AST) -> Result<AST, InvalidProfileResolutionPolicyScriptError> {
    let identify_cpu_fn = ast
        .iter_functions()
        .find(|f| f.name == "identify_cpu")
        .ok_or(InvalidProfileResolutionPolicyScriptError::NoIdentifyCpuFunction)?;

    let identify_cpu_num_params = identify_cpu_fn.params.len();
    if identify_cpu_num_params == 2 {
        Ok(ast)
    } else {
        Err(
            InvalidProfileResolutionPolicyScriptError::InvalidIdentifyCpuFunctionNumParams(
                identify_cpu_num_params,
            ),
        )
    }
}

pub struct ProfileResolutionPolicy {
    ast: AST,
    engine: Engine,
}

impl ProfileResolutionPolicy {
    pub fn from_script(script: &str) -> Result<Self, ProfileResolutionPolicyFromStringError> {
        let engine = Engine::new();

        let ast = engine.compile(script)?;

        Ok(Self {
            ast: validate_ast(ast)?,
            engine,
        })
    }

    pub fn from_file(path: &Path) -> Result<Self, ProfileResolutionPolicyFromFileError> {
        let engine = Engine::new();

        let ast = engine
            .compile_file(path.to_path_buf())
            .map_err(|e| ProfileResolutionPolicyFromFileError::Compilation(*e))?;

        Ok(Self {
            ast: validate_ast(ast)?,
            engine,
        })
    }

    pub fn resolve_cpu_profile(
        &self,
        partition: String,
        nodes: Vec<Node>,
    ) -> Result<String, EvalAltResult> {
        let nodes_dynamic = to_dynamic(&nodes).map_err(|e| *e)?;

        let mut scope = Scope::new();

        let result: Dynamic = self
            .engine
            .call_fn(
                &mut scope,
                &self.ast,
                "identify_cpu",
                (partition, nodes_dynamic),
            )
            .map_err(|e| *e)?;

        Ok(result.to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    mod test_validate_ast {
        use super::*;

        #[test]
        fn with_no_identify_cpu_fn_fails() {
            let engine = Engine::new();

            let ast = engine.compile("").unwrap();

            let result = validate_ast(ast);

            assert!(matches!(
                result,
                Err(e) if matches!(
                    e,
                    InvalidProfileResolutionPolicyScriptError::NoIdentifyCpuFunction
                )
            ));
        }

        #[test]
        fn with_identify_cpu_fn_wrong_num_params_fails() {
            let engine = Engine::new();

            let ast = engine.compile("fn identify_cpu(one_arg) {}").unwrap();

            let result = validate_ast(ast);

            println!("{:?}", result);

            assert!(matches!(
                result,
                Err(e) if matches!(
                    e,
                    InvalidProfileResolutionPolicyScriptError::InvalidIdentifyCpuFunctionNumParams(num) if num == 1
                )
            ))
        }

        #[test]
        fn with_valid_identify_cpu_fn_succeeds() {
            let engine = Engine::new();

            let ast = engine
                .compile("fn identify_cpu(partition, nodes) {}")
                .unwrap();

            validate_ast(ast).unwrap();
        }
    }

    mod test_profile_resolution_policy_from_script {
        use super::*;

        #[test]
        fn invalid_code_fails() {
            let result = ProfileResolutionPolicy::from_script(
                "as2830jlkdf a-1=235sijodf ak1'[35#'123lsd f12[3#51aj3ie",
            );

            assert!(result.is_err())
        }

        #[test]
        fn correct_code_compiles() {
            let result =
                ProfileResolutionPolicy::from_script("fn identify_cpu(partition, nodes) {}");

            assert!(result.is_ok())
        }
    }

    mod test_profile_resolution_policy_from_file {
        use super::*;
        use std::fs::write;
        use tempfile::tempdir;

        #[test]
        fn non_existent_file_fails() {
            let temp_dir = tempdir().unwrap();
            let file_path = temp_dir.path().join("this_doesnt_exist.rhai");

            let result = ProfileResolutionPolicy::from_file(&file_path);

            assert!(result.is_err())
        }

        #[test]
        fn invalid_file_fails() {
            let temp_dir = tempdir().unwrap();
            let file_path = temp_dir.path().join("my_file.rhai");

            write(&file_path, "am49q0-443]2cm4-=2=c23m").unwrap();

            let result = ProfileResolutionPolicy::from_file(&file_path);

            assert!(result.is_err())
        }

        #[test]
        fn existing_valid_file_compiles() {
            let temp_dir = tempdir().unwrap();
            let file_path = temp_dir.path().join("my_file.rhai");

            write(&file_path, "fn identify_cpu(partition, nodes) {}").unwrap();

            let result = ProfileResolutionPolicy::from_file(&file_path);

            assert!(result.is_ok())
        }
    }

    #[test]
    fn successfully_resolves_a_cpu_profile() {
        let cpu_profile_name = "test";

        let profile_resolution_policy = ProfileResolutionPolicy::from_script(&format!(
            "fn identify_cpu(partition, nodes) {{ \"{}\" }}",
            cpu_profile_name
        ))
        .unwrap();

        assert_eq!(
            profile_resolution_policy
                .resolve_cpu_profile("".to_string(), vec![])
                .unwrap(),
            cpu_profile_name
        )
    }

    #[test]
    fn successfully_takes_nodes() {
        let architecture = "architecture";
        let cores = 2;
        let cpus = 2;
        let features = vec!["feature1".to_string(), "feature2".to_string()];
        let name = "name";
        let operating_system = "";
        let partitions = vec!["partition1".to_string(), "partition2".to_string()];
        let memory = 2;
        let sockets = 2;
        let threads = 2;

        let nodes = vec![Node {
            architecture: architecture.to_string(),
            cores,
            cpus,
            features: features.clone(),
            name: name.to_string(),
            operating_system: operating_system.to_string(),
            partitions: partitions.clone(),
            memory,
            sockets,
            threads,
        }];

        let tests = vec![
            ("name".to_string(), name.to_string()),
            ("architecture".to_string(), architecture.to_string()),
            ("cores".to_string(), cores.to_string()),
            ("cpus".to_string(), cpus.to_string()),
            ("features[0]".to_string(), features[0].clone()),
            ("features[1]".to_string(), features[1].clone()),
            ("operating_system".to_string(), operating_system.to_string()),
            ("partitions[0]".to_string(), partitions[0].clone()),
            ("partitions[1]".to_string(), partitions[1].clone()),
            ("memory".to_string(), memory.to_string()),
            ("sockets".to_string(), sockets.to_string()),
            ("threads".to_string(), threads.to_string()),
        ];

        tests.iter().for_each(|(getter, expected_value)| {
            let profile_resolution_policy = ProfileResolutionPolicy::from_script(&format!(
                "fn identify_cpu(partition, nodes) {{ let n = nodes[0]; n.{} }}",
                getter
            ))
            .unwrap();

            let result = profile_resolution_policy
                .resolve_cpu_profile("".to_string(), nodes.clone())
                .unwrap();

            assert_eq!(result, expected_value.to_string());
        });
    }

    #[test]
    fn successfully_takes_partition() {
        let expected_value = "TestPartition";

        let profile_resolution_policy =
            ProfileResolutionPolicy::from_script("fn identify_cpu(partition, nodes) { partition }")
                .unwrap();

        let result = profile_resolution_policy
            .resolve_cpu_profile(expected_value.to_string(), vec![])
            .unwrap();

        assert_eq!(result, expected_value);
    }
}
