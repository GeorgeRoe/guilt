use reqwest;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct IpInfo {
    pub postal: String,
}

pub async fn fetch_ip_info() -> reqwest::Result<IpInfo> {
    let response = reqwest::get("https://ipinfo.io/json").await?;

    let response = response.error_for_status()?;

    response.json().await
}
