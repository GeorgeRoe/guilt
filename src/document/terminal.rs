use super::*;
use crate::plotting::get_chart_displayer;

pub struct TerminalDocumentRenderer;

impl DocumentRenderer for TerminalDocumentRenderer {
    fn render(&self, document: &Document) -> anyhow::Result<()> {
        for element in &document.elements {
            match element {
                Element::Heading(level, text) => {
                    let hashes = "#".repeat(level.index() as usize);
                    println!("{} {}", hashes, text);
                },
                Element::Paragraph(text) => {
                    println!("{}", text);
                },
                Element::Chart(chart) => {
                    get_chart_displayer().display(chart)?;
                }
            }
        }

        Ok(())
    }
}