import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css"; // ✅ Import Bootstrap

function App() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [activityLog, setActivityLog] = useState([]);
  const [searchPhoneNumber, setSearchPhoneNumber] = useState("");
  const [singleUser, setSingleUser] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);  // ✅ Loading state
  const [logLoading, setLogLoading] = useState(false);  // ✅ Loading state for logs

  // ✅ Fetch all users on component mount
  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = () => {
    setLoading(true);
    axios.get("http://127.0.0.1:5000/get_users")
      .then(response => {
        setUsers(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Error fetching users:", error);
        setLoading(false);
      });
  };

  // ✅ Fetch user activity log
  const fetchActivityLog = (phoneNumber) => {
    setLogLoading(true);
    axios.get(`http://127.0.0.1:5000/get_user_activity/${phoneNumber}`)
      .then(response => {
        setSelectedUser(phoneNumber);

        // Ensure activity log exists and is an array
        if (response.data && Array.isArray(response.data)) {
          setActivityLog(response.data); // 🔄 Force React to detect change
        } else {
          setActivityLog([]);
        }

        setLogLoading(false);
      })
      .catch(error => {
        console.error("Error fetching user activity:", error);
        setActivityLog([]);
        setLogLoading(false);
      });
  };

  // ✅ Fetch a single user
  const fetchUser = () => {
    if (!searchPhoneNumber.trim()) {
      setErrorMessage("Please enter a phone number");
      return;
    }

    axios.get(`http://127.0.0.1:5000/get_user/${searchPhoneNumber}`)
      .then(response => {
        setSingleUser(response.data);
        setErrorMessage("");
      })
      .catch(() => {
        setErrorMessage("User not found");
        setSingleUser(null);
      });
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">📊 USSD Users Dashboard</h1>

      {/* 🔎 Search User Section */}
      <div className="mb-4">
        <h3>🔎 Find a Specific User</h3>
        <div className="input-group mb-3">
          <input
            type="text"
            className="form-control"
            placeholder="Enter phone number"
            value={searchPhoneNumber}
            onChange={(e) => setSearchPhoneNumber(e.target.value)}
          />
          <button className="btn btn-success" onClick={fetchUser}>Fetch User</button>
        </div>
        {errorMessage && <p className="text-danger">{errorMessage}</p>}
        {singleUser && (
          <div className="alert alert-info">
            <strong>📞 Phone:</strong> {singleUser.phone_number} <br />
            <strong>📌 Last Menu Accessed:</strong> {singleUser.last_menu_accessed}
          </div>
        )}
      </div>

      {/* 📃 Users Table */}
      <h3>📃 All Users</h3>
      {loading ? (
        <p>Loading users...</p>
      ) : (
        <table className="table table-bordered table-hover">
          <thead className="table-dark">
            <tr>
              <th>📞 Phone Number</th>
              <th>📊 View Activity</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user, index) => (
              <tr key={index}>
                <td>{user.phone_number}</td>
                <td>
                  <button 
                    className="btn btn-primary"
                    onClick={() => fetchActivityLog(user.phone_number)}
                  >
                    View Activity 📜
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* 🛠 Refresh Users */}
      <button className="btn btn-secondary mt-3" onClick={fetchUsers}>
        🔄 Refresh Users
      </button>

      {/* 📊 Activity Log Table */}
      {selectedUser && (
        <div className="mt-5">
          <h3>📊 Activity Log for {selectedUser}</h3>
          {logLoading ? (
            <p>Loading activity log...</p>
          ) : (
            <table className="table table-striped">
              <thead className="table-light">
                <tr>
                  <th>⏰ Timestamp</th>
                  <th>📝 User Input</th>
                  <th>📌 Menu Displayed</th>
                </tr>
              </thead>
              <tbody>
                {activityLog.length > 0 ? (
                  activityLog.map((log, index) => (
                    <tr key={index}>
                      <td>{log.timestamp}</td>
                      <td>{log.user_input}</td>
                      <td>{log.menu_displayed}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="3" className="text-center">⚠️ No activity found</td>
                  </tr>
                )}
              </tbody>
            </table>
          )}

          {/* 🔄 Refresh Activity Log */}
          <button 
            className="btn btn-warning mt-3"
            onClick={() => fetchActivityLog(selectedUser)}
          >
            🔄 Refresh Activity Log
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
