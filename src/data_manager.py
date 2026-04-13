import pandas as pd
import numpy as np
import streamlit as st
from scipy import stats as sc_stats
from typing import Optional, Dict, Any, List, Tuple


class DataManager:
    """
    Handles data loading, cleaning, metadata, and all user-driven edits.
    Every mutating method returns (rows_affected, message) so the UI can report clearly.
    """

    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.original_data: Optional[pd.DataFrame] = None
        self.edit_log: List[str] = []

    # ──────────────────────────────────────────────────────────────
    # LOAD
    # ──────────────────────────────────────────────────────────────

    def load_data(self, uploaded_file) -> bool:
        try:
            ext = uploaded_file.name.rsplit('.', 1)[-1].lower()
            if ext == 'csv':
                self.data = pd.read_csv(uploaded_file)
            elif ext in ('xlsx', 'xls'):
                self.data = pd.read_excel(uploaded_file)
            else:
                st.error(f"Unsupported format: {ext}")
                return False
            self.original_data = self.data.copy()
            self.edit_log = []
            return True
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return False

    # ──────────────────────────────────────────────────────────────
    # AUTO-CLEAN ON LOAD
    # ──────────────────────────────────────────────────────────────

    def clean_data(self) -> pd.DataFrame:
        if self.data is None:
            return None
        self.cleaning_report = {
            'initial_rows': len(self.data),
            'initial_columns': len(self.data.columns),
            'duplicates_removed': 0,
            'values_filled': {},
            'type_conversions': [],
        }
        before = len(self.data)
        self.data = self.data.drop_duplicates()
        removed = before - len(self.data)
        self.cleaning_report['duplicates_removed'] = removed

        for col in self.data.columns:
            mb = self.data[col].isnull().sum()
            if self.data[col].dtype in ('float64', 'int64'):
                self.data[col] = self.data[col].ffill().bfill()
            else:
                mode = self.data[col].mode()
                if len(mode):
                    self.data[col] = self.data[col].fillna(mode[0])
            filled = mb - self.data[col].isnull().sum()
            if filled > 0:
                self.cleaning_report['values_filled'][col] = filled

        for col in self.data.columns:
            orig = str(self.data[col].dtype)
            try:
                self.data[col] = pd.to_numeric(self.data[col])
                new = str(self.data[col].dtype)
                if orig != new:
                    self.cleaning_report['type_conversions'].append(f"{col}: {orig} -> {new}")
            except (ValueError, TypeError):
                pass
        return self.data

    # ──────────────────────────────────────────────────────────────
    # EDITING — ROWS
    # ──────────────────────────────────────────────────────────────

    def remove_iqr_outliers(self, column: str) -> Tuple[int, str]:
        """Remove rows where `column` is an IQR outlier."""
        if self.data is None or column not in self.data.columns:
            return 0, "Column not found."
        Q1  = self.data[column].quantile(0.25)
        Q3  = self.data[column].quantile(0.75)
        IQR = Q3 - Q1
        mask   = (self.data[column] < Q1 - 1.5 * IQR) | (self.data[column] > Q3 + 1.5 * IQR)
        count  = int(mask.sum())
        before = len(self.data)
        self.data = self.data[~mask].reset_index(drop=True)
        msg = f"Removed {count} IQR-outlier rows from '{column}'. Rows: {before} -> {len(self.data)}."
        self.edit_log.append(msg)
        return count, msg

    def remove_zscore_anomalies(self, column: str, threshold: float = 3.0) -> Tuple[int, str]:
        """Remove rows where |z-score| > threshold for `column`."""
        if self.data is None or column not in self.data.columns:
            return 0, "Column not found."
        col_clean = self.data[column].dropna()
        z = np.abs(sc_stats.zscore(col_clean))
        bad_idx   = col_clean.index[z > threshold]
        count     = len(bad_idx)
        before    = len(self.data)
        self.data = self.data.drop(index=bad_idx).reset_index(drop=True)
        msg = f"Removed {count} anomalous rows (|z| > {threshold}) from '{column}'. Rows: {before} -> {len(self.data)}."
        self.edit_log.append(msg)
        return count, msg

    def remove_duplicates(self) -> Tuple[int, str]:
        """Remove all exact duplicate rows."""
        if self.data is None:
            return 0, "No data loaded."
        before = len(self.data)
        self.data = self.data.drop_duplicates().reset_index(drop=True)
        count = before - len(self.data)
        msg = f"Removed {count} duplicate rows. Rows: {before} -> {len(self.data)}."
        self.edit_log.append(msg)
        return count, msg

    def remove_missing_rows(self, column: Optional[str] = None) -> Tuple[int, str]:
        """Drop rows with any missing value, or only rows missing in `column`."""
        if self.data is None:
            return 0, "No data loaded."
        before = len(self.data)
        if column:
            self.data = self.data.dropna(subset=[column]).reset_index(drop=True)
            label = f"'{column}'"
        else:
            self.data = self.data.dropna().reset_index(drop=True)
            label = "any column"
        count = before - len(self.data)
        msg = f"Removed {count} rows with missing values in {label}. Rows: {before} -> {len(self.data)}."
        self.edit_log.append(msg)
        return count, msg

    def remove_rows_by_condition(self, column: str, operator: str, value: float) -> Tuple[int, str]:
        """
        Remove rows matching a condition: column {operator} value.
        operator: '<', '<=', '>', '>=', '==', '!='
        """
        if self.data is None or column not in self.data.columns:
            return 0, "Column not found."
        ops = {'<': '__lt__', '<=': '__le__', '>': '__gt__',
               '>=': '__ge__', '==': '__eq__', '!=': '__ne__'}
        if operator not in ops:
            return 0, f"Unknown operator: {operator}"
        before = len(self.data)
        mask   = getattr(self.data[column], ops[operator])(value)
        self.data = self.data[~mask].reset_index(drop=True)
        count = before - len(self.data)
        msg   = f"Removed {count} rows where {column} {operator} {value}. Rows: {before} -> {len(self.data)}."
        self.edit_log.append(msg)
        return count, msg

    # ──────────────────────────────────────────────────────────────
    # EDITING — MISSING VALUES IMPUTATION
    # ──────────────────────────────────────────────────────────────

    def fill_missing(self, column: str, method: str) -> Tuple[int, str]:
        """
        Fill missing values in `column`.
        method: 'mean' | 'median' | 'mode' | 'zero' | 'forward_fill' | 'backward_fill'
        """
        if self.data is None or column not in self.data.columns:
            return 0, "Column not found."
        count = int(self.data[column].isnull().sum())
        if count == 0:
            return 0, f"No missing values in '{column}'."
        if method == 'mean':
            val = self.data[column].mean()
            self.data[column] = self.data[column].fillna(val)
        elif method == 'median':
            val = self.data[column].median()
            self.data[column] = self.data[column].fillna(val)
        elif method == 'mode':
            val = self.data[column].mode().iloc[0]
            self.data[column] = self.data[column].fillna(val)
        elif method == 'zero':
            self.data[column] = self.data[column].fillna(0)
        elif method == 'forward_fill':
            self.data[column] = self.data[column].ffill()
        elif method == 'backward_fill':
            self.data[column] = self.data[column].bfill()
        else:
            return 0, f"Unknown method: {method}"
        remaining = int(self.data[column].isnull().sum())
        msg = f"Filled {count - remaining} missing values in '{column}' using {method}."
        self.edit_log.append(msg)
        return count - remaining, msg

    def fill_all_missing(self, method: str) -> Tuple[int, str]:
        """Apply fill_missing to every column with missing values."""
        if self.data is None:
            return 0, "No data loaded."
        total = 0
        for col in self.data.columns:
            if self.data[col].isnull().sum() > 0:
                n, _ = self.fill_missing(col, method)
                total += n
        msg = f"Filled {total} missing values across all columns using {method}."
        self.edit_log.append(msg)
        return total, msg

    # ──────────────────────────────────────────────────────────────
    # EDITING — COLUMNS
    # ──────────────────────────────────────────────────────────────

    def drop_column(self, column: str) -> Tuple[bool, str]:
        if self.data is None or column not in self.data.columns:
            return False, "Column not found."
        self.data = self.data.drop(columns=[column])
        msg = f"Dropped column '{column}'."
        self.edit_log.append(msg)
        return True, msg

    def rename_column(self, old_name: str, new_name: str) -> Tuple[bool, str]:
        if self.data is None or old_name not in self.data.columns:
            return False, "Column not found."
        if new_name.strip() == '':
            return False, "New name cannot be empty."
        self.data = self.data.rename(columns={old_name: new_name.strip()})
        msg = f"Renamed '{old_name}' to '{new_name.strip()}'."
        self.edit_log.append(msg)
        return True, msg

    def cast_column(self, column: str, dtype: str) -> Tuple[bool, str]:
        """Cast column to numeric, string, or datetime."""
        if self.data is None or column not in self.data.columns:
            return False, "Column not found."
        try:
            if dtype == 'numeric':
                self.data[column] = pd.to_numeric(self.data[column], errors='coerce')
            elif dtype == 'string':
                self.data[column] = self.data[column].astype(str)
            elif dtype == 'datetime':
                self.data[column] = pd.to_datetime(self.data[column], errors='coerce')
            msg = f"Cast '{column}' to {dtype}."
            self.edit_log.append(msg)
            return True, msg
        except Exception as e:
            return False, str(e)

    # ──────────────────────────────────────────────────────────────
    # RESET
    # ──────────────────────────────────────────────────────────────

    def reset_to_original(self) -> str:
        if self.original_data is None:
            return "No original data available."
        self.data = self.original_data.copy()
        self.edit_log.append("Reset to original dataset.")
        return f"Dataset reset to original ({len(self.data):,} rows, {len(self.data.columns)} columns)."

    # ──────────────────────────────────────────────────────────────
    # METADATA
    # ──────────────────────────────────────────────────────────────

    def identify_date_columns(self) -> List[str]:
        if self.data is None:
            return []
        date_cols = []
        for col in self.data.columns:
            dtype = self.data[col].dtype
            # Already a datetime column
            try:
                if np.issubdtype(dtype, np.datetime64):
                    date_cols.append(col)
                    continue
            except TypeError:
                pass
            # Try parsing string/object columns as dates
            if hasattr(dtype, 'name') and dtype.name in ('object', 'string'):
                try:
                    parsed = pd.to_datetime(self.data[col], errors='coerce')
                    if parsed.notna().sum() / max(len(self.data), 1) > 0.8:
                        date_cols.append(col)
                except (ValueError, TypeError):
                    continue
        return date_cols

    def get_cleaning_report(self) -> Optional[Dict[str, Any]]:
        if not hasattr(self, 'cleaning_report'):
            return None
        return self.cleaning_report

    def get_data_info(self) -> Dict[str, Any]:
        if self.data is None:
            return {}
        return {
            'rows':                 len(self.data),
            'columns':              len(self.data.columns),
            'column_names':         list(self.data.columns),
            'dtypes':               self.data.dtypes.to_dict(),
            'numeric_columns':      list(self.data.select_dtypes(include=[np.number]).columns),
            'categorical_columns':  list(self.data.select_dtypes(exclude=[np.number]).columns),
            'missing_values':       self.data.isnull().sum().to_dict(),
        }

    def get_missing_summary(self) -> pd.DataFrame:
        """Returns per-column missing value summary."""
        if self.data is None:
            return pd.DataFrame()
        rows = []
        for col in self.data.columns:
            missing = int(self.data[col].isnull().sum())
            rows.append({
                'Column':      col,
                'Type':        str(self.data[col].dtype),
                'Missing':     missing,
                'Missing (%)': round(missing / len(self.data) * 100, 2),
                'Complete':    len(self.data) - missing,
            })
        df = pd.DataFrame(rows).sort_values('Missing', ascending=False)
        return df[df['Missing'] > 0] if not df.empty else df

    def get_duplicate_rows(self) -> pd.DataFrame:
        """Returns all duplicate rows."""
        if self.data is None:
            return pd.DataFrame()
        return self.data[self.data.duplicated(keep='first')]
