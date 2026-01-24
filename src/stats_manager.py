import pandas as pd
import numpy as np
from scipy import stats
from typing import Optional, Dict, Any, List

class StatsManager:
    """
    Handles statistical calculations, hypothesis testing, and advanced analytics.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the StatsManager with a dataframe.
        
        Args:
            data: The dataframe to analyze.
        """
        self.data = data

    def get_basic_stats(self) -> Dict[str, Any]:
        """
        Calculate basic statistics for numeric columns.
        
        Returns:
            dict: Dictionary containing mean, median, and standard deviation
        """
        if self.data is None:
            return {}
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        stats_dict = {
            'mean': self.data[numeric_cols].mean().to_dict(),
            'median': self.data[numeric_cols].median().to_dict(),
            'std': self.data[numeric_cols].std().to_dict(),
            'min': self.data[numeric_cols].min().to_dict(),
            'max': self.data[numeric_cols].max().to_dict()
        }
        
        return stats_dict

    def get_advanced_stats(self) -> Dict[str, Any]:
        """
        Calculate advanced statistics for numeric columns.
        
        Returns:
            dict: Dictionary containing skewness, kurtosis, quantiles, and IQR
        """
        if self.data is None:
            return {}
        
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if numeric_cols.empty:
            return {}
            
        stats_dict = {
            'skewness': self.data[numeric_cols].skew().to_dict(),
            'kurtosis': self.data[numeric_cols].kurtosis().to_dict(),
            '25%': self.data[numeric_cols].quantile(0.25).to_dict(),
            '75%': self.data[numeric_cols].quantile(0.75).to_dict()
        }
        
        # Calculate IQR
        stats_dict['iqr'] = {col: stats_dict['75%'][col] - stats_dict['25%'][col] for col in numeric_cols}
        
        return stats_dict
    
    def get_outliers(self) -> Dict[str, pd.DataFrame]:
        """
        Identify outliers using IQR method.
        
        Returns:
            dict: Dictionary where keys are column names and values are dataframes of outliers
        """
        if self.data is None:
            return {}
            
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_cols:
            Q1 = self.data[col].quantile(0.25)
            Q3 = self.data[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Find outliers
            outlier_mask = (self.data[col] < lower_bound) | (self.data[col] > upper_bound)
            if outlier_mask.any():
                outlier_df = self.data[outlier_mask].copy()
                outlier_df['Outlier_Reason'] = np.where(
                    outlier_df[col] < lower_bound, 
                    f'Low (< {lower_bound:.2f})', 
                    f'High (> {upper_bound:.2f})'
                )
                outliers[col] = outlier_df
                
        return outliers

    def get_correlations(self) -> Optional[pd.DataFrame]:
        """
        Compute correlation matrix for numeric columns.
        
        Returns:
            pd.DataFrame: Correlation matrix or None if no numeric columns
        """
        if self.data is None:
            return None
        
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if numeric_data.empty:
            return None
        
        return numeric_data.corr()

    def get_top_correlations(self, n: int = 5) -> pd.DataFrame:
        """
        Get top n correlations (positive and negative).
        
        Args:
            n: Number of top correlations to return
            
        Returns:
            pd.DataFrame: DataFrame with pairs and correlation coefficients
        """
        corr_matrix = self.get_correlations()
        if corr_matrix is None:
            return pd.DataFrame()
            
        # Unstack and reset index to get pairs
        pairs = corr_matrix.abs().unstack()
        pairs = pairs.sort_values(ascending=False)
        
        # Remove self-correlations (1.0) and duplicates
        pairs = pairs[pairs < 1.0]
        pairs = pairs.iloc[::2]  # Take every other to remove duplicates (A-B, B-A)
        
        top_pairs = pairs.head(n).index
        
        results = []
        for (col1, col2) in top_pairs:
            coef = corr_matrix.loc[col1, col2]
            results.append({
                'Variable 1': col1,
                'Variable 2': col2,
                'Correlation': coef,
                'Strength': 'Strong' if abs(coef) > 0.7 else 'Moderate' if abs(coef) > 0.3 else 'Weak'
            })
            
        return pd.DataFrame(results)

    def get_grouped_stats(self, group_col: str, value_col: str, agg_func: str) -> pd.DataFrame:
        """
        Calculate grouped statistics.
        
        Args:
            group_col: Column to group by
            value_col: Column to aggregate
            agg_func: Aggregation function name ('mean', 'sum', 'count', 'min', 'max')
            
        Returns:
            pd.DataFrame: Grouped statistics
        """
        if self.data is None:
            return pd.DataFrame()
            
        try:
            grouped = self.data.groupby(group_col)[value_col].agg(agg_func).reset_index()
            grouped.columns = [group_col, f"{agg_func.capitalize()} of {value_col}"]
            return grouped.sort_values(by=grouped.columns[1], ascending=False)
        except Exception:
            return pd.DataFrame()
    
    def get_column_details(self) -> pd.DataFrame:
        """
        Get detailed info about columns.
        
        Returns:
            pd.DataFrame: DataFrame with column details
        """
        if self.data is None:
            return pd.DataFrame()
            
        details = []
        for col in self.data.columns:
            # Get top value safely
            try:
                top_val = self.data[col].mode().iloc[0] if not self.data[col].mode().empty else "N/A"
                freq = self.data[col].value_counts().iloc[0] if not self.data[col].value_counts().empty else 0
            except Exception:
                top_val = "Error"
                freq = 0
                
            details.append({
                'Column': col,
                'Type': str(self.data[col].dtype),
                'Unique Values': self.data[col].nunique(),
                'Missing Values': self.data[col].isnull().sum(),
                'Missing (%)': (self.data[col].isnull().sum() / len(self.data)) * 100,
                'Top Value': str(top_val)[:50],  # Truncate if too long
                'Freq': freq,
                'Memory (KB)': self.data[col].memory_usage(deep=True) / 1024
            })
        return pd.DataFrame(details)

    def get_comprehensive_summary(self) -> pd.DataFrame:
        """
        Get a master summary dataframe combining metadata and statistics.
        
        Returns:
            pd.DataFrame: Unified dataframe with all column info
        """
        if self.data is None:
            return pd.DataFrame()
            
        # 1. Get Base Metadata
        meta_df = self.get_column_details()
        if meta_df.empty:
            return pd.DataFrame()
        
        # 2. Get Statistics
        stats_dict = self.get_basic_stats()
        
        # 3. Merge
        # Initialize stat columns
        meta_df['Mean'] = '-'
        meta_df['Min'] = '-'
        meta_df['Max'] = '-'
        meta_df['Std Dev'] = '-'
        
        if stats_dict:
            for col in stats_dict['mean'].keys():
                idx = meta_df[meta_df['Column'] == col].index
                if not idx.empty:
                    i = idx[0]
                    meta_df.at[i, 'Mean'] = f"{stats_dict['mean'][col]:.2f}"
                    meta_df.at[i, 'Min'] = f"{stats_dict['min'][col]:.2f}"
                    meta_df.at[i, 'Max'] = f"{stats_dict['max'][col]:.2f}"
                    meta_df.at[i, 'Std Dev'] = f"{stats_dict['std'][col]:.2f}"
        
        # Reorder columns for better readability
        cols = ['Column', 'Type', 'Missing (%)', 'Unique Values', 'Top Value', 'Freq', 'Mean', 'Min', 'Max', 'Std Dev', 'Memory (KB)']
        return meta_df[cols]

    def get_time_series_data(self, date_col: str, value_col: str, freq: str = 'D') -> pd.DataFrame:
        """
        Resample data for time series analysis.
        
        Args:
            date_col: Date column name
            value_col: Numeric column to aggregate
            freq: Frequency ('D', 'W', 'M', 'Q', 'Y')
            
        Returns:
            pd.DataFrame: Resampled data
        """
        if self.data is None:
            return pd.DataFrame()
            
        try:
            df = self.data.copy()
            df[date_col] = pd.to_datetime(df[date_col])
            df = df.set_index(date_col)
            resampled = df[value_col].resample(freq).mean().reset_index()
            return resampled
        except Exception:
            return pd.DataFrame()

    def calculate_regression(self, x_col: str, y_col: str) -> Dict[str, Any]:
        """
        Calculate simple linear regression metrics.
        
        Args:
            x_col: Independent variable
            y_col: Dependent variable
            
        Returns:
            dict: Regression metrics (slope, intercept, r_squared, predictions)
        """
        if self.data is None:
            return {}
            
        try:
            # Drop NaNs for calculation
            valid_data = self.data[[x_col, y_col]].dropna()
            x = valid_data[x_col].values
            y = valid_data[y_col].values
            
            if len(x) < 2:
                return {}
            
            # Calculate regression (degree 1)
            slope, intercept = np.polyfit(x, y, 1)
            
            # Calculate R-squared
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            
            return {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_squared,
                'equation': f"y = {slope:.4f}x + {intercept:.4f}"
            }
        except Exception:
            return {}

    def perform_normality_test(self, column: str) -> Dict[str, Any]:
        """
        Perform Shapiro-Wilk test for normality.
        
        Args:
            column: Numeric column to test
            
        Returns:
            dict: Test results
        """
        if self.data is None or column not in self.data.columns:
            return {}
        
        try:
            # Drop NaNs
            data = self.data[column].dropna()
            
            # Shapiro-Wilk test (limit to 5000 samples for performance/validity)
            if len(data) > 5000:
                data = data.sample(5000)
                
            stat, p_value = stats.shapiro(data)
            
            results = {
                'test': 'Shapiro-Wilk',
                'statistic': stat,
                'p_value': p_value,
                'is_normal': p_value > 0.05
            }
            
            # Add sample size warning
            warning = self.validate_sample_size(column, min_required=30)
            if warning:
                results['warning'] = warning
            
            return results
        except Exception:
            return {}

    def perform_ttest(self, group_col: str, value_col: str) -> Dict[str, Any]:
        """
        Perform independent t-test between two groups.
        
        Args:
            group_col: Categorical column with 2 groups
            value_col: Numeric column to compare
            
        Returns:
            dict: Test results
        """
        if self.data is None:
            return {}
            
        try:
            groups = self.data[group_col].dropna().unique()
            if len(groups) != 2:
                return {'error': f'Column must have exactly 2 unique groups (found {len(groups)})'}
                
            group1 = self.data[self.data[group_col] == groups[0]][value_col].dropna()
            group2 = self.data[self.data[group_col] == groups[1]][value_col].dropna()
            
            stat, p_value = stats.ttest_ind(group1, group2)
            
            results = {
                'test': 'Independent T-Test',
                'group1': str(groups[0]),
                'group2': str(groups[1]),
                'statistic': stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
            
            # Add validation warnings
            warnings = self.validate_ttest_balance(group_col, value_col)
            if warnings:
                results['warnings'] = warnings
            
            return results
        except Exception as e:
            return {'error': str(e)}

    def _count_outlier_cells(self) -> int:
        """
        Count total number of outlier cells across all numeric columns.
        
        Returns:
            int: Total count of outlier cells
        """
        if self.data is None:
            return 0
            
        outliers = self.get_outliers()
        if not outliers:
            return 0
            
        total_outlier_cells = sum(df.shape[0] for df in outliers.values())
        return total_outlier_cells

    def calculate_health_score(self) -> Optional[Dict[str, Any]]:
        """
        Calculate dataset health score (0-100) based on multiple quality metrics.
        
        Returns:
            dict: Health score report with components, or None if no data
            {
                'score': float,              # 0-100
                'rating': str,               # "Excellent" | "Good" | "Fair" | "Poor"
                'components': {
                    'missing_score': float,
                    'duplicate_score': float,
                    'outlier_score': float,
                    'consistency_score': float
                }
            }
        """
        if self.data is None or self.data.empty:
            return None
            
        # Component 1: Missing Values Score (30% weight)
        total_cells = self.data.shape[0] * self.data.shape[1]
        if total_cells == 0:
            return None
            
        total_missing_cells = self.data.isnull().sum().sum()
        missing_ratio = total_missing_cells / total_cells
        missing_score = (1 - missing_ratio) * 100
        
        # Component 2: Duplicate Score (25% weight)
        total_rows = len(self.data)
        if total_rows == 0:
            return None
            
        duplicate_rows = self.data.duplicated().sum()
        duplicate_ratio = duplicate_rows / total_rows
        duplicate_score = (1 - duplicate_ratio) * 100
        
        # Component 3: Outlier Score (25% weight)
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        total_numeric_cells = len(numeric_cols) * total_rows
        
        if total_numeric_cells == 0:
            # No numeric columns → treat as perfect for this component
            outlier_score = 100.0
        else:
            total_outlier_cells = self._count_outlier_cells()
            outlier_ratio = total_outlier_cells / total_numeric_cells
            # Cap at 20% outliers for scoring
            capped_ratio = min(outlier_ratio, 0.2) / 0.2
            outlier_score = (1 - capped_ratio) * 100
        
        # Component 4: Consistency Score (20% weight)
        total_columns = len(self.data.columns)
        if total_columns == 0:
            return None
            
        # Count object columns that could potentially be numeric
        object_cols = self.data.select_dtypes(include=['object']).columns
        mixed_type_count = 0
        
        for col in object_cols:
            try:
                pd.to_numeric(self.data[col], errors='raise')
                mixed_type_count += 1
            except (ValueError, TypeError):
                pass  # Column is correctly non-numeric
        
        mixed_type_penalty = mixed_type_count / total_columns
        consistency_score = (1 - mixed_type_penalty) * 100
        
        # Calculate total score with weights
        total_score = (
            missing_score * 0.30 +
            duplicate_score * 0.25 +
            outlier_score * 0.25 +
            consistency_score * 0.20
        )
        
        # Determine rating
        if total_score >= 90:
            rating = "Excellent"
        elif total_score >= 70:
            rating = "Good"
        elif total_score >= 50:
            rating = "Fair"
        else:
            rating = "Poor"
        
        return {
            'score': total_score,
            'rating': rating,
            'components': {
                'missing_score': missing_score,
                'duplicate_score': duplicate_score,
                'outlier_score': outlier_score,
                'consistency_score': consistency_score
            }
        }

    def generate_distribution_insight(self, column: str) -> str:
        """
        Generate plain English insight about a column's distribution.
        
        Args:
            column: Name of numeric column to analyze
            
        Returns:
            str: User-friendly description of distribution characteristics
        """
        if self.data is None or column not in self.data.columns:
            return "Unable to analyze distribution for this column."
            
        try:
            col_data = self.data[column].dropna()
            
            if len(col_data) == 0:
                return f"{column} has no valid data to analyze."
                
            # Calculate skewness and kurtosis
            skew = col_data.skew()
            kurt = col_data.kurtosis()
            
            # Generate insight based on skewness
            if abs(skew) < 0.5:
                skew_desc = f"{column} has a fairly symmetric distribution with balanced spread."
            elif skew > 0.5:
                skew_desc = f"{column} is right-skewed with several high values pulling the average up."
            else:
                skew_desc = f"{column} is left-skewed with several low values pulling the average down."
            
            # Add kurtosis context if notable
            if abs(kurt) > 3:
                skew_desc += " The data has heavy tails with more extreme values than a normal distribution."
            
            return skew_desc
            
        except Exception:
            return f"Unable to generate insight for {column}."
    
    def generate_correlation_insight(self) -> str:
        """
        Generate plain English insight about the strongest correlation.
        
        Returns:
            str: User-friendly description of top correlation
        """
        try:
            top_corr = self.get_top_correlations(n=1)
            
            if top_corr.empty:
                return "Not enough numeric data to identify strong relationships."
            
            var1 = top_corr.iloc[0]['Variable 1']
            var2 = top_corr.iloc[0]['Variable 2']
            coef = top_corr.iloc[0]['Correlation']
            
            # Determine direction and strength
            if coef > 0:
                direction = "positively"
                meaning = "they tend to increase together"
            else:
                direction = "negatively"
                meaning = "when one increases, the other decreases"
            
            strength = top_corr.iloc[0]['Strength'].lower()
            
            return f"{var1} and {var2} are {strength} {direction} correlated (r={coef:.2f}), meaning {meaning}."
            
        except Exception:
            return "Unable to analyze correlations in this dataset."
    
    def generate_outlier_insight(self) -> str:
        """
        Generate plain English insight about outliers in the dataset.
        
        Returns:
            str: User-friendly description of outlier findings
        """
        try:
            outliers = self.get_outliers()
            
            if not outliers:
                return "No statistical outliers detected in your dataset."
            
            total_outliers = sum(df.shape[0] for df in outliers.values())
            num_columns = len(outliers)
            
            if num_columns == 1:
                col_text = "1 column"
            else:
                col_text = f"{num_columns} columns"
            
            return f"Found {total_outliers} outlier(s) across {col_text}. These are unusual values that differ significantly from the rest."
            
        except Exception:
            return "Unable to analyze outliers in this dataset."

    def validate_sample_size(self, column: str, min_required: int = 30) -> Optional[str]:
        """
        Validate if sample size is sufficient for statistical testing.
        
        Args:
            column: Column to check
            min_required: Minimum required sample size (default: 30)
            
        Returns:
            str: Warning message or None if valid
        """
        if self.data is None or column not in self.data.columns:
            return None
            
        n = self.data[column].dropna().shape[0]
        if n < min_required:
            return f"Small sample size (n={n}). Results may be unreliable. Aim for at least {min_required} samples."
        return None
    
    def validate_ttest_balance(self, group_col: str, value_col: str) -> List[str]:
        """
        Validate t-test conditions: group sizes and balance.
        
        Args:
            group_col: Grouping column
            value_col: Value column
            
        Returns:
            list: List of warning strings (empty if valid)
        """
        warnings = []
        
        if self.data is None:
            return warnings
            
        try:
            groups = self.data[group_col].dropna().unique()
            if len(groups) != 2:
                return warnings
            
            g1_size = len(self.data[self.data[group_col] == groups[0]][value_col].dropna())
            g2_size = len(self.data[self.data[group_col] == groups[1]][value_col].dropna())
            
            # Check minimum size (threshold: 10 per group)
            if g1_size < 10 or g2_size < 10:
                warnings.append(f"Small group size ({groups[0]}={g1_size}, {groups[1]}={g2_size}). Aim for at least 10 per group.")
            
            # Check balance (threshold: 3:1 ratio)
            if min(g1_size, g2_size) > 0:
                ratio = max(g1_size, g2_size) / min(g1_size, g2_size)
                if ratio > 3:
                    warnings.append(f"Unbalanced groups (ratio {ratio:.1f}:1). Results may be affected.")
            
        except Exception:
            pass
            
        return warnings
