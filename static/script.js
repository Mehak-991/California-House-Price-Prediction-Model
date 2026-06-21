document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const resultContainer = document.getElementById('result-container');
    const predictionValue = document.getElementById('prediction-value');
    const submitBtn = document.getElementById('submit-btn');

    // Live update for range outputs
    const ranges = [
        { id: 'housing_median_age', suffix: ' Years' },
        { id: 'median_income', multiplier: 10000, isCurrency: true }
    ];

    ranges.forEach(range => {
        const input = document.getElementById(range.id);
        const output = document.querySelector(`output[for="${range.id}"]`);
        
        input.addEventListener('input', () => {
            if (range.isCurrency) {
                const val = parseFloat(input.value) * range.multiplier;
                output.textContent = new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD',
                    maximumFractionDigits: 0
                }).format(val);
            } else {
                output.textContent = input.value + range.suffix;
            }
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Button state
        submitBtn.disabled = true;
        submitBtn.textContent = 'Calculating...';
        
        const data = {
            longitude: parseFloat(document.getElementById('longitude').value),
            latitude: parseFloat(document.getElementById('latitude').value),
            housing_median_age: parseFloat(document.getElementById('housing_median_age').value),
            total_rooms: parseFloat(document.getElementById('total_rooms').value),
            total_bedrooms: parseFloat(document.getElementById('total_bedrooms').value),
            population: parseFloat(document.getElementById('population').value),
            households: parseFloat(document.getElementById('households').value),
            median_income: parseFloat(document.getElementById('median_income').value),
            ocean_proximity: document.getElementById('ocean_proximity').value
        };

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) throw new Error('Prediction failed');

            const result = await response.json();
            
            // Display result with animation
            resultContainer.classList.remove('hidden');
            
            // Animate number count up if possible, or just show
            const formattedPrice = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
            }).format(result.prediction);
            
            predictionValue.textContent = formattedPrice;
            
            // Scroll to result
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            console.error('Error:', error);
            alert('Something went wrong. Please check your inputs.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Calculate Prediction';
        }
    });

    form.addEventListener('reset', () => {
        resultContainer.classList.add('hidden');
        // Reset range outputs manually
        setTimeout(() => {
            ranges.forEach(range => {
                const input = document.getElementById(range.id);
                const output = document.querySelector(`output[for="${range.id}"]`);
                input.dispatchEvent(new Event('input'));
            });
        }, 0);
    });
});
