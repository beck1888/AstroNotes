#!/bin/bash

# Exit on any error
set -e

# Set default region to us-west1 (Oregon)
gcloud config set run/region us-west1

echo "🚀 Building Docker image..."
docker build --platform linux/amd64 -t gcr.io/astro-notes-ai/streamlit-app .

echo "📤 Pushing to Google Container Registry..."
docker push gcr.io/astro-notes-ai/streamlit-app

echo "🎯 Deploying to Cloud Run..."
gcloud run deploy astro-notes --image gcr.io/astro-notes-ai/streamlit-app --region us-west1

echo "✨ Deployment complete!"