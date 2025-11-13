import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def test_connection():
    # Replace with your actual connection string
    MONGO_URI = "mongodb+srv://kodzgen_db_user:ynJstHDzJp1kr8j1@cluster67.uccsl1k.mongodb.net/?appName=Cluster67"

    print("🔄 Connecting to MongoDB Atlas...")

    try:
        # Create client
        client = AsyncIOMotorClient(MONGO_URI)

        # Test connection
        await client.admin.command('ping')

        print("✅ SUCCESS! Connected to MongoDB Atlas")

        # List databases
        dbs = await client.list_database_names()
        print(f"📦 Available databases: {dbs}")

        # Test write
        db = client['test_db']
        collection = db['test_collection']
        result = await collection.insert_one({"test": "data", "timestamp": "2025-01-01"})
        print(f"✅ Write test successful! Inserted ID: {result.inserted_id}")

        # Test read
        doc = await collection.find_one({"test": "data"})
        print(f"✅ Read test successful! Found: {doc}")

        # Cleanup
        await collection.delete_one({"test": "data"})
        print("🧹 Cleaned up test data")

        client.close()

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nCommon issues:")
        print("1. Check your password is correct")
        print("2. Make sure IP whitelist includes 0.0.0.0/0")
        print("3. Verify connection string format")


if __name__ == "__main__":
    asyncio.run(test_connection())