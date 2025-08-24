# MLOps OPPE-2: Production-Ready Heart Disease Prediction

This repository contains the complete solution for the MLOps OPPE-2 project. The goal was to create a production-ready, explainable, observable, scalable, and maintainable deployment for a heart disease prediction model on Google Cloud Platform (GCP).

---

## Part 1: Model Explainability

To understand the model's predictions, a SHAP (SHapley Additive exPlanations) analysis was performed on the trained Random Forest model.

**Analysis**:
The SHAP summary plot revealed the key features influencing the model's decision to predict the presence of heart disease. Features are ranked by their impact.

* **`thal` (Thallium Stress Test)**: This is the most influential feature. A value of 2 ("reversable defect") strongly increases the prediction towards having heart disease.
* **`ca` (Number of Major Vessels)**: A higher count of vessels colored during fluoroscopy strongly pushes the prediction towards a positive diagnosis.
* **`cp` (Chest Pain Type)**: More severe types of chest pain increase the likelihood of a heart disease prediction.
* **`thalach` (Maximum Heart Rate Achieved)**: A higher maximum heart rate achieved during exercise tends to *decrease* the model's prediction of heart disease.

---

## Part 2: Fairness Analysis

A fairness analysis was conducted using the Fairlearn library to assess if the model exhibits bias towards the `gender` attribute.

**Results**:
The analysis showed a significant disparity in performance and prediction rates between the two gender groups (0 and 1).

| Metric           | Gender 0 | Gender 1 |
| ---------------- | -------- | -------- |
| **Accuracy** | 81.0%    | 94.1%    |
| **Selection Rate** | 33.3%    | 11.8%    |

**Conclusion**: The model appears to be **biased**. It is significantly more accurate for group 1 and flags group 0 as having heart disease at a much higher rate.

---

## Part 3: Dockerized API Deployment on GCP

The trained model was deployed as a scalable, containerized API on Google Kubernetes Engine (GKE).

**Architecture**:
1.  **Model Artifact**: The best-performing Random Forest model was saved to a `model.joblib` file.
2.  **API**: A web API was created using **FastAPI** to load the model and serve predictions via a `/predict` endpoint.
3.  **Containerization**: The application was packaged into a Docker container using a `Dockerfile`. Dependencies were managed with `requirements.txt`.
4.  **Registry**: The Docker image was pushed to **Google Artifact Registry**.
5.  **Deployment**: The container was deployed to a **GKE Autopilot cluster** using three Kubernetes manifest files:
    * `deployment.yaml`: Defined how to run the container.
    * `service.yaml`: Exposed the application to the internet via a `LoadBalancer`.
    * `hpa.yaml`: Configured a HorizontalPodAutoscaler to scale up to 3 pods based on CPU usage.

**API Endpoint**:
The final API was accessible at `http://34.57.163.156/predict`.

---

## Part 4: Logging and Observability

Per-sample prediction logging was demonstrated by sending 100 randomly generated samples to the live API endpoint.

**Observability**:
The logs for every single request were automatically captured by **Google Cloud Logging**. The screenshot below shows the access logs in the Logs Explorer, filtered to our specific container, confirming that each of the 100 requests was received and processed with a "200 OK" status.

*[Insert your screenshot of the Logs Explorer here]*

---

## Part 5: Performance Monitoring & Timeout Analysis

A high-concurrency load test was performed using `wrk` to simulate 100 concurrent users over 30 seconds.

**Autoscaling Results**:
The HorizontalPodAutoscaler (HPA) performed perfectly. As the load increased, the average CPU utilization spiked to over 500%, and the HPA responded by scaling the number of replicas from the minimum of 1 up to the maximum of 3, as configured.

*[Insert your screenshot of the `kubectl get hpa -w` output here]*

**Performance and Timeout Analysis**:
The `wrk` test results showed that the application was unable to handle the intense load, even with 3 pods.

```text```
Running 30s test @ [http://34.57.163.156/predict](http://34.57.163.156/predict)
  4 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    0.00us    0.00us   0.00us    -nan%
    Req/Sec    2.54      3.80    20.00     90.43%
  114 requests in 30.05s, 21.38KB read
  Socket errors: connect 0, read 0, write 0, timeout 114
Requests/sec:      3.79
Transfer/sec:     728.31B
---

## Part 6: Input Drift Detection

A Kolmogorov-Smirnov (K-S) test was performed to detect input drift between the original training data and the 100 randomly generated samples. A p-value below 0.05 was used as the threshold for detecting drift.

| Feature  | P-value | Drift Detected? |
| :------- | :------ | :-------------- |
| age      | 0.0047  | Yes             |
| trestbps | 0.0000  | Yes             |
| chol     | 0.0000  | Yes             |
| thalach  | 0.0000  | Yes             |
| oldpeak  | 0.0000  | Yes             |

**Conclusion**: Significant drift was detected in all tested numerical features. This indicates the randomly generated data is statistically different from the original training data.

---

## Part 7: Data Poisoning Attack

A data poisoning attack was simulated by flipping the labels of 15% of the training data. A new model was trained on this corrupted data, and its performance was compared against the original model on a clean test set.

**Performance Comparison**:

| Model              | Precision (Class 1) | Recall (Class 1) | F1-Score (Class 1) | Accuracy |
| :----------------- | :------------------ | :--------------- | :----------------- | :------- |
| **Original Model** | 1.00                | 0.64             | 0.78               | 85%      |
| **Poisoned Model** | 0.89                | 0.68             | 0.77               | 83%      |

**Conclusion**: The attack successfully degraded the model's performance, primarily impacting its precision. The poisoned model's ability to be trusted in its positive predictions dropped significantly, demonstrating the model's vulnerability to data quality and security issues.
