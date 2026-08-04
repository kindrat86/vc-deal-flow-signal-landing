// MCP proxy — forwards requests to signals.gitdealflow.com MCP server
// This enables the apex domain to serve MCP without duplicating the server

const SIGNALS_MCP = "https://signals.gitdealflow.com/api/mcp/rpc";

export default async function handler(req, res) {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
    return res.status(200).end();
  }

  // GET — return MCP discovery info
  if (req.method === "GET") {
    res.setHeader("Content-Type", "application/json");
    res.setHeader("Access-Control-Allow-Origin", "*");
    return res.status(200).json({
      name: "GitDealFlow MCP Proxy",
      description: "Proxies to signals.gitdealflow.com MCP server",
      endpoint: "https://gitdealflow.com/api/mcp",
      tools: [
        "get_trending_startups",
        "search_startups_by_sector",
        "get_startup_signal",
        "get_signals_summary",
        "get_scout_receipts",
        "get_methodology"
      ],
      docs_url: "https://signals.gitdealflow.com/developers"
    });
  }

  // POST — forward to signals MCP
  if (req.method === "POST") {
    try {
      const body = req.body;
      const response = await fetch(SIGNALS_MCP, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });
      const data = await response.json();
      res.setHeader("Access-Control-Allow-Origin", "*");
      res.setHeader("Content-Type", "application/json");
      return res.status(200).json(data);
    } catch (err) {
      res.setHeader("Access-Control-Allow-Origin", "*");
      res.setHeader("Content-Type", "application/json");
      return res.status(502).json({
        jsonrpc: "2.0",
        error: { code: -32000, message: "MCP proxy error: " + err.message },
        id: body?.id || null
      });
    }
  }

  res.setHeader("Access-Control-Allow-Origin", "*");
  return res.status(405).json({ error: "Method not allowed" });
}
