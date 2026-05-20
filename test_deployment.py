"""
Quick Start Test Script

Run this script to verify everything is set up correctly before deployment.
This performs basic smoke tests on the model and inference API.
"""

import sys
from pathlib import Path
from typing import Any


def test_imports():
    """Test that all required packages are installed."""
    print("=" * 70)
    print("TEST 1: Checking Required Packages")
    print("=" * 70)
    
    required_packages = {
        'sklearn': 'scikit-learn',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'joblib': 'joblib'
    }
    
    missing: list[str] = []
    for module_name, package_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✅ {package_name} is installed")
        except ImportError:
            print(f"❌ {package_name} is NOT installed")
            missing.append(package_name)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All required packages are installed!\n")
    return True


def test_files():
    """Test that all required files exist."""
    print("=" * 70)
    print("TEST 2: Checking Required Files")
    print("=" * 70)
    
    required_files = [
        'house_price_model.joblib',
        'preprocessing_pipeline.joblib',
        'inference.py',
        'README.md',
        'requirements.txt',
        'LICENSE',
        '.gitattributes',
        'example_usage.py'
    ]
    
    missing: list[str] = []
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            size = filepath.stat().st_size
            size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
            print(f"✅ {filename:35s} ({size_str})")
        else:
            print(f"❌ {filename:35s} (MISSING)")
            missing.append(filename)
    
    if missing:
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
        return False
    
    print("\n✅ All required files exist!\n")
    return True


def test_model_loading() -> tuple[bool, Any]:
    """Test that the model can be loaded."""
    print("=" * 70)
    print("TEST 3: Loading Model and Pipeline")
    print("=" * 70)
    
    try:
        from inference import HousePricePredictor
        
        predictor = HousePricePredictor()
        predictor.load()
        
        print("✅ Model and pipeline loaded successfully!\n")
        return True, predictor
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}\n")
        return False, None


def test_prediction(predictor: Any) -> bool:
    """Test that predictions work correctly."""
    print("=" * 70)
    print("TEST 4: Making Test Predictions")
    print("=" * 70)
    
    test_cases: list[dict[str, Any]] = [
        {
            'name': 'Expensive Bay Area house',
            'data': {
                'longitude': -122.23, 'latitude': 37.88,
                'housing_median_age': 41.0, 'total_rooms': 880.0,
                'total_bedrooms': 129.0, 'population': 322.0,
                'households': 126.0, 'median_income': 8.3252,
                'ocean_proximity': 'NEAR BAY'
            },
            'expected_range': (300000, 600000)
        },
        {
            'name': 'Inland moderate house',
            'data': {
                'longitude': -119.56, 'latitude': 36.78,
                'housing_median_age': 15.0, 'total_rooms': 4500.0,
                'total_bedrooms': 800.0, 'population': 1800.0,
                'households': 750.0, 'median_income': 3.2,
                'ocean_proximity': 'INLAND'
            },
            'expected_range': (100000, 300000)
        },
        {
            'name': 'Coastal high-income house',
            'data': {
                'longitude': -118.40, 'latitude': 34.07,
                'housing_median_age': 35.0, 'total_rooms': 2500.0,
                'total_bedrooms': 500.0, 'population': 1200.0,
                'households': 450.0, 'median_income': 7.5,
                'ocean_proximity': '<1H OCEAN'
            },
            'expected_range': (250000, 550000)
        }
    ]
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest case {i}: {test['name']}")
        print("-" * 70)
        
        try:
            prediction = predictor.predict(test['data'])
            price = prediction[0]
            min_price, max_price = test['expected_range']
            
            print(f"Input: Income=${test['data']['median_income']*10000:,.0f}, "
                  f"Location=({test['data']['longitude']}, {test['data']['latitude']}), "
                  f"Proximity={test['data']['ocean_proximity']}")
            print(f"Predicted price: ${price:,.2f}")
            
            if min_price <= price <= max_price:
                print(f"✅ Prediction is within expected range (${min_price:,} - ${max_price:,})")
            else:
                print(f"⚠️  Prediction outside expected range (${min_price:,} - ${max_price:,})")
                print("   (This might be okay, just flagging for review)")
            
        except Exception as e:
            print(f"❌ Prediction failed: {e}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All predictions completed successfully!\n")
    else:
        print("\n⚠️  Some predictions had issues\n")
    
    return all_passed


