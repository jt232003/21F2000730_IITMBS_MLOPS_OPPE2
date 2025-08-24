# generate_data.py
import pandas as pd
import numpy as np

NUM_SAMPLES = 100

data = {
    'age': np.random.randint(29, 77, NUM_SAMPLES),
    'gender': np.random.randint(0, 2, NUM_SAMPLES),
    'cp': np.random.randint(0, 4, NUM_SAMPLES),
    'trestbps': np.random.randint(94, 200, NUM_SAMPLES),
    'chol': np.random.randint(126, 564, NUM_SAMPLES),
    'fbs': np.random.randint(0, 2, NUM_SAMPLES),
    'restecg': np.random.randint(0, 3, NUM_SAMPLES),
    'thalach': np.random.randint(71, 202, NUM_SAMPLES),
    'exang': np.random.randint(0, 2, NUM_SAMPLES),
    'oldpeak': np.round(np.random.uniform(0, 6.2, NUM_SAMPLES), 1),
    'slope': np.random.randint(0, 3, NUM_SAMPLES),
    'ca': np.random.randint(0, 5, NUM_SAMPLES), # 0-4 as per dataset
    'thal': np.random.randint(0, 4, NUM_SAMPLES) # 0-3 as per dataset
}

df = pd.DataFrame(data)

# Save to a JSON file, with each line being a separate JSON object
df.to_json('random_samples.jsonl', orient='records', lines=True)

print(f"Successfully generated {NUM_SAMPLES} random samples and saved to random_samples.jsonl")