import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/client";

function AdminDashboardPage() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchRequests() {
      setLoading(true);
      setError(null);
      try {
        const res = await api.get("/admin/requests");
        setItems(res.data);
      } catch (err) {
        console.error(err);
        setError("Could not load requests.");
      } finally {
        setLoading(false);
      }
    }
    fetchRequests();
  }, []);

  const total = items.length;
  const completed = items.filter((r) => r.status === "COMPLETED").length;
  const failed = items.filter((r) => r.status === "FAILED").length;
  const inProgress = items.filter(
    (r) => r.status !== "COMPLETED" && r.status !== "FAILED"
  ).length;

  return (
    <div>
      <div className="admin-header-row">
        <div>
          <div className="admin-header-title">Admin console</div>
          <div className="admin-header-sub">
            Monitor all GDPR / CCPA data-rights requests and inspect the deletion pipeline.
          </div>
        </div>
        <div className="admin-data-pill">
          Data sources: SQL · (Mongo later) · ADLS-like files
        </div>
      </div>

      <div className="admin-metrics">
        <div className="metric-card">
          <div className="metric-label">Total requests</div>
          <div className="metric-value">{total}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Completed</div>
          <div className="metric-value" style={{ color: "#bbf7d0" }}>
            {completed}
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Failed</div>
          <div className="metric-value" style={{ color: "#fecaca" }}>
            {failed}
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-label">In progress / other</div>
          <div className="metric-value" style={{ color: "#fed7aa" }}>
            {inProgress}
          </div>
        </div>
      </div>

      <div className="requests-panel">
        <div className="requests-panel-header">
          <div className="requests-panel-title">All requests</div>
          <div className="requests-panel-sub">
            Click on a row to open the full audit trail for that request.
          </div>
        </div>

        {loading && <div className="requests-panel-sub">Loading requests…</div>}
        {error && <div className="alert-error">{error}</div>}

        {!loading && !error && (
          <>
            {items.length === 0 ? (
              <div className="requests-panel-sub">
                No requests yet. Submit one from the User Portal.
              </div>
            ) : (
              <div className="requests-table-wrapper">
                <table className="requests-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Type</th>
                      <th>Status</th>
                      <th>Email</th>
                      <th>Customer ID</th>
                      <th>Mode</th>
                      <th>Created</th>
                      <th>Inspect</th>
                    </tr>
                  </thead>
                  <tbody>
                    {items.map((r: any) => {
                      let pillClass = "status-pill";
                      if (r.status === "COMPLETED") pillClass += " status-pill--success";
                      else if (r.status === "FAILED") pillClass += " status-pill--failed";

                      return (
                        <tr key={r.id}>
                          <td style={{ fontFamily: "monospace" }}>{r.id}</td>
                          <td>{r.request_type}</td>
                          <td>
                            <span className={pillClass}>{r.status}</span>
                          </td>
                          <td>{r.user_email}</td>
                          <td style={{ color: "#94a3b8" }}>{r.user_customer_id || "—"}</td>
                          <td style={{ color: "#cbd5f5" }}>{r.mode}</td>
                          <td style={{ color: "#9ca3af" }}>
                            {new Date(r.created_at).toLocaleString()}
                          </td>
                          <td>
                            <Link to={`/admin/requests/${r.id}`} className="view-button">
                              View <span style={{ fontSize: "9px" }}>↗</span>
                            </Link>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default AdminDashboardPage;
