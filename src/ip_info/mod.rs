pub mod types;

use reqwest;
use crate::ip_info::types::IpInfo;

pub async fn fetch_ip_info() -> Result<IpInfo, reqwest::Error> {
    let response = reqwest::get("https://ipinfo.io/json").await?;

    let response = response.error_for_status()?;

    let ip_info: IpInfo = response.json().await?;
    Ok(ip_info)
}