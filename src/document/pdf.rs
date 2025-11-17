use super::*;
use crate::plotting::image::{Resolution, render};
use charts_rs::DEFAULT_FONT_DATA;
use genpdf;
use genpdf::fonts::{FontData, FontFamily};

static RESOLUTION: Resolution = Resolution {
    width: 1600,
    height: 1200,
};

fn get_heading_font_size(level: &HeadingLevel) -> u8 {
    match level {
        HeadingLevel::H1 => 32,
        HeadingLevel::H2 => 24,
        HeadingLevel::H3 => 18,
        HeadingLevel::H4 => 16,
        HeadingLevel::H5 => 14,
        HeadingLevel::H6 => 12,
    }
}

pub fn render_document_to_pdf(document: &Document) -> anyhow::Result<()> {
    let font_data = FontData::new(DEFAULT_FONT_DATA.to_vec(), None)?;
    let font_family = FontFamily {
        regular: font_data.clone(),
        bold: font_data.clone(),
        italic: font_data.clone(),
        bold_italic: font_data,
    };

    let mut doc = genpdf::Document::new(font_family);

    doc.set_title(&document.name);
    let mut decorator = genpdf::SimplePageDecorator::new();
    decorator.set_margins(10);
    doc.set_page_decorator(decorator);

    for element in &document.elements {
        match element {
            Element::Heading(level, text) => {
                let mut paragraph = genpdf::elements::Paragraph::new("");
                paragraph.push_styled(
                    text.clone(),
                    genpdf::style::Style::new().with_font_size(get_heading_font_size(level)),
                );
                doc.push(paragraph);
            }
            Element::Paragraph(text) => {
                let paragraph = genpdf::elements::Paragraph::new(text.clone());
                doc.push(paragraph);
            }
            Element::Chart(chart) => {
                let image_data = render(chart, &RESOLUTION)?.to_rgb8();
                let img = genpdf::elements::Image::from_dynamic_image(
                    image::DynamicImage::ImageRgb8(image_data),
                )?
                .with_alignment(genpdf::Alignment::Center);
                doc.push(img);
            }
        }
        doc.push(genpdf::elements::Break::new(1));
    }

    Ok(doc.render_to_file(format!("{}.pdf", document.name))?)
}

pub struct PdfDocumentRenderer;

impl DocumentRenderer for PdfDocumentRenderer {
    fn render(&self, document: &Document) -> anyhow::Result<()> {
        render_document_to_pdf(document)
    }
}