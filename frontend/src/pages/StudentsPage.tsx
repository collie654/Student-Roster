// frontend/src/pages/StudentsPage.tsx
import { useState, useEffect } from "react";
import { getStudents, deleteStudent, createStudent, type Student } from "../api";

interface Props {
  token:    string;
  onLogout: () => void;
}

interface NewStudent {
  first_name:   string;
  last_name:    string;
  date_of_birth: string;
  grade_level:  number;
  district_id:  number;
}

export function StudentsPage({ token, onLogout }: Props) {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [saving,   setSaving]   = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const [form, setForm] = useState<NewStudent>({
    first_name:    "",
    last_name:     "",
    date_of_birth: "",
    grade_level:   9,
    district_id:   1,
  });

  useEffect(() => {
    getStudents(token)
      .then(setStudents)
      .catch(err => {
        if (err.message.includes("401")) onLogout();
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

  const handleFormChange = (e: { target: { name: string; value: string } }) => {
    const { name, value } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: name === "grade_level" || name === "district_id"
        ? parseInt(value)
        : value,
    }));
  };

  const handleCreate = async (e: { preventDefault: () => void }) => {
    e.preventDefault();
    setFormError(null);
    setSaving(true);
    try {
      const created = await createStudent(token, form);
      setStudents(prev => [...prev, created]);
      setShowForm(false);
      setForm({
        first_name: "", last_name: "", date_of_birth: "",
        grade_level: 9, district_id: 1,
      });
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Failed to create student");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <p>Loading students...</p>;
  if (error)   return <p style={{ color: "red" }}>Error: {error}</p>;

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Student Roster</h1>
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={() => { setShowForm(prev => !prev); setFormError(null); }}>
            {showForm ? "Cancel" : "+ Add Student"}
          </button>
          <button onClick={onLogout}>Sign Out</button>
        </div>
      </div>

      {/* Create form */}
      {showForm && (
        <form onSubmit={handleCreate} style={{
          margin: "16px 0", padding: 16,
          border: "1px solid #ccc", borderRadius: 8,
          display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12
        }}>
          <h3 style={{ gridColumn: "1 / -1", margin: 0 }}>New Student</h3>

          {formError && (
            <p style={{ gridColumn: "1 / -1", color: "red", margin: 0 }}>
              {formError}
            </p>
          )}

          <label style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            First name
            <input
              name="first_name"
              value={form.first_name}
              onChange={handleFormChange}
              required
            />
          </label>

          <label style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            Last name
            <input
              name="last_name"
              value={form.last_name}
              onChange={handleFormChange}
              required
            />
          </label>

          <label style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            Date of birth
            <input
              type="date"
              name="date_of_birth"
              value={form.date_of_birth}
              onChange={handleFormChange}
              required
            />
          </label>

          <label style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            Grade level
            <input
              type="number"
              name="grade_level"
              value={form.grade_level}
              onChange={handleFormChange}
              min={1}
              max={12}
              required
            />
          </label>

          <label style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            District ID
            <input
              type="number"
              name="district_id"
              value={form.district_id}
              onChange={handleFormChange}
              min={1}
              required
            />
          </label>

          <div style={{ gridColumn: "1 / -1", display: "flex", gap: 8 }}>
            <button type="submit" disabled={saving}>
              {saving ? "Saving..." : "Create Student"}
            </button>
            <button type="button" onClick={() => setShowForm(false)}>
              Cancel
            </button>
          </div>
        </form>
      )}

      {/* Student table */}
      {students.length === 0 ? (
        <p>No students found.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", padding: "8px 0", borderBottom: "1px solid #ccc" }}>Last name</th>
              <th style={{ textAlign: "left", padding: "8px 0", borderBottom: "1px solid #ccc" }}>First name</th>
              <th style={{ textAlign: "left", padding: "8px 0", borderBottom: "1px solid #ccc" }}>Grade</th>
              <th style={{ textAlign: "left", padding: "8px 0", borderBottom: "1px solid #ccc" }}>District</th>
              <th style={{ textAlign: "left", padding: "8px 0", borderBottom: "1px solid #ccc" }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {students.map(student => (
              <tr key={student.id}>
                <td style={{ padding: "8px 0", borderBottom: "1px solid #eee" }}>{student.last_name}</td>
                <td style={{ padding: "8px 0", borderBottom: "1px solid #eee" }}>{student.first_name}</td>
                <td style={{ padding: "8px 0", borderBottom: "1px solid #eee" }}>{student.grade_level}</td>
                <td style={{ padding: "8px 0", borderBottom: "1px solid #eee" }}>{student.district?.name ?? student.district_id}</td>
                <td style={{ padding: "8px 0", borderBottom: "1px solid #eee" }}>
                  <button onClick={() => handleDelete(student.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}