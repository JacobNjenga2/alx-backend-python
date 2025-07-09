import aiosqlite
import asyncio

DB_FILE = 'users.db'

async def async_fetch_users():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        print("All users:")
        for row in rows:
            print(row)
        await cursor.close()
        return rows

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        print("Users older than 40:")
        for row in rows:
            print(row)
        await cursor.close()
        return rows

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
