# API Contracts

**Feature**: Interactive Docusaurus Textbook
**Date**: 2026-02-01
**Phase**: 1 - API Contracts

## Overview

This directory contains API contract definitions for future backend integration. The Docusaurus textbook is currently a static site with no backend, but these contracts define the interfaces needed when backend features (RAG chatbot, authentication, personalization) are implemented.

## Contract Files

1. **content-api.yaml** - Content retrieval and search endpoints
2. **user-progress-api.yaml** - User reading progress tracking (future)
3. **rag-api.yaml** - RAG chatbot integration (future)

## Contract Principles

- **RESTful design**: Standard HTTP methods and status codes
- **JSON responses**: All responses in JSON format
- **Versioning**: API version in URL path (`/api/v1/...`)
- **Error handling**: Consistent error response format
- **Authentication**: JWT tokens for authenticated endpoints (future)
- **Rate limiting**: Documented rate limits for each endpoint

## Usage

These contracts serve as:
1. **Documentation**: Clear interface definitions for future implementation
2. **Testing**: Contract tests can be written before implementation
3. **Frontend integration**: Frontend can be designed with these contracts in mind
4. **Backend specification**: Backend team has clear requirements

## Status

- ✅ Content API: Defined (static site, no backend needed yet)
- 🔄 User Progress API: Defined (future implementation)
- 🔄 RAG API: Defined (future implementation)

## Notes

The textbook currently operates as a static site with no backend. These contracts will be implemented when:
- User authentication is added (Better-Auth integration)
- RAG chatbot is integrated
- Personalization features are enabled
