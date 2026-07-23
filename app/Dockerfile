FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy only what the app needs (docker:S6470 - no recursive context copy)
COPY app.py .
COPY static/ static/
COPY templates/ templates/
ENV FLASK_APP=app.py
# Run as a non-root user (docker:S6471)
RUN adduser -D appuser
USER appuser
CMD ["flask", "run", "--host=0.0.0.0"]
