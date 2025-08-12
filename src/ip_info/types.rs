use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct IpInfo {
    pub postal: String,
}
