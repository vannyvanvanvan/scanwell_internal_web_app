 
# Scanwell Logistics - Shipping Management System 

## Overview

This project is a shipping management system for **Scanwell Logistics** built using **Flask**. It provides real-time tracking of shipping schedules, space reservations, and user activity using **Redis** and **Docker**.

----------

## **Getting Started**

### **1. Setting Up the Environment**

Users must navigate to the project directory before executing commands:

```
cd Flask_shipping
```

#### **Install Dependencies**

Ensure all necessary dependencies are installed:

```
pip install -r requirements.txt
```

Additionally, **Docker** and **Redis** are required. Install them before proceeding.

----------

## **Why Use Docker and Redis?**

### **Docker:**
![Docker logo](https://raw.githubusercontent.com/docker-library/docs/c350af05d3fac7b5c3f6327ac82fe4d990d8729c/docker/logo.png)

-   Ensures **consistent environment setup** across different machines.
    
-   Packages dependencies inside a **container**, preventing version conflicts.
    
-   Simplifies deployment with **one command** instead of manual installation.
    

### **Redis:**
![Redis logo](https://avatars.githubusercontent.com/u/1529926?s=200&v=4)

-   Provides **real-time tracking** of users and shipping statuses.
    
-   Acts as an **in-memory database**, making queries much faster than SQL.
    
-   Stores **temporary user session data**, reducing load on the main database.
    

----------

## **Running the Server**

### **1. Create the Database**

To initialize the database file and enable multi-threading:

```
py -m driver --with-threads
```

### **2. Run Database Setup**

Execute the following commands to set up the database schema and insert basic data:

```
py -m setup.shipping_db_setup
py -m setup.user_db_setup
```

----------

## **Setting Up Docker and Redis**

### **1. Install Docker**

For Windows users:

-   Download Docker from: [Docker Desktop](https://docs.docker.com/get-started/get-docker/)
    
-   Open **PowerShell** and log in:
    

```
docker login
```

You can log in using **your username & password**, a **webpage authentication**, or a **Personal Access Token**.

**Note:** Personal Access Tokens work better in some cases.

### **2. Run Redis in Docker**

Start the Redis container:

```
docker run --name redis-container -d -p 6379:6379 redis:6
```

Verify Redis is running:

```
docker ps
```
```

 CONTAINER ID   IMAGE     COMMAND                  CREATED        STATUS        PORTS                   NAMES                          
 XXXXXXXXXXXX   redis     "docker-entrypoint.s…"   XX hours ago   Up XX hours   0.0.0.0:6379-6379/tcp   redis-container

```

If Redis is running correctly, you should see something like this in the terminal

### **3. Test Redis Connection**

Check if Redis is responding:

```
docker exec -it redis-container redis-cli ping
```

If Redis is running correctly, it should return:

```
PONG
```

### **4. Running Redis CLI**

To interact with Redis manually:

```
docker exec -it redis-container redis-cli
```

List all active users:

```
KEYS *
```

Check if a specific user is online:

```
GET online_user:1
```

This returns whether the user with **ID = 1** is online.

----------

## **Using the System**

Once Redis and the Flask server are running, users can:

-   **Log in to the web interface** to manage shipping data.
    
-   **Use Redis to monitor real-time user activity.**
    
-   **Check shipping status using the search function.**
    

For any issues, ensure:

-   **Redis is running** (`docker ps` should show `redis-container`).
    
-   **Flask server is running** (`py -m driver --with-threads`).
    

----------

## **Troubleshooting**

### Redis Not Running?

Restart the container:

```
docker start redis-container
```

### Flask Not Working?

Check logs for errors and ensure all dependencies are installed.

----------

## **Conclusion**

This project provides a **new**, **efficient** and **real-time shipping management system** for Scanwell Logistics, ensuring accurate user tracking and seamless data handling. With **Flask, Docker, and Redis**, the system is scalable and optimized for performance.

----------

For further improvements or debugging, refer to the **logs** in Flask and Redis.

### **Developed by:** Ong Man Hei and Shih Wing Hin
Simply test run the server with `python driver.py`

  

---

  

## Frontend Notes:

  

base.html contains things such as a header and footer which are automtically added to very webapage.