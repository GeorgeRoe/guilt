use nom::{
    branch::alt,
    bytes::complete::{tag, take_while1},
    character::complete::digit1,
    combinator::{map, opt},
    multi::separated_list1,
    sequence::{delimited, preceded},
    IResult,
    Parser
};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "lowercase")]
pub enum Constraint {
    Feature(String),
    Count(Box<Constraint>, i32),
    And(Vec<Constraint>),
    Or(Vec<Constraint>),
    MatchingOr(Vec<Constraint>),
}

impl Constraint {
    pub fn from_str(input: &str) -> Result<Self, String> {
        let (_, result) = parse_expression(input).map_err(|e| format!("Parsing error: {}", e))?;
        Ok(result)
    }
}

// --- Parsers ---

/// Parses a feature name.
/// Slurm features are alphanumeric, but can include '-' and '_'.
fn parse_feature_name(input: &str) -> IResult<&str, Constraint> {
    let (input, name) = take_while1(|c: char| c.is_alphanumeric() || c == '_' || c == '-')(input)?;
    Ok((input, Constraint::Feature(name.to_string())))
}

/// Handles grouped expressions:
fn parse_group(input: &str) -> IResult<&str, Constraint> {
    alt((
        // ( ... ) -> Standard grouping
        delimited(
            tag("("),
            parse_expression,
            tag(")")
        ),
        // [ ... ] -> Matching OR (or generic container)
        map(
            delimited(
                tag("["),
                separated_list1(tag("|"), parse_and),
                tag("]")
            ),
            Constraint::MatchingOr
        ),
    )).parse(input)
}

/// Handles the optional node count suffix: feature*count
/// Precedence: * binds tighter than &
fn parse_atom(input: &str) -> IResult<&str, Constraint> {
    let (input, inner) = alt((parse_group, parse_feature_name)).parse(input)?;
    
    // Check for optional '*count' suffix
    let (input, count) = opt(preceded(tag("*"), digit1)).parse(input)?;

    if let Some(c_str) = count {
        let c = c_str.parse::<i32>().unwrap_or(1);
        Ok((input, Constraint::Count(Box::new(inner), c)))
    } else {
        Ok((input, inner))
    }
}

/// Level 2: AND logic (&)
/// Precedence: & binds tighter than |
fn parse_and(input: &str) -> IResult<&str, Constraint> {
    let (input, mut list) = separated_list1(tag("&"), parse_atom).parse(input)?;
    
    if list.len() == 1 {
        Ok((input, list.pop().unwrap()))
    } else {
        Ok((input, Constraint::And(list)))
    }
}

/// Level 1: OR logic (|)
/// Lowest precedence
fn parse_expression(input: &str) -> IResult<&str, Constraint> {
    let (input, mut list) = separated_list1(tag("|"), parse_and).parse(input)?;
    
    if list.len() == 1 {
        Ok((input, list.pop().unwrap()))
    } else {
        Ok((input, Constraint::Or(list)))
    }
}

