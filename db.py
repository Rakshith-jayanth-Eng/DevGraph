import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def main():
    if not URI or not USERNAME or not PASSWORD:
        raise SystemExit(
            "Missing credentials. Check your .env file."
        )

    try:
        with GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD),
        ) as driver:
            driver.verify_connectivity()
            print("Neo4j connection established!")

            with driver.session(database=DATABASE) as session:
                result = session.run(
                    "RETURN 1 AS ok, "
                    "'DevGraph connected' AS message"
                ).single()

            print(result["message"])
            print(f"Test query result: {result['ok']}")

    except Exception as error:
        print(f"Connection failed: {type(error).__name__}")
        print(str(error))
        raise SystemExit(1)


if __name__ == "__main__":
    main()