mod plotter;
pub use plotter::Plotter;

mod kitty_plotter;
pub use kitty_plotter::KittyPlotter;

mod terminal_plotter;
pub use terminal_plotter::TerminalPlotter;

pub fn get_plotter() -> Box<dyn Plotter> {
    if std::env::var("TERM") == Ok("xterm-kitty".to_string()) {
        Box::new(KittyPlotter::new())
    } else {
        Box::new(TerminalPlotter)
    }
}