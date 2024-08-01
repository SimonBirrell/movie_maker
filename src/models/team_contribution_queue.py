import asyncio, json

queue = asyncio.Queue()

async def add_contribution_to_queue(movie_project_id, name, contribution):
    global queue 

    print("Adding contribution to queue:", movie_project_id, name, contribution)
    payload = {'movie_project_id': movie_project_id, 'name': name, 'contribution': contribution}
    await queue.put(payload)