// --- Tests ---

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_feature() {
        let input = "intel";
        let expected = Constraint::Feature("intel".to_string());
        assert_eq!(Constraint::from_str(input).unwrap(), expected);
    }

    #[test]
    fn test_feature_with_special_chars() {
        let input = "gpu_v100-node";
        let expected = Constraint::Feature("gpu_v100-node".to_string());
        assert_eq!(Constraint::from_str(input).unwrap(), expected);
    }

    #[test]
    fn test_node_count() {
        let input = "intel*4";
        let expected = Constraint::Count(Box::new(Constraint::Feature("intel".to_string())), 4);
        assert_eq!(Constraint::from_str(input).unwrap(), expected);
    }

    #[test]
    fn test_and_precedence() {
        // intel&gpu should create an And block
        let input = "intel&gpu";
        let result = Constraint::from_str(input).unwrap();
        if let Constraint::And(list) = result {
            assert_eq!(list.len(), 2);
            assert_eq!(list[0], Constraint::Feature("intel".to_string()));
            assert_eq!(list[1], Constraint::Feature("gpu".to_string()));
        } else {
            panic!("Expected And block, found {:?}", result);
        }
    }

    #[test]
    fn test_or_precedence() {
        let input = "intel|amd";
        let result = Constraint::from_str(input).unwrap();
        assert!(matches!(result, Constraint::Or(_)));
    }

    #[test]
    fn test_complex_precedence() {
        // Logic: (foo AND bar) OR baz
        // In Slurm, & binds tighter than |
        let input = "foo&bar|baz";
        let result = Constraint::from_str(input).unwrap();
        
        if let Constraint::Or(list) = result {
            assert_eq!(list.len(), 2);
            assert!(matches!(list[0], Constraint::And(_)));
            assert!(matches!(list[1], Constraint::Feature(_)));
        } else {
            panic!("Operator precedence failed: | should be the top-level node");
        }
    }

    #[test]
    fn test_parentheses() {
        // Logic: foo AND (bar OR baz)
        let input = "foo&(bar|baz)";
        let result = Constraint::from_str(input).unwrap();
        
        if let Constraint::And(list) = result {
            assert_eq!(list.len(), 2);
            assert_eq!(list[0], Constraint::Feature("foo".to_string()));
            assert!(matches!(list[1], Constraint::Or(_)));
        } else {
            panic!("Parentheses failed to override precedence");
        }
    }

    #[test]
    fn test_matching_or_brackets() {
        // This checks the logic of [a|b|c] parsing into MatchingOr(vec![a, b, c])
        let input = "[rack1|rack2|rack3]";
        let result = Constraint::from_str(input).unwrap();
        
        if let Constraint::MatchingOr(list) = result {
            assert_eq!(list.len(), 3);
            assert_eq!(list[0], Constraint::Feature("rack1".to_string()));
            assert_eq!(list[1], Constraint::Feature("rack2".to_string()));
            assert_eq!(list[2], Constraint::Feature("rack3".to_string()));
        } else {
            panic!("Expected MatchingOr for square brackets with 3 elements, found: {:?}", result);
        }
    }

    #[test]
    fn test_nested_complex_slurm_example() {
        // Example from Slurm docs: [(rack1|rack2)*1&(rack3)*2]
        // This is a "Multiple Count" example.
        let input = "[(rack1|rack2)*1&(rack3)*2]";
        let result = Constraint::from_str(input).unwrap();
        
        // The parser logic for brackets is: separated_list1(tag("|"), parse_and)
        // Since there is no '|' at the top level inside the brackets here, 
        // it parses the whole inner string as a single `Constraint::And`.
        // So we get MatchingOr( vec![ And(...) ] ) -> Length 1.
        
        if let Constraint::MatchingOr(outer_list) = result {
            assert_eq!(outer_list.len(), 1, "Should contain 1 complex expression");
            
            // Inside is an And (&)
            if let Constraint::And(and_list) = &outer_list[0] {
                // First part is a Count (*) of an Or (|)
                if let Constraint::Count(inner, count) = &and_list[0] {
                    assert_eq!(*count, 1);
                    assert!(matches!(**inner, Constraint::Or(_)));
                } else {
                    panic!("Inner count failed");
                }
            } else {
                panic!("Inner And failed");
            }
        } else {
            panic!("Outer MatchingOr failed");
        }
    }

    #[test]
    fn test_whitespace_rejection() {
        // Confirm that whitespace is NOT allowed
        let input = "( intel & gpu )";
        let result = Constraint::from_str(input);
        assert!(result.is_err(), "Parser should REJECT spaces");
    }

    #[test]
    fn test_invalid_input() {
        let input = "!!!";
        let result = Constraint::from_str(input);
        assert!(result.is_err());
    }

    #[test]
    fn test_empty_input() {
        let input = "";
        let result = Constraint::from_str(input);
        assert!(result.is_err());
    }
}