# Parses EngineeringTechnology_StatewideInventory.csv and outputs SQL INSERT statements
# for TaxonomyCourses. Only includes courses offered by at least one institution.
# Run from the Specifications directory.

$csvPath = "$PSScriptRoot\EngineeringTechnology_StatewideInventory.csv"
$outputPath = "$PSScriptRoot\seed_courses.sql"

# Known prefix → Level3Key mappings (must match taxonomy nodes in taxonomy.json)
$validPrefixes = @(
    'CET','EEL','EER','EET','EEV','EST','ETC','ETD','ETG','ETI','ETM','ETP','ETS','TDR'
)

$seen = @{}
$inserts = [System.Collections.Generic.List[string]]::new()

$lines = [System.IO.File]::ReadAllLines($csvPath)

foreach ($line in $lines) {
    $cols = $line -split ','

    # Need at least 12 columns
    if ($cols.Count -lt 12) { continue }

    $institution = $cols[1].Trim()
    $courseRaw   = $cols[3].Trim()
    $title       = $cols[6].Trim()
    $credits     = $cols[11].Trim()

    # Skip rows with no institution (not offered anywhere)
    if ([string]::IsNullOrWhiteSpace($institution)) { continue }

    # Course number must match pattern: 3 letters + space + digits + optional letter(s)
    if ($courseRaw -notmatch '^([A-Z]{2,3})\s+(\d{3,4}[A-Z]?)$') { continue }

    $prefix   = $Matches[1]
    $courseId = ($courseRaw -replace '\s+', '')  # e.g. "EET 1084C" -> "EET1084C"

    # Only include prefixes in our taxonomy
    if ($prefix -notin $validPrefixes) { continue }

    # Skip if already seen
    if ($seen.ContainsKey($courseId)) { continue }
    $seen[$courseId] = $true

    # Normalize title
    $title = if ([string]::IsNullOrWhiteSpace($title)) { $courseId } else { $title.Trim('"') }
    $title = $title -replace "'", "''"  # escape single quotes for SQL

    # Parse credit hours (take first number found)
    $creditHours = 'NULL'
    if ($credits -match '(\d+(\.\d+)?)') {
        $creditHours = [int][Math]::Round([double]$Matches[1])
    }

    $inserts.Add("INSERT OR IGNORE INTO TaxonomyCourses (CourseId, Level3Key, Title, CreditHours, IsActive) VALUES ('$courseId', '$prefix', '$title', $creditHours, 1);")
}

$output = @"
-- Auto-generated from EngineeringTechnology_StatewideInventory.csv
-- Only courses with at least one institution offering are included.
-- Run: sqlite3 /var/presemaker-repo/data/repo.db < seed_courses.sql

$($inserts -join "`n")
"@

[System.IO.File]::WriteAllText($outputPath, $output)

Write-Host "Generated $($inserts.Count) course INSERT statements -> $outputPath"
