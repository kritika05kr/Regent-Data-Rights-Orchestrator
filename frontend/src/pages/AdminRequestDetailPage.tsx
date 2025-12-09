import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/client";

function AdminRequestDetailPage() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDetail() {
      if (!id) return;
      setLoading(true);
      setError(null);
      try {
        const res = await api.get(`/admin/requests/${id}`);
        setData(res.data);
      } catch (err: any) {
        console.error(err);
        setError("Could not load request detail.");
      } finally {
        setLoading(false);
      }
    }
    fetchDetail();
  }, [id]);

  if (!id) return <div className="alert-error">No request ID provided.</div>;
  if (loading) return <div className="requests-panel-sub">Loading detail for request {id}…</div>;
  if (error) return <div className="alert-error">{error}</div>;
  if (!data) return <div className="requests-panel-sub">No data found for this request.</div>;

  let statusClass = "detail-status-pill";
  if (data.status === "COMPLETED") statusClass += " detail-status-pill--success";
  else if (data.status === "FAILED") statusClass += " detail-status-pill--failed";

  return (
    <div>
      <div className="detail-header-row">
        <div>
          <div className="detail-breadcrumb">
            <Link to="/admin" className="detail-back-link">
              ← Back to all requests
            </Link>
            <span>/</span>
            <span style={{ fontFamily: "monospace" }}>Request #{data.id}</span>
          </div>
          <div className="detail-title">
            Request #{data.id} — {data.request_type}
          </div>
          <div className="detail-sub">
            Inspect identity verification, data discovery, and policy actions applied for this
            request.
          </div>
        </div>
        <div className="detail-badges">
          <span className={statusClass}>{data.status}</span>
          <span style={{ color: "#9ca3af" }}>
            Mode: <span style={{ color: "#a5b4fc", fontWeight: 600 }}>{data.mode}</span>
          </span>
        </div>
      </div>

      {/* 2-column layout */}
      <div className="detail-grid">
        {/* Left: meta + summaries */}
        <div className="detail-card">
          <div className="detail-card-title">Request metadata</div>
          <div className="detail-card-sub">
            Who requested, when, and the identifiers that Regent used.
          </div>

          <div className="detail-meta-grid">
            <div>
              <div className="detail-meta-label">Email</div>
              <div className="detail-meta-value" style={{ fontFamily: "monospace" }}>
                {data.user_email}
              </div>
            </div>
            <div>
              <div className="detail-meta-label">Customer ID</div>
              <div className="detail-meta-value" style={{ fontFamily: "monospace" }}>
                {data.user_customer_id || "—"}
              </div>
            </div>
            <div>
              <div className="detail-meta-label">Created at</div>
              <div className="detail-meta-value">
                {new Date(data.created_at).toLocaleString()}
              </div>
            </div>
            <div>
              <div className="detail-meta-label">Last updated</div>
              <div className="detail-meta-value">
                {new Date(data.updated_at).toLocaleString()}
              </div>
            </div>
          </div>

          {/* User summary */}
          <div style={{ marginTop: "12px" }}>
            <div className="detail-card-title">User-facing summary</div>
            <div className="detail-card-sub">
              What the end-user would see explaining what happened with their data.
            </div>
            <div className="detail-pre">
              {data.user_summary || "No user summary stored for this request."}
            </div>
          </div>

          {/* Admin report */}
          <div style={{ marginTop: "12px" }}>
            <div className="detail-card-title">Technical audit report</div>
            <div className="detail-card-sub">
              Agent timeline: identity check, discovery, and policy engine decisions.
            </div>
            <pre className="detail-pre">
              {data.admin_report || "No admin report stored for this request."}
            </pre>
          </div>
        </div>

        {/* Right: actions per source */}
        <div className="detail-card">
          <div className="detail-card-title">Policy-driven actions</div>
          <div className="detail-card-sub">
            How Regent applied MASK / DELETE / FLAG across SQL, (Mongo), and ADLS-like folders.
          </div>

          {!data.deletion_actions || data.deletion_actions.length === 0 ? (
            <div className="requests-panel-sub" style={{ marginTop: "10px" }}>
              No actions recorded for this request.
            </div>
          ) : (
            <div className="actions-wrapper">
              {data.deletion_actions.map((a: any, idx: number) => {
                let actionClass = "action-chip";
                if (a.action_type === "mask" || a.action_type === "ActionType.MASK")
                  actionClass += " action-chip--mask";
                else if (a.action_type === "delete" || a.action_type === "ActionType.DELETE")
                  actionClass += " action-chip--delete";
                else if (a.action_type === "flag" || a.action_type === "ActionType.FLAG")
                  actionClass += " action-chip--flag";

                let statusChip = "action-chip";
                if (a.status === "success" || a.status === "ActionStatus.SUCCESS")
                  statusChip += " action-chip--success";

                return (
                  <div key={idx} className="action-card">
                    <div className="action-header">
                      <div>
                        <div className="action-source">{a.source_name}</div>
                        <div className="action-location">
                          Location type: <span>{a.location_type}</span>
                        </div>
                      </div>
                      <div className="action-chips">
                        <span className={actionClass}>{a.action_type}</span>
                        <span className={statusChip}>{a.status}</span>
                      </div>
                    </div>
                    {a.details && <div className="action-details">{a.details}</div>}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminRequestDetailPage;
