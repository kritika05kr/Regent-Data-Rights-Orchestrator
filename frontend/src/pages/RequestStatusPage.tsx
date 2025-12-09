import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api/client";

function RequestStatusPage() {
  const { id } = useParams();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchStatus() {
      if (!id) return;
      setLoading(true);
      setError(null);

      try {
        const res = await api.get(`/requests/${id}`);
        setData(res.data);
      } catch (err) {
        console.error(err);
        setError("Could not load request status.");
      } finally {
        setLoading(false);
      }
    }

    fetchStatus();
  }, [id]);

  if (!id) {
    return <p className="text-sm text-red-600">No request ID provided.</p>;
  }

  if (loading) {
    return <p className="text-sm text-slate-600">Loading status for request {id}...</p>;
  }

  if (error) {
    return <p className="text-sm text-red-600">{error}</p>;
  }

  if (!data) {
    return <p className="text-sm text-slate-600">No data found for this request.</p>;
  }

  return (
    <div className="bg-white shadow-sm rounded-md p-6">
      <h1 className="text-xl font-semibold mb-2">Request Status</h1>

      <p className="text-sm text-slate-600 mb-4">
        Request ID: <span className="font-mono">{data.id}</span>
      </p>

      <div className="space-y-1 text-sm mb-4">
        <p>
          <span className="font-medium">Type:</span> {data.request_type}
        </p>
        <p>
          <span className="font-medium">Status:</span>{" "}
          <span
            className={
              data.status === "COMPLETED"
                ? "text-green-700"
                : data.status === "FAILED"
                ? "text-red-700"
                : "text-slate-700"
            }
          >
            {data.status}
          </span>
        </p>
        <p>
          <span className="font-medium">Mode:</span> {data.mode}
        </p>
        <p>
          <span className="font-medium">Email:</span> {data.user_email}
        </p>
        {data.user_customer_id && (
          <p>
            <span className="font-medium">Customer ID:</span> {data.user_customer_id}
          </p>
        )}
      </div>

      <div className="mt-4">
        <h2 className="text-sm font-semibold mb-1">Summary</h2>
        <p className="text-sm text-slate-700 whitespace-pre-wrap">
          {data.final_user_summary || "No summary is available yet."}
        </p>
      </div>
    </div>
  );
}

export default RequestStatusPage;
