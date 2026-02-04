use nom::{
    branch::alt,
    bytes::complete::take_while1,
    character::complete::{char, digit1},
    combinator::opt,
    multi::{many1, separated_list1},
    sequence::delimited,
    IResult, Parser, // Import Parser trait to enable .parse()
};

#[derive(Debug, PartialEq, Clone)]
enum NodePart {
    Literal(String),
    Range(Vec<String>),
}

/// Parses a single item inside brackets, e.g., "01-05" or just "10"
/// Handles leading zeros (Slurm syntax: node[001-010] -> node001...node010)
fn parse_range_item(input: &str) -> IResult<&str, Vec<String>> {
    let (input, start_str) = digit1(input)?;
    
    let (input, maybe_dash) = opt(char('-')).parse(input)?;

    if maybe_dash.is_some() {
        let (input, end_str) = digit1(input)?;
        
        let start = start_str.parse::<u32>().unwrap_or(0);
        let end = end_str.parse::<u32>().unwrap_or(0);
        
        // Capture the width of the start string to preserve leading zeros
        let width = start_str.len();

        let range = (start..=end)
            .map(|n| format!("{:0width$}", n, width = width))
            .collect();
        Ok((input, range))
    } else {
        Ok((input, vec![start_str.to_string()]))
    }
}

/// Parses the contents inside brackets: "01-05,10,12-14"
fn parse_bracket_contents(input: &str) -> IResult<&str, Vec<String>> {
    // separated_list1 returns a Vec<Vec<String>>, so we flatten it
    let (input, lists) = separated_list1(char(','), parse_range_item)
        .parse(input)?;
    
    Ok((input, lists.into_iter().flatten().collect()))
}

/// Parses either a bracketed range "[...]" or a literal string "node"
fn parse_part(input: &str) -> IResult<&str, NodePart> {
    alt((
        // Case 1: Bracketed Range -> [01-05]
        delimited(char('['), parse_bracket_contents, char(']'))
            .map(NodePart::Range),
            
        // Case 2: Literal String -> node, rack, _blade, etc.
        // We accept alphanumeric, dashes, and underscores outside of brackets
        take_while1(|c: char| c.is_alphanumeric() || c == '-' || c == '_')
            .map(|s: &str| NodePart::Literal(s.to_string())),
    ))
    .parse(input)
}

/// Entry point: Parses a SLURM node string and returns the expanded list
/// e.g. "rack[1-2]_blade[1-2]"
pub fn parse_slurm_nodes(input: &str) -> Result<Option<Vec<String>>, String> {
    if input == "None assigned" {
        return Ok(None);
    }

    // Parse the input into a list of Parts
    let (remainder, parts) = many1(parse_part).parse(input)
        .map_err(|e| format!("Parsing error: {}", e))?;

    if !remainder.is_empty() {
        return Err(format!("Unparsed input remaining: {}", remainder));
    }

    // Expand the parts (Cartesian product logic)
    // We start with a single empty string and append parts to it
    let mut results = vec!["".to_string()];

    for part in parts {
        let mut new_results = Vec::new();
        match part {
            NodePart::Literal(s) => {
                // Append the literal to every current result
                for r in results {
                    new_results.push(format!("{}{}", r, s));
                }
            }
            NodePart::Range(variants) => {
                // Branch every current result for every variant in the range
                for r in results {
                    for v in variants.iter() {
                        new_results.push(format!("{}{}", r, v));
                    }
                }
            }
        }
        results = new_results;
    }

    Ok(Some(results))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_literal() {
        let input = "node01";
        let expected = vec!["node01"];
        assert_eq!(parse_slurm_nodes(input).unwrap().unwrap(), expected);
    }

    #[test]
    fn test_basic_range() {
        let input = "node[01-03]";
        let expected = vec!["node01", "node02", "node03"];
        assert_eq!(parse_slurm_nodes(input).unwrap().unwrap(), expected);
    }

    #[test]
    fn test_mixed_list_comma_separated() {
        let input = "node[1,3-5,10]";
        // Note: Slurm usually sorts numeric output, but our parser preserves input order
        // unless you explicitly sort it. The parser logic provided creates:
        let expected = vec!["node1", "node3", "node4", "node5", "node10"];
        assert_eq!(parse_slurm_nodes(input).unwrap().unwrap(), expected);
    }

    #[test]
    fn test_cartesian_product_multi_brackets() {
        // This tests logic like rack[1-2] combined with blade[01-02]
        let input = "rack[1-2]_blade[01-02]";
        let expected = vec![
            "rack1_blade01", "rack1_blade02",
            "rack2_blade01", "rack2_blade02"
        ];
        assert_eq!(parse_slurm_nodes(input).unwrap().unwrap(), expected);
    }

    #[test]
    fn test_leading_zeros_padding() {
        // Ensures 001 stays 001 and doesn't become 1
        let input = "cluster-[001-003]";
        let expected = vec!["cluster-001", "cluster-002", "cluster-003"];
        assert_eq!(parse_slurm_nodes(input).unwrap().unwrap(), expected);
    }

    #[test]
    fn test_complex_alphanumeric_prefix() {
        let input = "gpu-node-v1-[01-02]";
        let expected = vec!["gpu-node-v1-01", "gpu-node-v1-02"];
        assert_eq!(parse_slurm_nodes(input).unwrap().unwrap(), expected);
    }

    #[test]
    fn test_invalid_input() {
        // Test malformed input to ensure we get an Error, not a panic
        let input = "node[01-"; // Unclosed bracket
        assert!(parse_slurm_nodes(input).is_err());
    }

    #[test]
    fn test_none_assigned() {
        let input = "None assigned";
        assert_eq!(parse_slurm_nodes(input).unwrap(), None);
    }
}