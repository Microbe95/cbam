class CustomerCommandService:
    async def create_customer(self, **kwargs):
        return "service: create_customer 호출됨"

    async def update_customer(self, **kwargs):
        return "service: update_customer 호출됨"

    async def delete_customer(self, **kwargs):
        return "service: delete_customer 호출됨"
