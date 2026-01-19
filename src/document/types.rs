use crate::plotting::ChartDefinition;

#[derive(Debug, Clone, Copy)]
pub enum HeadingLevel {
    H1,
    H2,
    H3,
    H4,
    H5,
    H6,
}

impl HeadingLevel {
    pub fn index(&self) -> u8 {
        match self {
            HeadingLevel::H1 => 1,
            HeadingLevel::H2 => 2,
            HeadingLevel::H3 => 3,
            HeadingLevel::H4 => 4,
            HeadingLevel::H5 => 5,
            HeadingLevel::H6 => 6,
        }
    }
}

pub enum Element {
    Heading(HeadingLevel, String),
    Paragraph(String),
    Chart(ChartDefinition),
}

#[derive(Default)]
pub struct Document {
    pub name: String,
    pub elements: Vec<Element>,
}
