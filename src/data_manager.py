import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional, Dict, Any, List

class DataManager:
    """
    Handles data loading, cleaning, and basic metadata.
    """
    
    def __init__(self):
        """Initialize the DataManager with empty dataframe."""
        self.data: Optional[pd.DataFrame] = None
        self.original_data: Optional[pd.DataFrame] = None
        
    def load_data(self, uploaded_file) -> bool:
        """
        Load data from CSV or Excel file.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Determine file type and load accordingly
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                self.data = pd.read_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                self.data = pd.read_excel(uploaded_file)
            else:
                st.error(f"Unsupported file format: {file_extension}")
                return False
            
            # Store original data for reference
            self.original_data = self.data.copy()
            return True
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return False
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean the loaded dataset.
        
        Performs the following operations:
        - Removes duplicate rows
        - Handles missing values (forward fill for numeric, mode for categorical)
        - Converts appropriate columns to numeric types
        
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        if self.data is None:
            return None
        
        # Initialize tracking
        self.cleaning_report = {
            'initial_rows': len(self.data),
            'initial_columns': len(self.data.columns),
            'duplicates_removed': 0,
            'values_filled': {},
            'type_conversions': []
        }
        
        # Remove duplicates
        initial_rows = len(self.data)
        self.data = self.data.drop_duplicates()
        final_rows = len(self.data)
        duplicates_removed = final_rows - initial_rows
        self.cleaning_report['duplicates_removed'] = duplicates_removed
        
        # Handle missing values
        for column in self.data.columns:
            missing_before = self.data[column].isnull().sum()
            
            if self.data[column].dtype in ['float64', 'int64']:
                # Forward fill for numeric columns
                self.data[column] = self.data[column].ffill().bfill()
            else:
                # Mode for categorical columns
                mode_value = self.data[column].mode()
                if len(mode_value) > 0:
                    self.data[column] = self.data[column].fillna(mode_value[0])
            
            # Track actual filled values
            missing_after = self.data[column].isnull().sum()
            filled_count = missing_before - missing_after
            if filled_count > 0:
                self.cleaning_report['values_filled'][column] = filled_count
        
        # Convert potential numeric columns
        for column in self.data.columns:
            original_type = str(self.data[column].dtype)
            try:
                self.data[column] = pd.to_numeric(self.data[column])
                new_type = str(self.data[column].dtype)
                if original_type != new_type:
                    self.cleaning_report['type_conversions'].append(
                        f"{column}: {original_type} -> {new_type}"
                    )
            except (ValueError, TypeError):
                pass  # Keep as is if conversion fails
        
        if duplicates_removed > 0:
            st.info(f"Cleaned data: Removed {duplicates_removed} duplicate rows")
        
        return self.data

    def identify_date_columns(self) -> List[str]:
        """
        Identify columns that can be parsed as dates.
        
        Returns:
            List[str]: List of date column names
        """
        if self.data is None:
            return []
            
        date_cols = []
        for col in self.data.columns:
            if self.data[col].dtype == 'object':
                try:
                    pd.to_datetime(self.data[col], errors='raise')
                    date_cols.append(col)
                except (ValueError, TypeError):
                    continue
            elif np.issubdtype(self.data[col].dtype, np.datetime64):
                date_cols.append(col)
        return date_cols

    def get_cleaning_report(self) -> Optional[Dict[str, Any]]:
        """
        Get report of data cleaning operations performed.
        
        Returns:
            dict: Cleaning report with counts, or None if no cleaning performed
            {
                'initial_rows': int,
                'initial_columns': int,
                'duplicates_removed': int,
                'values_filled': Dict[str, int],  # {column: count}
                'type_conversions': List[str]
            }
        """
        if not hasattr(self, 'cleaning_report'):
            return None
        return self.cleaning_report

    def get_data_info(self) -> Dict[str, Any]:
        """
        Get metadata about the dataset.
        
        Returns:
            dict: Dictionary with row count, column count, and data types
        """
        if self.data is None:
            return {}
        
        return {
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'column_names': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'numeric_columns': list(self.data.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(self.data.select_dtypes(exclude=[np.number]).columns),
            'missing_values': self.data.isnull().sum().to_dict()
        }
