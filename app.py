import asyncio

from bentley import main


with open(input("File with emails: ")) as file:
    emails = file.read().strip().split()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    r = loop.run_until_complete(main(emails))

    print(
        f"Quantity: {len(list(filter(lambda a: a == 200, list(r))))}/{len(emails)}"
    )
