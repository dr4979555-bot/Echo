from services.breeth_service import BreethService


breeth = BreethService()


try:

    result = breeth.search(
        "What is Echo Mind?",
        limit=5
    )

    print("\nBreeth Search Response:")
    print(result)

except Exception as e:

    print("\nBreeth Search Error:")
    print(e)