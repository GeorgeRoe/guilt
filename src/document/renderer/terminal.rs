use super::*;

pub fn render_document_to_terminal(document: &Document) -> () {
    for element in &document.elements {
        match element {
            &Element::Heading(level, ref text) => {
                let hashes = "#".repeat(level.index() as usize);
                println!("{} {}", hashes, text);
            }

            &Element::Paragraph(ref text) => {
                println!("{}", text);
            }
        }
        println!();
    }

}