mod types;
pub use types::*;

mod renderer;
pub use renderer::DocumentRenderer;

pub mod pdf;

pub mod terminal;

#[derive(clap::ValueEnum, Clone)]
pub enum DocumentRendererType {
    Pdf,
    Terminal,
}

impl DocumentRendererType {
    pub fn get_renderer(&self) -> Box<dyn DocumentRenderer> {
        match self {
            DocumentRendererType::Pdf => Box::new(pdf::PdfDocumentRenderer {}),
            DocumentRendererType::Terminal => Box::new(terminal::TerminalDocumentRenderer {}),
        }
    }
}
