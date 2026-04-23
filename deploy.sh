#!/bin/bash
set -e

# ==============================================================================
# Google Cloud Platform Initialization & Deployment Script
# ==============================================================================
PROJECT_ID="election-assistant-prod"
REGION="us-central1"
SERVICE_NAME="election-assistant"
ARTIFACT_REPO="election-repo"

echo "Step 1: Setting up GCP Project..."
gcloud config set project $PROJECT_ID

echo "Step 2: Enabling Required Google APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com \
    secretmanager.googleapis.com \
    aiplatform.googleapis.com \
    civicinfo.googleapis.com \
    translate.googleapis.com \
    geocoding-backend.googleapis.com \
    places-backend.googleapis.com \
    maps-backend.googleapis.com \
    firestore.googleapis.com \
    identitytoolkit.googleapis.com

echo "Step 3: Creating Artifact Registry Repository..."
gcloud artifacts repositories create $ARTIFACT_REPO \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for Election Assistant" || true

echo "Step 4: Submitting Cloud Build..."
gcloud builds submit \
    --tag $REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO/$SERVICE_NAME \
    .

echo "Step 5: Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$ARTIFACT_REPO/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars="ENV=production" \
    --set-secrets="GOOGLE_MAPS_API_KEY=maps_api_key:latest,CIVIC_API_KEY=civic_api_key:latest"

echo "Deployment Successful! The application is now live."
