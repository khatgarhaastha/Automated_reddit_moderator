
# Automated Reddit Moderator

This project is an **LLM-powered moderation tool** for Reddit that periodically scans subreddit submissions and flags posts that violate predefined rules. It leverages a **local language model (via Ollama)** to interpret content and determine compliance with subreddit-specific guidelines.

---

## Features

- Periodic scanning of Reddit submissions using `praw`
- Natural language rule enforcement using LLMs (e.g., LLaMA)
- Custom rules per subreddit stored in AWS DynamoDB
- Cloud-native architecture with support for local inference
- Post metadata and violations logged to DynamoDB

---

## Project Structure

```

.
├── main.py                  # Entry point that triggers moderation pipeline
├── mod\_pipeline.py          # Orchestrates Reddit data pull and moderation
├── comment\_evaluator.py     # Evaluates post content against rules using LLM
├── dynamodb\_handler.py      # Handles reading/writing to DynamoDB tables
├── requirements.txt         # Python dependencies
├── .env.example             # Template for environment variables

````
## Project Architecture

![Architecture](architecture.png)


## How It Works

1. **Fetch submissions** using Reddit API (`praw`)
2. **Retrieve subreddit-specific rules** from `reddit-subreddit-rules` table (DynamoDB)
3. **Evaluate each post** using an LLM via `LangChain` and `Ollama`
4. **Log metadata and violations** into `reddit-submissions` table (DynamoDB)

---

## Requirements

* Python 3.10+
* AWS account with access to DynamoDB
* Reddit developer credentials
* Ollama installed locally with a supported LLM (e.g., LLaMA 3)

---

## Tech Stack

* **PRAW** – Reddit API client
* **LangChain + Ollama** – LLM orchestration and inference
* **Boto3** – AWS DynamoDB integration
* **Python-dotenv** – Secure environment variable handling

---

## DynamoDB Tables

### `reddit-subreddit-rules`

* **Partition key:** `subreddit`
* **Attributes:** `rules` (list of moderation rules)

### `reddit-submissions`

* **Partition key:** `submission_id`
* **Attributes:** metadata like title, content, subreddit, evaluation result

