use chrono::Duration;

pub struct SlurmScriptDirectives {
    pub time: Duration,
    pub nodes: i32,
    pub tasks_per_node: i32,
    pub cpus_per_task: i32,
}

pub struct GuiltScriptDirectives {
    pub cpu_profile: String,
}
