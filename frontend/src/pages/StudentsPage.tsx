import { useState, useEffect } from "react";
import { getStudents, deleteStudent } from "../api";
import type { Student } from "../api"
 
interface Props {
  token:    string;
  onLogout: () => void;
}
 
export function StudentsPage({ token, onLogout }: Props) {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState<string | null>(null);
 
  // Fetch students when the component mounts.
  // The empty [] dependency array means 'run once on mount'.
  useEffect(() => {
    getStudents(token)
      .then(setStudents)
      .catch(err => {
        if (err.message.includes("401")) onLogout(); // token expired
        else setError(err.message);
      })
      .finally(() => setLoading(false));
  }, [token]);
 
  const handleDelete = async (id: number) => {
    if (!confirm("Delete this student?")) return;
    try {
      await deleteStudent(token, id);
      setStudents(prev => prev.filter(s => s.id !== id));
    } catch (err) {
      alert("Delete failed: " + (err instanceof Error ? err.message : "unknown"));
    }
  };
 
  // Always handle all three states: loading, error, empty
  if (loading) return <p>Loading students...</p>;
  if (error)   return <p style={{ color: "red" }}>Error: {error}</p>;
 
  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <h1>Student Roster</h1>
        <button onClick={onLogout}>Sign Out</button>
      </div>
 
      {students.length === 0 ? (
        <p>No students found.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Last Name</th>
              <th>First Name</th>
              <th>Grade</th>
              <th>District</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {students.map(student => (
              <tr key={student.id}>
                <td>{student.last_name}</td>
                <td>{student.first_name}</td>
                <td>{student.grade_level}</td>
                <td>{student.district?.name ?? student.district_id}</td>
                <td>
                  <button onClick={() => handleDelete(student.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
