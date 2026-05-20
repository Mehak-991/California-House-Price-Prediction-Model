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
    
    def __init__(self, model_path: str = "house_price_model.joblib", 
                 pipeline_path: str = "preprocessing_pipeline.joblib"):
        """
        Initialize the predictor by loading the model and preprocessing pipeline.
        
        Args:
            model_path: Path to the trained model joblib file
            pipeline_path: Path to the preprocessing pipeline joblib file
        """
        self.model_path = Path(model_path)
        self.pipeline_path = Path(pipeline_path)
        self.model = None
        self.pipeline = None
        self.feature_names = [
            'longitude', 'latitude', 'housing_median_age', 'total_rooms',
            'total_bedrooms', 'population', 'households', 'median_income',
            'ocean_proximity'
        ]
        self.valid_ocean_proximity = ['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND']
        
    def load(self):
        """Load the model and preprocessing pipeline from disk."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        if not self.pipeline_path.exists():
            raise FileNotFoundError(f"Pipeline file not found: {self.pipeline_path}")
            
        self.model = joblib.load(self.model_path)
        self.pipeline = joblib.load(self.pipeline_path)
        print(f"✅ Model loaded successfully from {self.model_path}")
        print(f"✅ Pipeline loaded successfully from {self.pipeline_path}")
        
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
        if self.model is None or self.pipeline is None:
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
def load_model(model_path: str = "house_price_model.joblib",
               pipeline_path: str = "preprocessing_pipeline.joblib") -> HousePricePredictor:
    """
    Load and return a HousePricePredictor instance.
    
    Args:
        model_path: Path to the trained model joblib file
        pipeline_path: Path to the preprocessing pipeline joblib file
        
    Returns:
        Loaded HousePricePredictor instance
    """
    predictor = HousePricePredictor(model_path, pipeline_path)
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
