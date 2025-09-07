use super::*;
use clap::ValueEnum;

mod terminal;

#[derive(Debug, Clone, ValueEnum)]
pub enum Renderer {
    Terminal
}

impl Renderer {
    pub fn render(&self, document: &Document) -> anyhow::Result<()> {
        match self {
            Renderer::Terminal => Ok(terminal::render_document_to_terminal(document)),
        }
    }
}