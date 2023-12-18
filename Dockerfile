# References: https://github.com/reevald/learn-deploy-model-tfserving/blob/main/Dockerfile
FROM tensorflow/serving:2.13.0

# Copy model into image container
COPY ./saved_model /models/kulinerin-app

# Setting environment variables
ENV MODEL_NAME kulinerin-app
ENV MODEL_BASE_PATH /models
