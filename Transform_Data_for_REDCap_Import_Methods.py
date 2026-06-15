# Methods used in Transform-Data-for-REDCap-Import.ipynb
"""
V01 (2026-05-25)
by Michael Rabenstein (https://orcid.org/0000-0001-7712-224X)
Code written with the help of: Perplexity AI. (2025). Perplexity AI: AI-powered search engine. https://www.perplexity.ai
and
UKB‑GPT (2026-02-17; institutional LLM based on openai/gpt-oss-120b (OpenAI et al. (2025). gpt-oss-120b & gpt-oss-20b Model Card. arXiv. https://doi.org/10.48550/arXiv.2508.10925))

This modul contains the functions used in the Jupyter Notebook 'Transform-Data-for-REDCap-Import.ipynb'. 
"""
# import packages
import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, date, time
import re
import traceback

# Check if field is empty
def is_empty(val):
    if val is None:
        return True
    if pd.isna(val):
        return True
    if isinstance(val, str) and val.strip() == '':
        return True
    return False

# Dynamically generate filetypes for the dialog
def build_filetypes(ext_list):
    # Create a pattern string like "*.csv *.tsv *.txt *.xls *.xlsx"
    pattern = ' '.join(f'*{ext}' for ext in ext_list)
    # Create a user-friendly label
    label = "Supported files"
    # Build the filetypes list for askopenfilename
    filetypes = [(label, pattern)]
    # Optionally, add each extension separately
    for ext in ext_list:
        filetypes.append((f"{ext.upper()} files", f"*{ext}"))
    filetypes.append(("All files", "*.*"))
    return filetypes

