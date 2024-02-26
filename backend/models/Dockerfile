FROM tensorflow/serving:latest

# Copy the contents of the models/fer_model directory into the image
COPY fer_model /models/fer_model

EXPOSE 8080
EXPOSE 8081

CMD ["tensorflow_model_server","--rest_api_port=8080","--port=8081", "--model_base_path=/models/fer_model", "--model_name=fer_model"]