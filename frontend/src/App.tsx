import { useState } from "react";
import { LoginPage }    from "./pages/LoginPage";
import { StudentsPage } from "./pages/StudentsPage";
 
export default function App() {
  // token lives in React state — not localStorage.
  // Storing in localStorage is simpler but exposes the token to XSS attacks.
  // Storing in memory means the user has to log in again on page refresh,
  // which is an acceptable tradeoff for a staff-facing internal tool.
  const [token, setToken] = useState<string | null>(null);
 
  const handleLogin = (newToken: string) => setToken(newToken);
  const handleLogout = () => setToken(null);
 
  if (!token) {
    return <LoginPage onLogin={handleLogin} />;
  }
 
  return <StudentsPage token={token} onLogout={handleLogout} />;
}
