from fastapi import FastAPI, Depends

app = FastAPI()


class Pagination:

    def __init__(
        self,
        limit: int = 10,
        skip: int = 0
    ):
        self.limit = limit
        self.skip = skip
        
@app.get('/students')
def get_students(
    query : Pagination =Depends()
):
    return {
        "limit": query.limit,
        "skip" : query.skip
    }