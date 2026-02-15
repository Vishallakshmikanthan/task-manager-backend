# Use official Python Image
FROM python:3.11-slim

#set working directory inside directory
WORKDIR /app

#copy requirments file
COPY requirements.txt .

#install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copy all project files into container
COPY . .

#Expose port
EXPOSE 8000

#Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]