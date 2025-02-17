use std::{fs::read_to_string, path::PathBuf};

pub fn read_migrate_file(file: PathBuf) -> anyhow::Result<Vec<(PathBuf, PathBuf)>> {
    let contents = read_to_string(file)?;
    let lines: Vec<String> = contents
        .split('\n')
        .map(|x| x.to_owned())
        .filter(|x| x != "")
        .collect();
    let migrations = lines
        .iter()
        .filter_map(|x| x.split_once(" -> "))
        .map(|x| {
            (
                x.0.parse().expect("a valid path"),
                x.1.parse().expect("a valid path"),
            )
        })
        .collect::<Vec<_>>();
    Ok(migrations)
}
