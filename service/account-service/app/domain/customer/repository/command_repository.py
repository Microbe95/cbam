class CustomerCommandRepository:
    async def create_customer(self, **kwargs):
        return "repository: create_customer 호출됨"

    async def update_customer(self, **kwargs):
        return "repository: update_customer 호출됨"

    async def delete_customer(self, **kwargs):
        return "repository: delete_customer 호출됨"
