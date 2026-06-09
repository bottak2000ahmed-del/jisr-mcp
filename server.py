import os
import httpx
from fastmcp import FastMCP

JISR_KEY = os.environ["JISR_API_KEY"]
JISR_SECRET = os.environ.get("JISR_API_SECRET", "")
JISR_BASE = os.environ.get("JISR_BASE_URL", "https://api.jisr.net")

mcp = FastMCP(name="jisr-connector")

def jisr_headers():
    return {"Authorization": f"Bearer {JISR_KEY}", "Accept": "application/json"}

@mcp.tool
def get_employees(page: int = 1) -> dict:
    """جلب قائمة الموظفين من جسر."""
    r = httpx.get(f"{JISR_BASE}/v1/employees",
                  headers=jisr_headers(), params={"page": page}, timeout=30)
    r.raise_for_status()
    return r.json()

@mcp.tool
def get_attendance(date_from: str, date_to: str) -> dict:
    """جلب سجلات الحضور والانصراف بين تاريخين بصيغة YYYY-MM-DD."""
    r = httpx.get(f"{JISR_BASE}/v1/attendance",
                  headers=jisr_headers(),
                  params={"from": date_from, "to": date_to}, timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)
