import asyncio
from workflow import app
 

async def main():
    final_state = await app.ainvoke({})
    print(f"final_state : {final_state}")


if __name__ == "__main__":
    asyncio.run(main())
