import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";  // ✅ Import Bootstrap

function App() {
  const [users, setUsers] = useState([]);  // ✅ Stores full user list
  const [phoneNumber, setPhoneNumber] = useState("");
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  // ✅ Fetch all users on page load
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/get_users")
      .then((response) => {
        setUsers(response.data);
      })
      .catch(() => {
        setError("Failed to fetch users.");
      });
  }, []);

  // ✅ Fetch a specific user
  const fetchUser = () => {
    if (!phoneNumber.trim()) {
      setError("Please enter a valid phone number.");
      return;
    }

    axios
      .get(`http://127.0.0.1:5000/get_user/${phoneNumber}`)
      .then((response) => {
        setUser(response.data);
        setError("");  // Clear any previous errors
      })
      .catch(() => {
        setUser(null);
        setError("User not found or server error.");
      });
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">USSD Users Dashboard</h1>

      {/* ✅ Input to search for a specific user */}
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Enter Phone Number"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
        />
        <button className="btn btn-primary mt-2" onClick={fetchUser}>
          Fetch User
        </button>
      </div>

      {/* ✅ Show error message if any */}
      {error && <div className="alert alert-danger">{error}</div>}

      {/* ✅ Display Specific User Data if Found */}
      {user && (
        <div className="mt-4">
          <h4>Selected User</h4>
          <table className="table table-bordered">
            <thead className="table-dark">
              <tr>
                <th>Phone Number</th>
                <th>Last Menu Accessed</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{user.phone_number || phoneNumber}</td>
                <td>{user.last_menu_accessed || "N/A"}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* ✅ Display Full List of Users */}
      <div className="mt-4">
        <h4>All Users</h4>
        <table className="table table-bordered table-hover">
          <thead className="table-dark">
            <tr>
              <th>Phone Number</th>
              <th>Last Menu Accessed</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? (
              users.map((user, index) => (
                <tr key={index}>
                  <td>{user.phone_number}</td>
                  <td>{user.last_menu_accessed}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="2" className="text-center">
                  No users found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
