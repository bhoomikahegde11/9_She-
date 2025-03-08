import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css"; // ✅ Import Bootstrap

function App() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [activityLog, setActivityLog] = useState([]);

  // Fetch all users
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/get_users") 
      .then(response => setUsers(response.data))
      .catch(error => console.error("Error fetching users:", error));
  }, []);

  // Fetch user activity log
  const fetchActivityLog = (phoneNumber) => {
    axios.get(`http://127.0.0.1:5000/get_user_activity/${phoneNumber}`)
      .then(response => {
        setSelectedUser(phoneNumber);
        setActivityLog(response.data);
      })
      .catch(error => console.error("Error fetching user activity:", error));
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">USSD Users Dashboard</h1>
      
      {/* Users Table */}
      <table className="table table-bordered table-hover">
        <thead className="table-dark">
          <tr>
            <th>Phone Number</th>
            <th>View Activity</th>
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
                  View Activity
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Activity Log Table */}
      {selectedUser && (
        <div className="mt-5">
          <h3>Activity Log for {selectedUser}</h3>
          <table className="table table-striped">
            <thead className="table-light">
              <tr>
                <th>Timestamp</th>
                <th>User Input</th>
                <th>Menu Displayed</th>
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
                  <td colSpan="3" className="text-center">No activity found</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
