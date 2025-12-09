import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";

function UserRequestPage() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("kritika@example.com");
  const [customerId, setCustomerId] = useState("CUST001");
  const [phoneLast4, setPhoneLast4] = useState("2345");
  const [message, setMessage] = useState(
    "Please delete my personal data associated with this account under GDPR / CCPA."
  );
  const [loading, setLoading] = useState(false);
  const [createdId, setCreatedId] = useState<any>(null);
  const [error, setError] = useState<any>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    setCreatedId(null);

    const payload = {
      email,
      customer_id: customerId || undefined,
      phone_last4: phoneLast4 || undefined,
      request_type: "deletion",
      message,
    };

    try {
      const res = await api.post("/requests", payload);
      setCreatedId(res.data.id);
    } catch (err) {
      console.error(err);
      setError("Something went wrong while creating your request.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-grid">
      {/* Left: explanation */}
      <section className="hero-panel">
        <div>
          <span className="hero-pill">
            <span className="hero-pill-dot" />
            Privacy-first automation · Simulation mode
          </span>
        </div>

        <div>
          <h1 className="hero-title">
            Submit a <span>Right to be Forgotten</span> request
          </h1>
          <p className="hero-text">
            Regent validates your identity, discovers where your personal data lives
            (databases, logs, files), and then orchestrates policy-driven actions like{" "}
            <span className="hero-highlight">masking, deletion, or manual review flags</span>.
          </p>
        </div>

        <div className="hero-steps">
          <div className="hero-step-card">
            <div className="hero-step-title">1. Identity verification</div>
            <div className="hero-step-text">
              Checks email / customer ID / phone against the customer master profile.
            </div>
          </div>
          <div className="hero-step-card">
            <div className="hero-step-title">2. Data discovery</div>
            <div className="hero-step-text">
              Searches transactional DBs and data lake folders for your PII footprint.
            </div>
          </div>
          <div className="hero-step-card">
            <div className="hero-step-title">3. Policy actions</div>
            <div className="hero-step-text">
              Applies configured policies: mask in SQL, simulate delete in logs, flag files.
            </div>
          </div>
        </div>

        <div className="hero-note">
          <strong>Note:</strong> This demo runs in{" "}
          <span style={{ color: "#6ee7b7", fontWeight: 600 }}>simulation mode</span>. No real data
          is deleted — all actions are logged for audit only.
        </div>
      </section>

      {/* Right: form */}
      <section className="form-card">
        <div className="form-card-header">
          <div>
            <div className="form-card-title">Request form</div>
            <div className="form-card-subtitle">
              Provide identifiers so Regent can locate your profile and linked records.
            </div>
          </div>
          <div className="form-mode-pill">
            Mode: <span>SIMULATION</span>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="form-body">
          {/* email */}
          <div className="form-field">
            <label className="form-label">
              Email <span>*</span>
            </label>
            <input
              type="email"
              className="form-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <div className="form-help">
              This should match the email you used when interacting with the product.
            </div>
          </div>

          {/* customer + phone row */}
          <div style={{ display: "grid", gap: "10px" }}>
            <div className="form-field">
              <label className="form-label">
                Customer ID <span>(optional)</span>
              </label>
              <input
                type="text"
                className="form-input"
                value={customerId}
                onChange={(e) => setCustomerId(e.target.value)}
                placeholder="CUST001"
              />
            </div>
            <div className="form-field">
              <label className="form-label">
                Phone (last 4 digits) <span>(optional)</span>
              </label>
              <input
                type="text"
                maxLength={4}
                className="form-input"
                value={phoneLast4}
                onChange={(e) => setPhoneLast4(e.target.value)}
                placeholder="1234"
              />
            </div>
          </div>

          {/* message */}
          <div className="form-field">
            <label className="form-label">
              Message / Reason <span>(optional)</span>
            </label>
            <textarea
              className="form-textarea"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </div>

          <div className="form-footer">
            <button type="submit" disabled={loading} className="form-submit">
              {loading ? "Submitting request..." : "Submit deletion request"}
            </button>
            <div className="form-footer-note">
              You&apos;ll receive a request ID to track status in the portal or admin console.
            </div>
          </div>
        </form>

        {error && <div className="alert-error">{error}</div>}
        {createdId && (
          <div className="alert-success">
            <div style={{ fontWeight: 600 }}>Request submitted successfully.</div>
            <div>
              Your request ID is{" "}
              <span style={{ fontFamily: "monospace", fontWeight: 600 }}>{createdId}</span>.
            </div>
            <button
              style={{
                marginTop: "4px",
                padding: 0,
                border: "none",
                background: "transparent",
                color: "#bbf7d0",
                fontSize: "11px",
                textDecoration: "underline",
                cursor: "pointer",
              }}
              onClick={() => navigate(`/status/${createdId}`)}
            >
              View live status →
            </button>
          </div>
        )}
      </section>
    </div>
  );
}

export default UserRequestPage;
