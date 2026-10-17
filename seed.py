
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(override=True)

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


SEED_QUERY = """
MERGE (p:Project {id: 'shopapi'})
SET p.name = 'ShopAPI',
    p.description = 'Demo project for DevGraph troubleshooting'

MERGE (auth:Component {id: 'auth-module'})
SET auth.name = 'Authentication Module',
    auth.description = 'Validates JWT tokens for protected API routes'

MERGE (client:Component {id: 'api-client'})
SET client.name = 'API Client',
    client.description = 'Sends API requests and attaches authentication headers'

MERGE (orders:Component {id: 'orders-api'})
SET orders.name = 'Orders API',
    orders.description = 'Provides order endpoints for ShopAPI'

MERGE (d:Decision {id: 'decision-jwt-001'})
SET d.title = 'Migrate authentication to JWT',
    d.reason = 'Authentication was migrated to stateless JWT tokens'

MERGE (b:Bug {id: 'bug-header-001'})
SET b.title = 'API client omits JWT Authorization header',
    b.description = 'After the JWT migration, the API client omitted the Authorization Bearer token, causing HTTP 401 errors'

MERGE (f:Fix {id: 'fix-forward-jwt-001'})
SET f.title = 'Forward JWT in Authorization header',
    f.description = 'Update the API client to attach the JWT Bearer token to protected requests'

MERGE (p)-[:HAS_COMPONENT]->(auth)
MERGE (p)-[:HAS_COMPONENT]->(client)
MERGE (p)-[:HAS_COMPONENT]->(orders)
MERGE (p)-[:HAS_DECISION]->(d)
MERGE (p)-[:HAS_BUG]->(b)

MERGE (client)-[:DEPENDS_ON]->(auth)
MERGE (orders)-[:DEPENDS_ON]->(auth)
MERGE (client)-[:CALLS]->(orders)

MERGE (d)-[:AFFECTS]->(auth)
MERGE (b)-[:OCCURRED_IN]->(client)
MERGE (b)-[:RESOLVED_BY]->(f)

RETURN p.name AS project
"""


SUMMARY_QUERY = """
MATCH (p:Project {id: 'shopapi'})
OPTIONAL MATCH (p)-[:HAS_COMPONENT]->(c:Component)
WITH p, count(DISTINCT c) AS components
OPTIONAL MATCH (p)-[:HAS_DECISION]->(d:Decision)
WITH p, components, count(DISTINCT d) AS decisions
OPTIONAL MATCH (p)-[:HAS_BUG]->(b:Bug)
WITH p, components, decisions, count(DISTINCT b) AS bugs
OPTIONAL MATCH (p)-[:HAS_BUG]->(:Bug)-[:RESOLVED_BY]->(f:Fix)
RETURN p.name AS project,
       components,
       decisions,
       bugs,
       count(DISTINCT f) AS fixes
"""


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
                record = session.run(SEED_QUERY).single()
                print(f"Seeded graph for: {record['project']}")

                summary = session.run(SUMMARY_QUERY).single()
                print("\nGraph verification:")
                print(f"Components: {summary['components']}")
                print(f"Decisions:  {summary['decisions']}")
                print(f"Historical bugs: {summary['bugs']}")
                print(f"Fixes: {summary['fixes']}")

        print("\nDevGraph knowledge graph created successfully!")

    except Exception as error:
        print(f"Seeding failed: {type(error).__name__}")
        print(str(error))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
