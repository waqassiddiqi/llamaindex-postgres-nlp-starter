import re


FORBIDDEN = re.compile(r";|--|/\*|\*/|DROP|DELETE|UPDATE|INSERT|ALTER|CREATE|RENAME|TRUNCATE", re.I)

ALLOWED_TABLES: set[str] = {
"orders", "customers", "products", "sales", "invoices"
}

def validate_sql(sql: str) -> None:
    if FORBIDDEN.search(sql):
        raise ValueError("Potentially dangerous SQL detected.")
    if sql.count(";") > 0:
        raise ValueError("Multi-statement SQL not allowed.")


def whitelist_tables(sql: str) -> None:
    mentioned = set(re.findall(r"from\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql, flags=re.I))
    mentioned |= set(re.findall(r"join\s+([a-zA-Z_][a-zA-Z0-9_]*)", sql, flags=re.I))
    if not mentioned.issubset(ALLOWED_TABLES):
        bad = mentioned - ALLOWED_TABLES
        raise ValueError(f"Query references disallowed tables: {bad}")


def enforce_limit(sql: str, max_rows: int) -> str:
    if re.search(r"\blimit\b", sql, flags=re.I):
        return sql
    return sql.rstrip() + f" LIMIT {max_rows}"