from supabase_client import get_supabase_client

def test_conn():
    client = get_supabase_client()

    res = client.table("fact_report").select("*").limit(1).execute()
    print("Connected. Sample:", res.data)

if __name__ == "__main__":
    test_conn()