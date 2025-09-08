use super::*;
use clap::ValueEnum;

mod pdf;
mod terminal;

#[derive(Debug, Clone, ValueEnum)]
pub enum Renderer {
    Terminal,
    Pdf,
}

impl Renderer {
    pub fn render(&self, document: &Document) -> anyhow::Result<()> {
        match self {
            Renderer::Terminal => terminal::render_document_to_terminal(document),
            Renderer::Pdf => pdf::render_document_to_pdf(document),
        }
    }
}