# --- Helper function for data import ---
def read_datatable(path, delimiter):
    """
    Reads a table as a pandas DataFrame, automatically handling CSV (with configurable delimiter) and Excel files.
    All columns are read as text (dtype=str).
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.csv', '.tsv', '.txt']:
        return pd.read_csv(path, dtype=str, sep=delimiter)
    elif ext in ['.xls', '.xlsx']:
        return pd.read_excel(path, dtype=str)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

# --- Helper function for date conversion ---
def parse_date(val, dateformat_source,output_type):
    if is_empty(val):
        return "emptyValue"
    dateformat_output = '%d/%m/%Y'
    try:
        if val is None:
            return val
        if pd.isna(val):
            return val
        if isinstance(val, (float, int)) and pd.isna(val):
            # NaN (float) aus pandas
            return val
        try:
            dt = _as_datetime(val, dateformat_source)
        except Exception:
            # Hier kann man sehr detailliert loggen; wir geben einfach error zurück
            print("Fehler beim Parsen von:", val)
            print(traceback.format_exc())
            return "errorVal"
        
        if output_type == 1:
            return dt.strftime(dateformat_output)

        if output_type == 2:
            return dt.strftime(f"{dateformat_output} %H:%M")

        if output_type == 3:
            return dt.strftime(f"{dateformat_output} %H:%M:%S")

        # unbekannter output_type
        return "errorVal"

    except Exception:
        print(val)
        #traceback.print_exc()
        stacktrace_str = traceback.format_exc()
        print(stacktrace_str)
        return "errorVal"
        
# --- Helper function for date conversion ---
def _as_datetime(val, dateformat_source):
    """
    Attempts to convert `val` to a datetime object.
    - If `val` is already a datetime or timestamp → returns it unchanged.
    - If `val` is a date or time → fills in the missing parts with default values.
    - Otherwise, the string is parsed using `datetime.strptime`.
    """
    # 1.) Already a datetime object??
    if isinstance(val, (datetime, pd.Timestamp)):
        return pd.Timestamp(val).to_pydatetime()   # Normalisiere zu python datetime

    # 2.) Only one date object → add time with 00:00:00
    if isinstance(val, date) and not isinstance(val, datetime):
        return datetime.combine(val, time.min)

    # 3.) Just a time object → combine with a dummy date (e.g., 1900-01-01)
    if isinstance(val, time):
        return datetime.combine(date(1900, 1, 1), val)

    # 4.) String – Preprocess (dots → hyphens)
    val_mod = str(val).replace('.', '-').strip()
    # If `dateformat_source` does not yet contain a time component but the string includes a time portion,
    # we automatically expand `dateformat_source`.
    # Example: dateformat_source = "%d-%m-%Y", val = "19-02-2024 13:45"
    if any(sep in val_mod for sep in (' ', 'T')) and '%H' not in dateformat_source:
        # Check if there are seconds
        if ':' in val_mod.split()[-1]:
            # "HH:MM[:SS]" → Determine whether seconds are included
            time_part = val_mod.split()[-1]
            if time_part.count(':') == 2:
                dateformat_source += ' %H:%M:%S'
            else:
                dateformat_source += ' %H:%M'

    return datetime.strptime(val_mod, dateformat_source)

# --- Helper function to check if email address has a valid structure ---
def validate_email(val):
    """
    Checks if the input string is a valid email address.
    Returns the original value if valid, otherwise 'errorVal'.
    """
    if is_empty(val):
        return "emptyValue"
    if is_empty(val):
        return val
    email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if isinstance(val, str) and re.match(email_regex, val):
        return val
    else:
        return "errorVal"


# --- Helper function to check if german PLZ address is valid ---
def validate_postal_ger(val):
    """
    Checks if the input is a valid German postal code (5-digit integer).
    Returns the original value if valid, otherwise 'errorVal'.
    """
    if is_empty(val):
        return "emptyValue"
    if is_empty(val):
        return val
    if isinstance(val, str) and val.isdigit() and len(val) == 5:
        return val
    else:
        return "errorVal"

# --- Helper functions to check if time formats are  valid ---
def validate_time(val):
    """
    Checks if the input is a valid time in HH:MM format.
    Returns the original value if valid, otherwise 'errorVal'.
    """
    if is_empty(val):
        return "emptyValue"
    if is_empty(val):
        return val
    try:
        if isinstance(val, str):
            datetime.strptime(val, '%H:%M')
            return val
        else:
            return "errorVal"
    except Exception:
        return "errorVal"

def validate_time_sec(val):
    """
    Checks if the input is a valid time in HH:MM:SS format.
    Returns the original value if valid, otherwise 'errorVal'.
    """
    if is_empty(val):
        return ""
    if is_empty(val):
        return val
    try:
        if isinstance(val, str):
            datetime.strptime(val, '%H:%M:%S')
            return val
        else:
            return "errorVal"
    except Exception:
        return "errorVal"

# --- Function to extract valid choices from choices string ---
def extract_choices(choices_str):
    if pd.isna(choices_str) or not isinstance(choices_str, str):
        return []
    # Split by |, then take the part before the first comma in each choice
    choices = []
    for part in choices_str.split('|'):
        part = part.strip()
        if ',' in part:
            value = part.split(',')[0].strip()
            choices.append(value)
        elif part:  # in case there's a value without a comma
            choices.append(part.strip())
    return choices

# --- Main transformation logic based on field_type ---
def process_column_by_field_type(
    df, var_name, format_str, field_type, choices_str, min_val, max_val, out_of_range_log, dateformat_source
):
    if field_type == 'text':
        # Standard transformation for text fields
        df[var_name] = transform_column(
            df[var_name], format_str, var_name, min_val, max_val, out_of_range_log, dateformat_source
        )
    elif field_type in ['dropdown', 'radio']:
        # Validate against possible choices
        valid_choices = extract_choices(choices_str)
        def check_choice(val):
            if is_empty(val):  # Do not check empty value
                return "emptyValue"
            #if pd.isna(val) or val == "":
                #return val
            if val in valid_choices:
                return val
            else:
                return "errorVal"
        df[var_name] = df[var_name].apply(check_choice)
    elif field_type == 'checkbox':
        # Find all columns starting with var_name + '___'
        checkbox_cols = [col for col in df.columns if col.startswith(var_name + '___')]
        for col in checkbox_cols:
            def check_checkbox(val):
                if is_empty(val):  # Do not check empty value
                    return "emptyValue"
                #if pd.isna(val) or val == "":
                    #return val
                if val in ['0', '1']:
                    return val
                else:
                    return "errorVal"
            df[col] = df[col].apply(check_checkbox)
    elif field_type in ['yesno', 'truefalse']:
        def check_binary(val):
            if is_empty(val):  # Do not check empty value
                return "emptyValue"
            #if pd.isna(val) or val == "":
                #return val
            if val in ['0', '1']:
                return val
            else:
                return "errorVal"
        df[var_name] = df[var_name].apply(check_binary)
    elif field_type == 'slider':
        def check_slider(val):
            if is_empty(val):  # Do not check empty value
                return "emptyValue"
            #if pd.isna(val) or val == "":
                #return val
            try:
                ival = int(val)
                return str(ival)
            except:
                return "errorVal"
        df[var_name] = df[var_name].apply(check_slider)
    elif field_type == 'notes':
        # Keep value as is
        pass
    else:
        # If field_type is unknown, keep value as is
        pass

def parse_min_max(val, default):
    if pd.isna(val) or val == "":
        return default
    try:
    # Replace the comma with a period, then convert to a float
        return float(str(val).replace(',', '.'))
    except Exception:
        return default

def transform_column(series, format_str, var_name, min_val, max_val, out_of_range_log, dateformat_source):
    # Helper function for robust parsing of min and max
    def parse_min_max(val, default):
        if pd.isna(val) or val == "":
            return default
        try:
            return float(str(val).replace(',', '.'))
        except Exception:
            return default

    # Blank value detection
    def is_empty(val):
        return pd.isna(val) or (isinstance(val, str) and val.strip() == "")

    # Handling of number formats
    if format_str in ('integer', 'number', 'number_1dp_comma_decimal', 'number_1dp', 'number_2dp_comma_decimal', 'number_2dp', 'number_3dp_comma_decimal', 'number_3dp'):
        # Conversion to float with blank value handling
        def to_num(val):
            if is_empty(val):
                return np.nan
            try:
                return float(str(val).replace(",", "."))
            except Exception:
                return np.nan

        num_series = series.apply(to_num)

        # Detection of invalid values (not blank, but not a valid float)
        error_mask = num_series.isna() & ~series.isna() & (series.astype(str).str.strip() != "")

        # Set the number of decimal places
        if format_str == 'integer':
            decimals = 0
        elif format_str in ('number_1dp_comma_decimal', 'number_1dp'):
            decimals = 1
        elif format_str in ('number_2dp_comma_decimal', 'number_2dp'):
            decimals = 2
        elif format_str in ('number_3dp_comma_decimal', 'number_3dp'):
            decimals = 3
        else:
            decimals = -1  # No rounding

        # Parse min/max values
        min_num = parse_min_max(min_val, -np.inf)
        max_num = parse_min_max(max_val, np.inf)

        # Rounding numbers
        if decimals == -1:
            rounded_num_series = num_series
        else:
            rounded_num_series = num_series.round(decimals)

        # Check for values outside the min-max limits
        out_of_range_mask = ~error_mask & ((rounded_num_series < min_num) | (rounded_num_series > max_num))

        # Logging values outside the permissible ranges
        for idx in series.index[out_of_range_mask]:
            out_of_range_log.append({
                'variable': var_name,
                'value': series.loc[idx],
                'index': idx,
                'min value': min_num,
                'max value': max_num
            })

        # Formatted output with handling of emptyValue and errorVal
        def format_result(x, original_val):
            if is_empty(original_val):
                return "emptyValue"  # Output null values as “emptyValue”
            if pd.isna(x):
                return "errorVal"   # Mark invalid values as “errorVal”
            # Format according to the number of decimal places
            if decimals == 0:
                return str(int(x))
            elif decimals > 0:
                # Output with decimal place(s)
                fmt = f"{{:.{decimals}f}}"
                return fmt.format(x)
            else:
                return str(x)

        # Result as a series
        result = pd.Series([
            format_result(x, orig) for x, orig in zip(rounded_num_series, series)
        ], index=series.index)

        # Explicitly mark erroneous values with “errorVal” (for non-empty fields)
        result[error_mask] = "errorVal"

        # For formats that use a comma as the decimal separator, replace the period with a comma
        if format_str in ('number_1dp_comma_decimal', 'number_2dp_comma_decimal'):
            result = result.str.replace('.', ',', regex=False)

        return result

    # Date/time fields (delegated to parse_date)
    elif format_str in ('date_dmy', 'date_mdy', 'date_ymd'):
        return series.apply(parse_date, args=(dateformat_source, 1))
    elif format_str in ('datetime_dmy', 'datetime_mdy', 'datetime_ymd'):
        return series.apply(parse_date, args=(dateformat_source, 2))
    elif format_str in ('datetime_seconds_dmy', 'datetime_seconds_mdy', 'datetime_seconds_ymd'):
        return series.apply(parse_date, args=(dateformat_source, 3))

    # Email field with validation
    elif format_str == 'email':
        return series.apply(validate_email)

    # Time fields with validation
    elif format_str == 'time':
        return series.apply(validate_time)
    elif format_str == 'time_hh_mm_ss':
        return series.apply(validate_time_sec)

    else:
        # No transformation for unknown or “text” formats
        return series

if __name__ == "__main__":
    print("This file contains functions for a Jupyter Notebook.")