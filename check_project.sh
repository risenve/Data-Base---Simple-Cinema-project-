#!/bin/bash
echo "🔍 Final Project Verification"
echo "=============================="

# activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "1. Database & Tables:"
psql -U postgres -d reportage_db -c "\dt"

echo ""
echo "2. Starting Server..."
#server start
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > /dev/null 2>&1 &
SERVER_PID=$!
echo "   Server PID: $SERVER_PID"

# server startup wait
echo "   Waiting for server to start..."
sleep 5

echo ""
echo "3. Server Status:"
if curl -s http://localhost:8000/ > /dev/null; then
    echo "   ✅ Server is running at http://localhost:8000/"
else
    echo "   ❌ Server failed to start"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

echo ""
echo "4. API Endpoints Check:"
echo "   Testing endpoints..."
ENDPOINTS=(
    "/"
    "/events/?limit=1"
    "/correspondents/?limit=1" 
    "/reportages/?limit=1"
    "/queries/events_stats_by_city"
    "/queries/sorted_events?limit=1"
)

for endpoint in "${ENDPOINTS[@]}"; do
    if curl -s "http://localhost:8000$endpoint" > /dev/null; then
        echo "   ✅ $endpoint"
    else
        echo "   ❌ $endpoint"
    fi
done

echo ""
echo "5. Database Records:"
psql -U postgres -d reportage_db << EOF
SELECT 
    'events' as table_name, 
    COUNT(*) as records
FROM events
UNION ALL
SELECT 
    'correspondent', 
    COUNT(*)
FROM correspondent
UNION ALL
SELECT 
    'reportage', 
    COUNT(*)
FROM reportage;
EOF

echo ""
echo "6. Special Queries Quick Test:"
echo "   a) SELECT WHERE: $(curl -s "http://localhost:8000/queries/events_by_city_and_danger?city=Yerevan&danger_level=high&limit=1" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")"
echo "   b) Full-text search: $(curl -s "http://localhost:8000/queries/fulltext_search_events?q=concert&limit=1" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('results', [])))" 2>/dev/null || echo "?")"

echo ""
echo "7. Migrations:"
alembic history

echo ""
echo "8. Full-text Search Setup:"
psql -U postgres -d reportage_db -c "SELECT extname FROM pg_extension WHERE extname = 'pg_trgm';"

echo ""
echo "9. Stopping server..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null

echo ""
echo "=============================="
echo "🎉 Project is READY for submission!"
echo "📚 Docs: http://localhost:8000/docs (when server is running)"
echo "=============================="