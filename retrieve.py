import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


DECISION_QUERY = """
MATCH (p:Project {id: $project_id})
      -[:HAS_DECISION]->(d:Decision)
      -[:AFFECTS]->(c:Component)
RETURN d.title AS decision,
       d.reason AS reason,
       c.name AS component
"""


BUG_QUERY = """
MATCH (p:Project {id: $project_id})
      -[:HAS_BUG]->(b:Bug)
      -[:OCCURRED_IN]->(c:Component)
OPTIONAL MATCH (b)-[:RESOLVED_BY]->(f:Fix)
RETURN b.title AS bug,
       b.description AS details,
       c.name AS component,
       f.title AS fix,
       f.description AS fix_details
"""


DEPENDENCY_QUERY = """
MATCH (p:Project {id: $project_id})
      -[:HAS_COMPONENT]->(c:Component)
MATCH (c)-[r:DEPENDS_ON|CALLS]->(dependency:Component)
RETURN c.name AS component,
       type(r) AS relationship,
       dependency.name AS connected_to
ORDER BY component, relationship, connected_to
"""


def print_section(title, rows):
    print(f"\n{title}")
    print("=" * len(title))

    if not rows:
        print("No records found.")
        return

    for row in rows:
        print(f"\n- {row}")


def main():
    if not URI or not USERNAME or not PASSWORD:
        raise SystemExit("Missing Neo4j settings. Check your .env file.")

    try:
        with GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD),
        ) as driver:
            driver.verify_connectivity()

            with driver.session(database=DATABASE) as session:
                decisions = [
                    dict(record)
                    for record in session.run(
                        DECISION_QUERY,
                        project_id="shopapi",
                    )
                ]

                bugs = [
                    dict(record)
                    for record in session.run(
                        BUG_QUERY,
                        project_id="shopapi",
                    )
                ]

                dependencies = [
                    dict(record)
                    for record in session.run(
                        DEPENDENCY_QUERY,
                        project_id="shopapi",
                    )
                ]

        print("DevGraph retrieval successful!")
        print_section("TECHNICAL DECISIONS", decisions)
        print_section("HISTORICAL BUGS AND FIXES", bugs)
        print_section("PROJECT DEPENDENCIES", dependencies)

    except Exception as error:
        print(f"Retrieval failed: {type(error).__name__}")
        print(str(error))
        raise SystemExit(1)


if __name__ == "__main__":
    main()