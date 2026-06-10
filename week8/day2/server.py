from mcp.server.fastmcp import FastMCP
import os
import psycopg2

mcp = FastMCP("Learning MCP Server")


# Tool 1: Calculator
@mcp.tool()
def calculator(expression: str) -> str:
    """Perform basic math calculations."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


# Tool 2: File Reader
@mcp.tool()
def read_file(file_path: str) -> str:
    """Read contents of a file."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"


# Tool 3: Database Query 


@mcp.tool()
def query_db(query: str) -> str:
    """Run SQL query on PostgreSQL using .env config"""

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )

        cur = conn.cursor()
        cur.execute(query)

        if query.strip().lower().startswith("select"):
            rows = cur.fetchall()
            conn.close()
            return str(rows)

        conn.commit()
        conn.close()
        return "Query executed successfully"

    except Exception as e:
        return f"DB Error: {e}"
    

if __name__ == "__main__":
    #print("Starting MCP Server...")
    mcp.run()