def test_batch_prediction(predictor: Any) -> bool:
    """Test batch predictions."""
    print("=" * 70)
    print("TEST 5: Batch Prediction")
    print("=" * 70)
    
    try:
        import pandas as pd
        
        # Create batch data
        batch_data = pd.DataFrame([
            {
                'longitude': -122.23, 'latitude': 37.88,
                'housing_median_age': 41.0, 'total_rooms': 880.0,
                'total_bedrooms': 129.0, 'population': 322.0,
                'households': 126.0, 'median_income': 8.3252,
                'ocean_proximity': 'NEAR BAY'
            },
            {
                'longitude': -119.56, 'latitude': 36.78,
                'housing_median_age': 15.0, 'total_rooms': 4500.0,
                'total_bedrooms': 800.0, 'population': 1800.0,
                'households': 750.0, 'median_income': 3.2,
                'ocean_proximity': 'INLAND'
            }
        ])
        
        predictions = predictor.predict(batch_data)
        
        print(f"✅ Successfully predicted {len(predictions)} houses in batch:")
        for i, price in enumerate(predictions, 1):
            print(f"   House {i}: ${price:,.2f}")
        
        print("\n✅ Batch prediction works!\n")
        return True
        
    except Exception as e:
        print(f"❌ Batch prediction failed: {e}\n")
        return False


def test_validation(predictor: Any) -> bool:
    """Test input validation."""
    print("=" * 70)
    print("TEST 6: Input Validation")
    print("=" * 70)
    
    # Test with missing feature
    print("\nTest: Missing required feature...")
    try:
        import pandas as pd
        invalid_data = pd.DataFrame([{
            'longitude': -122.23,
            'latitude': 37.88,
            # Missing other required features
        }])
        predictor.predict(invalid_data)
        print("❌ Should have raised an error for missing features")
        return False
    except ValueError as e:
        print(f"✅ Correctly caught missing features: {e}")
    
    # Test with invalid ocean_proximity
    print("\nTest: Invalid ocean_proximity value...")
    try:
        import pandas as pd
        invalid_data = pd.DataFrame([{
            'longitude': -122.23, 'latitude': 37.88,
            'housing_median_age': 41.0, 'total_rooms': 880.0,
            'total_bedrooms': 129.0, 'population': 322.0,
            'households': 126.0, 'median_income': 8.3252,
            'ocean_proximity': 'INVALID_VALUE'
        }])
        predictor.predict(invalid_data)
        print("❌ Should have raised an error for invalid ocean_proximity")
        return False
    except ValueError as e:
        print(f"✅ Correctly caught invalid value: {e}")
    
    print("\n✅ Input validation works correctly!\n")
    return True


def main() -> None:
    """Run all tests."""
    print("\n" + "=" * 70)
    print("🏠 CALIFORNIA HOUSE PRICE PREDICTION - DEPLOYMENT READINESS CHECK")
    print("=" * 70 + "\n")
    
    results: list[tuple[str, bool]] = []
    
    # Test 1: Imports
    results.append(("Required packages", test_imports()))
    
    if not results[-1][1]:
        print("\n❌ Cannot continue without required packages. Install them first.")
        sys.exit(1)
    
    # Test 2: Files
    results.append(("Required files", test_files()))
    
    if not results[-1][1]:
        print("\n❌ Cannot continue without required files.")
        sys.exit(1)
    
    # Test 3: Model loading
    success, predictor = test_model_loading()
    results.append(("Model loading", success))
    
    if not success:
        print("\n❌ Cannot continue without loading the model.")
        sys.exit(1)
    
    # Test 4: Predictions
    results.append(("Predictions", test_prediction(predictor)))
    
    # Test 5: Batch prediction
    results.append(("Batch prediction", test_batch_prediction(predictor)))
    
    # Test 6: Validation
    results.append(("Input validation", test_validation(predictor)))
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:25s} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your model is ready for deployment!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Review the DEPLOYMENT_GUIDE.md file")
        print("2. Set up Git LFS: git lfs install")
        print("3. Create a Hugging Face account if you don't have one")
        print("4. Follow the deployment steps in DEPLOYMENT_GUIDE.md")
        print("\n✨ Your model will be live on Hugging Face Model Hub soon!")
    else:
        print("⚠️  SOME TESTS FAILED - Please fix the issues above")
        print("=" * 70)
        sys.exit(1)
    
    print()


if __name__ == "__main__":
    main()
