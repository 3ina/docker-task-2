import os
import motor.motor_asyncio
from pymongo.errors import ConnectionFailure

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "taskdb")

# MongoDB client and database instances
client = None
database = None
tasks_collection = None

async def init_db():
    """Initialize database connection"""
    global client, database, tasks_collection
    
    try:
        # Create a Motor client
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
        
        # Get database instance
        database = client[MONGODB_DB]
        
        # Get tasks collection
        tasks_collection = database.tasks
        
        # Verify connection
        await client.admin.command('ping')
        print(f"Connected to MongoDB at {MONGODB_URL}, database: {MONGODB_DB}")
        
        # Create indexes if needed
        await tasks_collection.create_index("created_at")
        
        return database
    except ConnectionFailure:
        print("Failed to connect to MongoDB. Check if MongoDB is running.")
        raise

async def get_all_tasks():
    """Get all tasks from the database"""
    tasks = []
    cursor = tasks_collection.find().sort("created_at", -1)
    async for document in cursor:
        tasks.append(document)
    return tasks

async def get_task(task_id):
    """Get a single task by ID"""
    return await tasks_collection.find_one({"_id": task_id})

async def create_task(task_data):
    """Create a new task"""
    result = await tasks_collection.insert_one(task_data)
    return await get_task(result.inserted_id)

async def update_task(task_id, task_data):
    """Update an existing task"""
    # Filter out None values
    update_data = {k: v for k, v in task_data.items() if v is not None}
    
    if update_data:
        await tasks_collection.update_one(
            {"_id": task_id},
            {"$set": update_data}
        )
    
    return await get_task(task_id)

async def delete_task(task_id):
    """Delete a task"""
    result = await tasks_collection.delete_one({"_id": task_id})
    return result.deleted_count > 0