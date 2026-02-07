@echo off
REM Quick Start Script for RAG Chatbot MVP (Windows)
REM Run this script after installing Ollama and pulling a model

echo ==========================================
echo RAG Chatbot MVP - Quick Start
echo ==========================================
echo.

REM Check if Ollama is installed
echo Step 1: Checking Ollama installation...
where ollama >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo X Ollama is not installed!
    echo Please install from: https://ollama.ai
    exit /b 1
)
echo √ Ollama is installed
echo.

REM Check if model is available
echo Step 2: Checking for Ollama model...
ollama list | findstr /C:"llama3.2" /C:"mistral" >nul
if %ERRORLEVEL% NEQ 0 (
    echo X No model found!
    echo Please run: ollama pull llama3.2
    exit /b 1
)
echo √ Model is available
echo.

REM Install backend dependencies
echo Step 3: Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo X Failed to install dependencies
    exit /b 1
)
echo √ Dependencies installed
echo.

REM Create data directory
echo Step 4: Creating data directory...
if not exist "data\chroma" mkdir data\chroma
echo √ Data directory created
echo.

REM Run ingestion
echo Step 5: Running document ingestion...
python -m rag.scripts.ingest_textbook --clear
if %ERRORLEVEL% NEQ 0 (
    echo X Ingestion failed
    exit /b 1
)
echo √ Ingestion complete
echo.

echo ==========================================
echo √ Setup complete!
echo ==========================================
echo.
echo To start the backend:
echo   cd backend
echo   python -m src.main
echo.
echo To start the frontend:
echo   cd website
echo   npm start
echo.
echo Then open http://localhost:3000 and click the chat button!
echo.
pause
