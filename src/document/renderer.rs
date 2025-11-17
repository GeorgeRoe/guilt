use super::Document;

pub trait DocumentRenderer {
	fn render(&self, document: &Document) -> anyhow::Result<()>;
}