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