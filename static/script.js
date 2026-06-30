function init() {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const predictionValue = document.getElementById('prediction-value');
    const submitBtn = document.getElementById('submit-btn');

    // Validation rules
    const validationRules = {
        longitude: { min: -124.5, max: -114.0 },
        latitude: { min: 32.5, max: 42.0 },
        housing_median_age: { min: 1, max: 52, isInt: true },
        median_income: { min: 0.5, max: 15.0 },
        total_rooms: { min: 1, isInt: true },
        total_bedrooms: { min: 1, isInt: true },
        population: { min: 1, isInt: true },
        households: { min: 1, isInt: true },
        ocean_proximity: { required: true }
    };

    // Form inputs to validate
    const inputsToValidate = form.querySelectorAll('input, select');

    // Validate form fields dynamically
    function validateForm() {
        let isFormValid = true;

        for (const [id, rules] of Object.entries(validationRules)) {
            const input = document.getElementById(id);
            const errorSpan = document.getElementById(`${id}-error`);
            if (!input) {
                console.log(`Field not found: ${id}`);
                continue;
            }

            const val = input.value;
            let numVal = NaN;
            let isFieldValid = true;

            // Handle empty/unselected state
            if (val === "" || val === null || val === undefined) {
                isFieldValid = false;
                isFormValid = false;
                input.classList.remove('invalid');
                if (errorSpan) errorSpan.style.display = 'none';
            } else if (id === 'ocean_proximity') {
                if (val === "") {
                    isFieldValid = false;
                    isFormValid = false;
                    input.classList.add('invalid');
                    if (errorSpan) errorSpan.style.display = 'block';
                } else {
                    input.classList.remove('invalid');
                    if (errorSpan) errorSpan.style.display = 'none';
                }
            } else {
                // Numeric field validation
                numVal = parseFloat(val);
                if (isNaN(numVal)) {
                    isFieldValid = false;
                } else {
                    if (rules.min !== undefined && numVal < rules.min) isFieldValid = false;
                    if (rules.max !== undefined && numVal > rules.max) isFieldValid = false;
                    if (rules.isInt && (!Number.isInteger(numVal) || numVal % 1 !== 0)) isFieldValid = false;
                }

                if (isFieldValid) {
                    input.classList.remove('invalid');
                    if (errorSpan) errorSpan.style.display = 'none';
                } else {
                    isFormValid = false;
                    input.classList.add('invalid');
                    if (errorSpan) errorSpan.style.display = 'block';
                }
            }

            console.log(`Field: ${id} | Value: "${val}" | Parsed Numeric: ${numVal} | Field Valid: ${isFieldValid}`);
        }

        console.log("Form Valid:", isFormValid);
        submitBtn.disabled = !isFormValid;
    }

    // Attach event listeners for real-time validation
    inputsToValidate.forEach(input => {
        input.addEventListener('input', validateForm);
        input.addEventListener('change', validateForm);
    });

    // Run validation on initial load
    validateForm();

    // Range slider updates
    const ranges = [
        { id: 'housing_median_age', suffix: ' Years', isIncome: false },
        { id: 'median_income', suffix: '', isIncome: true }
    ];

    ranges.forEach(range => {
        const input = document.getElementById(range.id);
        const output = document.querySelector(`output[for="${range.id}"]`);
        
        if (input && output) {
            input.addEventListener('input', () => {
                if (range.isIncome) {
                    // Display raw float value without dollar symbol or commas
                    output.textContent = parseFloat(input.value).toFixed(1);
                } else {
                    output.textContent = input.value + range.suffix;
                }
                validateForm();
            });
        }
    });

    // Form submit listener
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        console.log("Button clicked");
        
        // Final sanity check before submission
        validateForm();
        if (submitBtn.disabled) {
            console.log("Form is invalid, submission cancelled.");
            return;
        }

        // Button state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Calculating...';
        
        // Exact data type casting
        const data = {
            longitude: parseFloat(document.getElementById('longitude').value),
            latitude: parseFloat(document.getElementById('latitude').value),
            housing_median_age: parseInt(document.getElementById('housing_median_age').value, 10),
            total_rooms: parseInt(document.getElementById('total_rooms').value, 10),
            total_bedrooms: parseInt(document.getElementById('total_bedrooms').value, 10),
            population: parseInt(document.getElementById('population').value, 10),
            households: parseInt(document.getElementById('households').value, 10),
            median_income: parseFloat(document.getElementById('median_income').value),
            ocean_proximity: document.getElementById('ocean_proximity').value
        };

        console.log("Sending request", data);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                let errMsg = 'Prediction failed';
                try {
                    const errJson = await response.json();
                    if (errJson && errJson.error) {
                        errMsg = errJson.error;
                    } else if (errJson && errJson.detail) {
                        if (typeof errJson.detail === 'string') {
                            errMsg = errJson.detail;
                        } else if (Array.isArray(errJson.detail)) {
                            errMsg = errJson.detail.map(d => `${d.loc.join('.')}: ${d.msg}`).join(', ');
                        }
                    }
                } catch (e) {
                    // Ignore JSON parsing errors
                }
                const fetchErr = new Error(errMsg);
                console.error("Print fetch errors:", fetchErr);
                throw fetchErr;
            }

            const result = await response.json();
            console.log("Print API response", result);
            
            // Display result
            resultContainer.classList.remove('hidden');
            
            const formattedPrice = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
            }).format(result.prediction);
            
            predictionValue.textContent = formattedPrice;
            
            // Scroll to result
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            console.error('Error:', error);
            alert(`Error: ${error.message}`);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Calculate Prediction';
            validateForm();
        }
    });

    // Reset listener
    form.addEventListener('reset', () => {
        resultContainer.classList.add('hidden');
        // Reset range outputs manually
        setTimeout(() => {
            ranges.forEach(range => {
                const input = document.getElementById(range.id);
                const output = document.querySelector(`output[for="${range.id}"]`);
                if (input && output) {
                    input.dispatchEvent(new Event('input'));
                }
            });
            // Clear invalid styling classes on reset
            inputsToValidate.forEach(input => {
                input.classList.remove('invalid');
                const errorSpan = document.getElementById(`${input.id}-error`);
                if (errorSpan) errorSpan.style.display = 'none';
            });
            validateForm();
        }, 0);
    });
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
