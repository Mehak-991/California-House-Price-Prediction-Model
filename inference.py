"""
House Price Prediction Inference Module

This module provides a simple API for loading the trained California house price
prediction model and making predictions on new data.
"""

import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, Dict, List


class HousePricePredictor:
    """
    A predictor class for California house prices.
    
    This class loads a pre-trained Random Forest model and its preprocessing pipeline,
    and provides methods for making predictions on new housing data.
    """
    
    def __init__(self, model_dir: Union[str, Path] = None):
        """
        Initialize the predictor by setting paths.
        
        Args:
            model_dir: Path to the directory containing model files
        """
        self.base_dir = Path(__file__).resolve().parent
        self.model_dir = Path(model_dir) if model_dir else self.base_dir / "model"
        
        self.model_path = self.model_dir / "model.pkl"
        self.encoder_path = self.model_dir / "encoder.pkl"
        self.scaler_path = self.model_dir / "scaler.pkl"
        self.pipeline_path = self.model_dir / "pipeline.pkl"
        
        self.model = None
        self.pipeline = None
        self.encoder = None
        self.scaler = None
        
        self.feature_names = [
            'longitude', 'latitude', 'housing_median_age', 'total_rooms',
            'total_bedrooms', 'population', 'households', 'median_income',
            'ocean_proximity'
        ]
        self.valid_ocean_proximity = ['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND']
        
    def load(self):
        """Load the model, encoder, scaler, and pipeline from disk."""
        # Check if files exist. If not, try auto-migration
        paths = {
            "model.pkl": self.model_path,
            "encoder.pkl": self.encoder_path,
            "scaler.pkl": self.scaler_path,
            "pipeline.pkl": self.pipeline_path
        }
        
        missing = [name for name, path in paths.items() if not path.exists()]
        
        if missing:
            # Try to auto-migrate from joblib files in parent/base directory if they exist
            joblib_model_path = self.base_dir / "house_price_model.joblib"
            joblib_pipeline_path = self.base_dir / "preprocessing_pipeline.joblib"
            
            if joblib_model_path.exists() and joblib_pipeline_path.exists():
                print("🔄 Migrating joblib model files to PKL format...")
                try:
                    self.model_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Load from joblib
                    forest_reg = joblib.load(joblib_model_path)
                    full_pipeline = joblib.load(joblib_pipeline_path)
                    
                    # Extract components
                    scaler = full_pipeline.named_transformers_['num'].named_steps['std_scaler']
                    encoder = full_pipeline.named_transformers_['cat']
                    
                    # Dump as PKLs
                    joblib.dump(forest_reg, self.model_path)
                    joblib.dump(full_pipeline, self.pipeline_path)
                    joblib.dump(encoder, self.encoder_path)
                    joblib.dump(scaler, self.scaler_path)
                    print("✅ Migration completed successfully!")
                    
                    # Re-clear missing list since files are now created
                    missing = []
                except Exception as migrate_err:
                    print(f"⚠️  Auto-migration failed: {migrate_err}")
            
        # If still missing, raise a descriptive FileNotFoundError
        if missing:
            missing_details = ", ".join([f"'{name}' (expected at: {paths[name]})" for name in missing])
            error_details = (
                f"Missing required ML model files: {missing_details}.\n"
                f"Please ensure they are located in the model directory: {self.model_dir}.\n"
                f"Alternatively, place the original 'house_price_model.joblib' and 'preprocessing_pipeline.joblib' "
                f"files in the base directory '{self.base_dir}' to trigger automatic migration."
            )
            raise FileNotFoundError(error_details)
            
        # Load the components
        self.model = joblib.load(self.model_path)
        self.pipeline = joblib.load(self.pipeline_path)
        self.encoder = joblib.load(self.encoder_path)
        self.scaler = joblib.load(self.scaler_path)
        
        # Log model components loaded
        print(f"✅ Loaded model from {self.model_path}")
        print(f"✅ Loaded pipeline from {self.pipeline_path}")
        print(f"✅ Loaded encoder from {self.encoder_path}")
        print(f"✅ Loaded scaler from {self.scaler_path}")
        
    def validate_input(self, data: pd.DataFrame):
        """
        Validate that input data has all required features.
        
        Args:
            data: DataFrame with input features
            
        Raises:
            ValueError: If required features are missing or invalid
        """
        missing_features = set(self.feature_names) - set(data.columns)
        if missing_features:
            raise ValueError(f"Missing required features: {missing_features}")
        
        # Validate ocean_proximity values
        invalid_values = set(data['ocean_proximity'].unique()) - set(self.valid_ocean_proximity)
        if invalid_values:
            raise ValueError(
                f"Invalid ocean_proximity values: {invalid_values}. "
                f"Valid values are: {self.valid_ocean_proximity}"
            )
    
    def predict(self, data: Union[pd.DataFrame, Dict, List[Dict]]) -> np.ndarray:
        """
        Make predictions on input data.
        
        Args:
            data: Input data as DataFrame, single dict, or list of dicts.
                  Must contain all required features:
                  - longitude (float): Longitude coordinate
                  - latitude (float): Latitude coordinate
                  - housing_median_age (float): Median age of houses in the block
                  - total_rooms (float): Total number of rooms in the block
                  - total_bedrooms (float): Total number of bedrooms in the block
                  - population (float): Total population in the block
                  - households (float): Total number of households in the block
                  - median_income (float): Median income of households (in tens of thousands)
                  - ocean_proximity (str): Proximity to ocean, one of:
                    '<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND'
        
        Returns:
            numpy array of predicted house prices (in dollars)
            
        Example:
            >>> predictor = HousePricePredictor()
            >>> predictor.load()
            >>> data = {
            ...     'longitude': -122.23,
            ...     'latitude': 37.88,
            ...     'housing_median_age': 41.0,
            ...     'total_rooms': 880.0,
            ...     'total_bedrooms': 129.0,
            ...     'population': 322.0,
            ...     'households': 126.0,
            ...     'median_income': 8.3252,
            ...     'ocean_proximity': 'NEAR BAY'
            ... }
            >>> prediction = predictor.predict(data)
            >>> print(f"Predicted price: ${prediction[0]:,.2f}")
        """
        if self.model is None or self.pipeline is None or self.encoder is None or self.scaler is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        # Convert input to DataFrame if needed
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        elif isinstance(data, list):
            data = pd.DataFrame(data)
        elif not isinstance(data, pd.DataFrame):
            raise TypeError("Input must be a DataFrame, dict, or list of dicts")
        
        # Validate input
        self.validate_input(data)
        
        # Ensure exact column order matching self.feature_names
        data = data[self.feature_names]
        
        # Prepare data using the preprocessing pipeline
        prepared_data = self.pipeline.transform(data)
        
        # Make predictions
        predictions = self.model.predict(prepared_data)
        
        return predictions
    
    def predict_single(self, longitude: float, latitude: float, 
                      housing_median_age: float, total_rooms: float,
                      total_bedrooms: float, population: float,
                      households: float, median_income: float,
                      ocean_proximity: str) -> float:
        """
        Convenience method to predict a single house price from individual parameters.
        
        Args:
            longitude: Longitude coordinate
            latitude: Latitude coordinate
            housing_median_age: Median age of houses in the block
            total_rooms: Total number of rooms in the block
            total_bedrooms: Total number of bedrooms in the block
            population: Total population in the block
            households: Total number of households in the block
            median_income: Median income of households (in tens of thousands)
            ocean_proximity: Proximity to ocean ('&lt;1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND')
        
        Returns:
            Predicted house price in dollars
        """
        data = {
            'longitude': longitude,
            'latitude': latitude,
            'housing_median_age': housing_median_age,
            'total_rooms': total_rooms,
            'total_bedrooms': total_bedrooms,
            'population': population,
            'households': households,
            'median_income': median_income,
            'ocean_proximity': ocean_proximity
        }
        
        prediction = self.predict(data)
        return float(prediction[0])


# Convenience functions for quick use
def load_model(model_dir: Union[str, Path] = None) -> HousePricePredictor:
    """
    Load and return a HousePricePredictor instance.
    
    Args:
        model_dir: Path to the directory containing model files
        
    Returns:
        Loaded HousePricePredictor instance
    """
    predictor = HousePricePredictor(model_dir)
    predictor.load()
    return predictor


if __name__ == "__main__":
    # Example usage
    print("Loading model...")
    predictor = load_model()
    
    # Example prediction
    example_data = {
        'longitude': -122.23,
        'latitude': 37.88,
        'housing_median_age': 41.0,
        'total_rooms': 880.0,
        'total_bedrooms': 129.0,
        'population': 322.0,
        'households': 126.0,
        'median_income': 8.3252,
        'ocean_proximity': 'NEAR BAY'
    }
    
    print("\nMaking prediction for example data:")
    print(example_data)
    
    prediction = predictor.predict(example_data)
    print(f"\n✅ Predicted house price: ${prediction[0]:,.2f}")
