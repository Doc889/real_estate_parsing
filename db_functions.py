import aiosqlite


async def db_init():
    async with aiosqlite.connect("estate.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS estate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_id TEXT NOT NULL UNIQUE
            );
        """)

        await db.commit()


async def get_data_from_db():
    async with aiosqlite.connect("estate.db") as db:
        cursor = await db.execute("SELECT * FROM estate;")
        rows = await cursor.fetchall()
        await cursor.close()

        return rows


async def insert_db(unique_id):
    async with aiosqlite.connect("estate.db") as db:
        # INSERT OR IGNORE — чтобы не добавлять дубликаты
        await db.execute("""
            INSERT OR IGNORE INTO estate (unique_id)
            VALUES (?);
        """, (unique_id,))

        await db.commit()

        cursor = await db.execute("SELECT COUNT(*) FROM estate;")
        count_row = await cursor.fetchone()
        await cursor.close()
        total = count_row[0]

        if total >= 50:
            await db.execute("""
                DELETE FROM estate
                WHERE id IN (
                    SELECT id FROM estate
                    ORDER BY id ASC
                    LIMIT 40
                );
            """)
