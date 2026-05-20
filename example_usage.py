"""
Example script demonstrating how to use the house price prediction model.

This script shows various ways to load the model and make predictions.
"""

from inference import load_model, HousePricePredictor
import pandas as pd


def example_single_prediction():
    """Example: Predict a single house price using a dictionary."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Single House Prediction (Dictionary)")
    print("="*60)
    
    # Load the model
    predictor = load_model()
    
    # Define a house
    house = {  # pyright: ignore[reportUnknownVariableType]
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
    
    print("\nInput house features:")
    for key, value in house.items():  # pyright: ignore[reportUnknownVariableType]
        print(f"  {key}: {value}")
    
    # Make prediction
    prediction = predictor.predict(house)  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
    print(f"\n✅ Predicted house price: ${prediction[0]:,.2f}")


def example_convenience_method():
    """Example: Use the convenience method for single prediction."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Using Convenience Method")
    print("="*60)
    
    predictor = HousePricePredictor()
    predictor.load()
    
    # Predict using individual parameters
    price = predictor.predict_single(
        longitude=-122.22,
        latitude=37.86,
        housing_median_age=21.0,
        total_rooms=7099.0,
        total_bedrooms=1106.0,
        population=2401.0,
        households=1138.0,
        median_income=8.3014,
        ocean_proximity='NEAR BAY'
    )
    
    print(f"\n✅ Predicted house price: ${price:,.2f}")


def example_batch_predictions():
    """Example: Predict multiple houses at once using a DataFrame."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Predictions (DataFrame)")
    print("="*60)
    
    # Load the model
    predictor = load_model()
    
    # Create a DataFrame with multiple houses
    houses = pd.DataFrame([
        {
            'longitude': -122.23, 'latitude': 37.88, 
            'housing_median_age': 41.0, 'total_rooms': 880.0,
            'total_bedrooms': 129.0, 'population': 322.0,
            'households': 126.0, 'median_income': 8.3252,
            'ocean_proximity': 'NEAR BAY'
        },
        {
            'longitude': -122.22, 'latitude': 37.86,
            'housing_median_age': 21.0, 'total_rooms': 7099.0,
            'total_bedrooms': 1106.0, 'population': 2401.0,
            'households': 1138.0, 'median_income': 8.3014,
            'ocean_proximity': 'NEAR BAY'
        },
        {
            'longitude': -118.40, 'latitude': 34.07,
            'housing_median_age': 35.0, 'total_rooms': 2500.0,
            'total_bedrooms': 500.0, 'population': 1200.0,
            'households': 450.0, 'median_income': 5.5,
            'ocean_proximity': '<1H OCEAN'
        },
        {
            'longitude': -119.56, 'latitude': 36.78,
            'housing_median_age': 15.0, 'total_rooms': 4500.0,
            'total_bedrooms': 800.0, 'population': 1800.0,
            'households': 750.0, 'median_income': 3.2,
            'ocean_proximity': 'INLAND'
        }
    ])
    
    print(f"\nPredicting prices for {len(houses)} houses...")
    print("\nInput DataFrame:")
    print(houses.to_string(index=False))  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
    
    # Make predictions
    predictions = predictor.predict(houses)  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
    
    print("\n" + "-"*60)
    print("PREDICTIONS:")
    print("-"*60)
    for i, (_, row) in enumerate(houses.iterrows()):  # pyright: ignore[reportUnknownVariableType]
        print(f"\nHouse {i+1}:")
        print(f"  Location: ({row['longitude']:.2f}, {row['latitude']:.2f})")
        print(f"  Ocean Proximity: {row['ocean_proximity']}")
        print(f"  Median Income: ${row['median_income']*10000:,.0f}")
        print(f"  ➡️  Predicted Price: ${predictions[i]:,.2f}")


def example_different_ocean_proximities():
    """Example: Compare predictions for different ocean proximities."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Impact of Ocean Proximity")
    print("="*60)
    
    predictor = load_model()
    
    # Base house features
    base_house = {
        'longitude': -122.0,
        'latitude': 37.5,
        'housing_median_age': 30.0,
        'total_rooms': 2000.0,
        'total_bedrooms': 400.0,
        'population': 1000.0,
        'households': 380.0,
        'median_income': 5.0,
    }
    
    ocean_proximities = ['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND']
    
    print("\nComparing same house with different ocean proximities:")
    print(f"Base features: Median Income=${base_house['median_income']*10000:,.0f}, "
          f"Age={base_house['housing_median_age']:.0f} years")
    print("\n" + "-"*60)
    
    predictions = []  # pyright: ignore[reportUnknownVariableType]
    for proximity in ocean_proximities:
        house = base_house.copy()  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        house['ocean_proximity'] = proximity  # pyright: ignore[reportArgumentType, reportUnknownVariableType,reportUnknownMemberType]
        prediction = predictor.predict(house)  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        predictions.append((proximity, prediction[0]))  # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
        print(f"{proximity:15s} ➡️  ${prediction[0]:,.2f}")
    
    # Find the most expensive
    most_expensive = max(predictions, key=lambda x: x[1])  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType,reportUnknownLambdaType,reportUnknownParameterType]
    print(f"\n💰 Highest price: {most_expensive[0]} at ${most_expensive[1]:,.2f}")


if __name__ == "__main__":
    print("\n🏠 CALIFORNIA HOUSE PRICE PREDICTION - USAGE EXAMPLES 🏠")
    print("="*60)
    
    try:
        example_single_prediction()
        example_convenience_method()
        example_batch_predictions()
        example_different_ocean_proximities()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the model files are in the current directory:")
        print("  - house_price_model.joblib")
        print("  - preprocessing_pipeline.joblib")
    except Exception as e:
        print(f"\n❌ Error: {e}")
