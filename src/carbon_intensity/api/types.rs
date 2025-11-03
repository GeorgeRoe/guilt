use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct Intensity {
    pub forecast: i32,
}

#[derive(Deserialize, Debug)]
pub struct GenerationMix {
    pub fuel: String,
    pub perc: f64,
}

#[derive(Deserialize, Debug)]
pub struct Data {
    pub from: String,
    pub to: String,
    pub intensity: Intensity,
    pub generationmix: Vec<GenerationMix>,
}

#[derive(Deserialize, Debug)]
pub struct RegionData {
    pub data: Vec<Data>,
}

#[derive(Deserialize, Debug)]
pub struct ApiError {
    pub code: String,
    pub message: String,
}
