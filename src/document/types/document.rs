use super::Element;

#[derive(Default)]
pub struct Document {
    pub name: String,
    pub elements: Vec<Element>,
}