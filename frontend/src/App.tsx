import { Route, Routes, Link, useLocation } from "react-router-dom";
import UserRequestPage from "./pages/UserRequestPage";
import RequestStatusPage from "./pages/RequestStatusPage";
import AdminDashboardPage from "./pages/AdminDashboardPage";
import AdminRequestDetailPage from "./pages/AdminRequestDetailPage";
import "./index.css"; // IMPORTANT — ensures CSS loads

function App() {
  const location = useLocation();
  const isAdminRoute = location.pathname.startsWith("/admin");

  return (
    <div className="app-root">
      <div className="app-shell">
        {/* HEADER */}
        <header className="app-header">
          <div className="app-title-block">
            <span className="app-title-main">
              Regent <span style={{ color: "#818cf8" }}>Data Rights Orchestrator</span>
            </span>
            <span className="app-title-sub">
              Automating GDPR / CCPA “Right to be Forgotten” across your data estate.
            </span>
          </div>

          {/* NAV */}
          <nav className="app-nav">
            <Link
              to="/"
              style={
                !isAdminRoute
                  ? {
                      backgroundColor: "#e5e7eb",
                      color: "#020617",
                      borderColor: "#e5e7eb",
                      fontWeight: 600,
                    }
                  : {}
              }
            >
              User Portal
            </Link>

            <Link
              to="/admin"
              style={
                isAdminRoute
                  ? {
                      backgroundColor: "#6366f1",
                      color: "#f9fafb",
                      borderColor: "#6366f1",
                      fontWeight: 600,
                    }
                  : {}
              }
            >
              Admin Console
            </Link>
          </nav>
        </header>

        {/* MAIN CONTENT */}
        <main className="app-main">
          <Routes>
            <Route path="/" element={<UserRequestPage />} />
            <Route path="/status/:id" element={<RequestStatusPage />} />
            <Route path="/admin" element={<AdminDashboardPage />} />
            <Route path="/admin/requests/:id" element={<AdminRequestDetailPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
