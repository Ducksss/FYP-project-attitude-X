FROM tensorflow/serving

COPY . /FYP-project-attitude-X

WORKDIR /FYP-project-attitude-X

EXPOSE 8080

ENTRYPOINT ["tensorflow_model_server", "--model_base_path=/FYP-project-attitude-X/models/fer_model", "--model_name=fer_model"]

CMD ["--rest_api_port=8080","--port=8081"]