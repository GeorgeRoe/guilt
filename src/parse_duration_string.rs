use chrono::Duration;

pub fn parse_duration_string(time_str: &str) -> Result<Duration, String> {
    let (days, time_part) = if let Some((days_part, rest)) = time_str.split_once('-') {
        let days = days_part
            .parse::<i64>()
            .map_err(|_| format!("Invalid days part: {}", days_part))?;
        (days, rest)
    } else {
        (0, time_str)
    };

    let parts: Vec<&str> = time_part.split(':').collect();

    // from the slurm sbatch docs:
    // 'Acceptable time formats include "minutes", "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes" and "days-hours:minutes:seconds".'
    let (hours, minutes, seconds) = match parts.len() {
        1 => (
            0,
            parts[0]
                .parse::<i64>()
                .map_err(|_| format!("Invalid minutes: {}", parts[0]))?,
            0,
        ),
        2 => {
            if days > 0 {
                let hours = parts[0]
                    .parse::<i64>()
                    .map_err(|_| format!("Invalid hours: {}", parts[0]))?;

                let minutes = parts[1]
                    .parse::<i64>()
                    .map_err(|_| format!("Invalid minutes: {}", parts[1]))?;
                (hours, minutes, 0)
            } else {
                let minutes = parts[0]
                    .parse::<i64>()
                    .map_err(|_| format!("Invalid minutes: {}", parts[0]))?;
                let seconds = parts[1]
                    .parse::<i64>()
                    .map_err(|_| format!("Invalid seconds: {}", parts[1]))?;
                (0, minutes, seconds)
            }
        }
        3 => {
            let hours = parts[0]
                .parse::<i64>()
                .map_err(|_| format!("Invalid hours: {}", parts[0]))?;
            let minutes = parts[1]
                .parse::<i64>()
                .map_err(|_| format!("Invalid minutes: {}", parts[1]))?;
            let seconds = parts[2]
                .parse::<i64>()
                .map_err(|_| format!("Invalid seconds: {}", parts[2]))?;
            (hours, minutes, seconds)
        }
        _ => return Err(format!("Invalid time format: {}", time_str)),
    };

    let dur = Duration::days(days)
        + Duration::hours(hours)
        + Duration::minutes(minutes)
        + Duration::seconds(seconds);

    Ok(dur)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_format() {
        let cases = [
            ("45", Duration::minutes(45)),
            ("2:30", Duration::minutes(2) + Duration::seconds(30)),
            ("1:15:20", Duration::hours(1) + Duration::minutes(15) + Duration::seconds(20)),
            ("3-04:20:10", Duration::days(3) + Duration::hours(4) + Duration::minutes(20) + Duration::seconds(10)),
            ("5-12:00", Duration::days(5) + Duration::hours(12)),
        ];

        for (input, expected) in cases {
            let result = parse_duration_string(input).unwrap();
            assert_eq!(result, expected, "input = {input}");
        }
    }

    #[test]
    fn test_invalid_format() {
        let result = parse_duration_string("1-2:3:4:5");

        assert!(result.is_err());
    }
}
