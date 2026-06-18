#=========================================================
# Metadata
#=========================================================

# Combine Excel Sheets to CSV
# v01.0 (2026-05-25)
# by Michael Rabenstein ((https://orcid.org/0000-0001-7712-224X))
#  Code written with the help of: Perplexity AI. (2025). Perplexity AI: AI-powered search engine. https://www.perplexity.ai

# This script merges different sheets of an Excel-Spreadsheet to a single CSV by column.
# Merged cells must first be unmerged in the Excel spreadsheet.

#=========================================================
# Code
#=========================================================

library(readxl)
library(dplyr)

excel_file <- "/Users/MichaelR/Sciebo/Projekte/IDM/Zertifikatskurs-FDM/Modul10/Data/01_TransformDataforREDCapImport_Cleaned.xlsx"
output_csv <- "/Users/MichaelR/Sciebo/Projekte/IDM/Zertifikatskurs-FDM/Modul10/Data/02_TransformDataforREDCapImport_Stitched.csv"
n_rows <- 201 # Number of data rows + header row. Prevent conflicts if additional (empty) rows are imported from a sheet. 

# Get sheetnames
sheets <- excel_sheets(excel_file)

# A helper function to determine the column types for each sheet: is it a date field?
guess_col_types <- function(sheetname, n = 10) {
  # Dummy reading to guess types
  pre <- read_excel(excel_file, sheet = sheetname, n_max = n, guess_max = n, col_names = TRUE)
  sapply(pre, function(v) if (inherits(v, c("Date", "POSIXct", "POSIXlt"))) "date" else "text")
}

sheet_list <- lapply(sheets, function(sh) {
  col_types <- guess_col_types(sh)
  # Explicitly set column types (text, except for date fields found)
  df <- read_excel(excel_file, sheet = sh, col_types = unname(col_types), guess_max = 2000, col_names = TRUE)
  df <- df[seq_len(min(n_rows, nrow(df))), , drop=FALSE]
  return(df)
})

# Merge by column
result <- bind_cols(sheet_list)

# Replace line breaks with “; ”
replace_linebreaks <- function(x) {
  if (is.character(x)) return(gsub("\\r?\\n|\\r", "; ", x)) else return(x)
}
result[] <- lapply(result, replace_linebreaks)

# Export
write.table(result,
            file = output_csv,
            sep = "|",
            row.names = FALSE,
            col.names = TRUE,
            quote = TRUE,
            qmethod = "double",
            na = ""
)
