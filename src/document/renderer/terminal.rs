use super::*;
use crate::plotting::get_chart_displayer;

pub fn render_document_to_terminal(document: &Document) -> anyhow::Result<()> {
    for element in &document.elements {
        match element {
            &Element::Heading(level, ref text) => {
                let hashes = "#".repeat(level.index() as usize);
                println!("{} {}", hashes, text);
            }
            Element::Paragraph(text) => {
                println!("{}", text);
            }
            Element::Chart(chart) => {
                get_chart_displayer().display(chart)?;
            }
        }
        println!();
    }
    Ok(())
}
