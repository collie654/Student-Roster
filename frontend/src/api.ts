const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
 
// types
export interface Student {
  id:          number;
  first_name:  string;
  last_name:   string;
  grade_level: number;
  district_id: number;
  district?: { id: number; name: string };
}
 
export interface AuthToken {
  access_token: string;
  token_type:   string;
}
 
// helper
async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
  token?: string,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(options.headers as Record<string, string> ?? {}),
  };
  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T; // No Content
  return res.json() as Promise<T>;
}
 
// auth 
export async function login(email: string, password: string): Promise<AuthToken> {
  // Login uses form encoding (required by OAuth2PasswordRequestForm)
  const body = new URLSearchParams({ username: email, password });
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body.toString(),
  });
  if (!res.ok) throw new Error("Invalid email or password");
  return res.json();
}
 
// students
export const getStudents = (token: string, districtId?: number): Promise<Student[]> =>
  apiFetch<Student[]>(
    `/students/${districtId ? `?district_id=${districtId}` : ""}`,
    {}, token
  );
 
export const getStudent = (token: string, id: number): Promise<Student> =>
  apiFetch<Student>(`/students/${id}`, {}, token);
 
export const createStudent = (token: string, data: Omit<Student, "id" | "district">): Promise<Student> =>
  apiFetch<Student>("/students/", { method: "POST", body: JSON.stringify(data) }, token);
 
export const deleteStudent = (token: string, id: number): Promise<void> =>
  apiFetch<void>(`/students/${id}`, { method: "DELETE" }, token);
