#  Profile API

A simple FastAPI endpoint that returns a static user profile along with the current UTC time and a random cat fact.

---

##  Features

-   **Fast & Modern:** Built with FastAPI.
-   **Rate Limited:** Protects the endpoint from excessive requests.
-   **External API Call:** Fetches data from the [Cat Fact Ninja API](https://catfact.ninja/fact).

---

##  Getting Started (Local Development)

Follow these steps to run the project on your own machine.

### 1. Clone the Repository

```bash
git clone https://github.com/JoseAyobami/hng
cd hng
```

### 2. Create and Activate a Virtual Environment

-   **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
-   **macOS / Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
uvicorn main:app --reload
```

The application will be running at `http://127.0.0.1:8000`.

---

##  Deployment on Railway

Follow these steps to deploy the application using Railway.

### 1. Push to GitHub

Make sure your project is pushed to a GitHub repository.

### 2. Create a New Railway Project

1.  Go to your [Railway Dashboard](https://railway.app/dashboard).
2.  Click **New Project** and select **Deploy from GitHub repo**.
3.  Choose your repository.

### 3. Configure the Start Command

Railway will likely detect this is a Python project. You need to tell it how to start the server.

1.  In your project's dashboard, go to the **Settings** tab.
2.  Find the **Deploy** section.
3.  In the **Start Command** field, enter the following:

    ```bash
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```

    This command ensures the server is accessible publicly within the Railway container and uses the port provided by Railway.

### 4. Deploy

Railway will automatically build and deploy your application. Once it's done, you will get a public URL to access your live API (e.g., `https://your-project-name.up.railway.app`).

---

##  API Endpoint

You can access the user profile by making a GET request to the `/me` endpoint on your local or deployed server.

-   **Method:** `GET`
-   **URL:** `/me`

#### Example Response:

```json
{
  "status": "success",
  "user": {
    "email": "bamjoe46_4@gmail.com",
    "name": "Joseph Ayeni",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-19T12:00:00.000000Z",
  "fact": "Cats have over 20 muscles that control their ears."
}
```
