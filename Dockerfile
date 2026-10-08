# 1. Start from a small official Python image
FROM python:3.12-slim
 
# 2. Work inside /app in the container
WORKDIR /app
 
# 3. Install libraries first (cached if requirements don't change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# 4. Copy the app code
COPY . .
 
# 5. The app listens on port 5000
EXPOSE 5000
 
# 6. Command that runs when the container starts
CMD ["python", "app.py"]