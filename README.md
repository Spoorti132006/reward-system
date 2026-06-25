# Reward System

## Project Overview

Reward System is a full-stack web application built using FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript.

The system processes user transactions, awards reward points, maintains user summaries, and generates rankings based on a scoring algorithm.

## Features

* Add Transactions
* Duplicate Request Prevention
* User Summary
* Ranking System
* Reward Points Calculation
* Basic Abuse Prevention
* REST API using FastAPI
* Frontend deployed on Vercel
* Backend deployed on Render

## Technologies Used

### Backend

* FastAPI
* SQLAlchemy
* SQLite
* Uvicorn

### Frontend

* HTML
* CSS
* JavaScript

## API Endpoints

### POST /transaction

Processes a transaction and awards reward points.

Example Request:

```json
{
  "request_id": "tx1001",
  "user_id": "u1",
  "amount": 100
}
```

### GET /summary/{user_id}

Returns user statistics including:

* Total Amount
* Total Points
* Transaction Count

### GET /ranking

Returns users ranked by score.

Score Formula:

```text
score = total_points + (transaction_count × 5) - penalty
```

## Deployment Links

### Frontend

https://reward-system-roan.vercel.app

### Backend

https://reward-system-vyze.onrender.com

## Author

Spoorti Yalagur
