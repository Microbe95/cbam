class CustomerCommandController:

    def __init__(self):
        pass

    async def create_customer(self, **kwargs):
        return "create_customer 호출됨"

    async def update_customer(self, **kwargs):
        return "update_customer 호출됨"

    async def delete_customer(self, **kwargs):
        return "delete_customer 호출됨"