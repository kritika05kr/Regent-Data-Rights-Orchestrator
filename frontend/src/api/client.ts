import axios from "axios";

// Base URL of your FastAPI backend
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export default api;

// ----------------- Types matching backend responses -----------------

export interface CreateRequestPayload {
  email: string;
  customer_id?: string;
  phone_last4?: string;
  request_type: string;
  message?: string;
}

export interface RequestCreateResponse {
  id: number;
  status: string;
  mode: string;
}

export interface RequestStatusResponse {
  id: number;
  request_type: string;
  status: string;
  user_email: string;
  user_customer_id?: string;
  mode: string;
  created_at: string;
  updated_at: string;
  final_user_summary?: string;
}

export interface AdminRequestListItem {
  id: number;
  request_type: string;
  status: string;
  user_email: string;
  user_customer_id?: string;
  mode: string;
  created_at: string;
  updated_at: string;
}

export interface DeletionActionView {
  source_name: string;
  location_type: string;
  action_type: string;
  status: string;
  details?: string;
}

export interface AdminRequestDetail {
  id: number;
  request_type: string;
  status: string;
  user_email: string;
  user_customer_id?: string;
  mode: string;
  created_at: string;
  updated_at: string;
  user_summary?: string;
  admin_report?: string;
  deletion_actions: DeletionActionView[];
}
